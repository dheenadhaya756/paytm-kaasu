// Kaasu demo server. No npm install needed: node server.mjs
// The API key stays here on the server. The browser never sees it.
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";
import { recommend, simulate, loanFor, inr, SHOP } from "./public/sim.js";

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const PUB = path.join(ROOT, "public");
const CACHE = process.env.VERCEL ? "/tmp/kaasu-cache" : path.join(ROOT, "cache"); // Vercel only allows writes in /tmp
fs.mkdirSync(CACHE, { recursive: true });

// ---- config from .env ----
for (const line of (fs.existsSync(path.join(ROOT, ".env")) ? fs.readFileSync(path.join(ROOT, ".env"), "utf8") : "").split(/\r?\n/)) {
  const m = line.match(/^([A-Z_]+)=(.*)$/); if (m && !process.env[m[1]]) process.env[m[1]] = m[2].trim();
}
const KEY = process.env.LLM_API_KEY || "";
const TEXT_MODELS = (process.env.TEXT_MODELS || "gemini-3.5-flash-lite,gemini-3.5-flash,gemini-flash-lite-latest").split(",");
const TTS_MODELS = (process.env.TTS_MODELS || "gemini-3.8-flash-tts,gemini-2.5-flash-preview-tts").split(",");
const TTS_MODEL = TTS_MODELS[0];
const PORT = Number(process.env.PORT || 3000);
const OFFLINE = process.env.OFFLINE === "1" || !KEY;

// ---- Gemini helpers ----
async function gemini(model, body, timeoutMs = 15000) {
  const ctrl = new AbortController(); const t = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`, {
      method: "POST", signal: ctrl.signal,
      headers: { "content-type": "application/json", "x-goog-api-key": KEY },
      body: JSON.stringify(body),
    });
    if (!r.ok) throw new Error(`${model} ${r.status}: ${(await r.text()).slice(0, 200)}`);
    return await r.json();
  } finally { clearTimeout(t); }
}
async function geminiText(body) {
  let last;
  for (const m of TEXT_MODELS) {
    try { const j = await gemini(m, body); return { text: j.candidates?.[0]?.content?.parts?.map(p => p.text || "").join("") || "", model: m }; }
    catch (e) { last = e; console.warn("[ai]", e.message); }
  }
  throw last;
}

// ---- Sarvam fallback: used only when Gemini fails (text answers + Tamil voice) ----
const SARVAM_KEY = process.env.SARVAM_API_KEY || "";
let sarvamClient = null;
async function sarvam() {
  if (!SARVAM_KEY) return null;
  if (!sarvamClient) { const { SarvamAIClient } = await import("sarvamai"); sarvamClient = new SarvamAIClient({ apiSubscriptionKey: SARVAM_KEY }); }
  return sarvamClient;
}
async function sarvamText(system, user) {
  const c = await sarvam(); if (!c) throw new Error("no Sarvam key");
  const r = await c.chat.completionsV2({
    model: "sarvam-105b-conversations",
    messages: [{ role: "system", content: system }, { role: "user", content: user }],
    max_tokens: 300,
  });
  const text = r.choices?.[0]?.message?.content;
  if (!text) throw new Error("Sarvam returned no text");
  return { text, model: "sarvam-105b-conversations" };
}
async function sarvamSpeech(text) {
  const c = await sarvam(); if (!c) return null;
  const lang = /[஀-௿]/.test(text) ? "ta-IN" : "en-IN";
  for (const model of ["bulbul:v4-flash", "bulbul:v3"]) {
    try {
      const r = await c.textToSpeech.convert({ text: text.slice(0, 1500), target_language_code: lang, model });
      const b64 = r.audios?.[0];
      if (b64) { console.log("[tts] Sarvam", model, lang); return Buffer.from(b64, "base64"); }
    } catch (e) { console.warn("[tts] Sarvam", model, String(e.message || e).slice(0, 160)); }
  }
  return null;
}

// ---- Guardrail: every number the AI says must come from the engine ----
function allowedNumbers(facts) {
  const set = new Set();
  const walk = (v) => {
    if (typeof v === "number") { set.add(String(Math.round(v))); set.add(Math.round(v).toLocaleString("en-IN")); set.add(Math.round(v).toLocaleString("en-US")); }
    else if (typeof v === "string") (v.match(/\d[\d,]*/g) || []).forEach(n => set.add(n));
    else if (v && typeof v === "object") Object.values(v).forEach(walk);
  };
  walk(facts);
  ["1", "2", "3", "6", "7", "10", "12", "14", "15", "16", "21", "2026", "2027"].forEach(n => set.add(n));
  return set;
}
function numbersOk(text, allowed) {
  const found = (text.match(/\d[\d,]*/g) || []).map(n => n.replace(/,$/, ""));
  const bad = found.filter(n => !allowed.has(n) && !allowed.has(n.replace(/,/g, "")));
  return { ok: bad.length === 0, bad };
}

// ---- Facts the AI is allowed to use ----
function factsFor(plan) {
  const r = recommend();
  const dailySave = plan?.dailySave ?? r.dailySave;
  const a = simulate({ dailySave, collectUdhaar: true });
  const loan = loanFor(a.shortfall);
  return {
    shop: SHOP.name, owner: SHOP.owner, area: SHOP.area, today: SHOP.today,
    goal: SHOP.goal.label, goalAmount: SHOP.goal.amount, goalDue: SHOP.goal.due, goalItems: SHOP.goal.items,
    daysToGoal: r.daysToGoal, shortfallWithoutPlan: r.baseline.shortfall, shortfallDate: r.baseline.minDate,
    typicalDailyTakeHome: r.dailyFree, dailySave, potAtGoal: dailySave * r.daysToGoal,
    udhaarCustomers: r.udhaarCount, udhaarTotal: r.udhaarTotal, udhaarExpected: r.udhaarExpected,
    loanNeeded: loan, loanDate: r.loanDate, loanInsteadOf: loanFor(r.baseline.shortfall),
    takeHomeAfterSaving: Math.max(0, r.dailyFree - dailySave), lowestBalanceWithPlan: simulate({ dailySave, collectUdhaar: true, loan }).minBalance,
    pongalWeek: "Sales are usually about double normal between 11 and 16 January, so cash recovers after Pongal",
  };
}

function fallbackBrief(f) {
  const loanLine = f.loanNeeded ? `Tell me if you want a planned loan of ${inr(f.loanNeeded)} on 16 December, instead of ${inr(f.loanInsteadOf)} in a hurry.` : "";
  return {
    source: "offline",
    spoken_en: `Good morning ${f.owner}. Pongal stock of ${inr(f.goalAmount)} is due on 6 January. At this pace you will be short by ${inr(f.shortfallWithoutPlan)}. If we keep ${inr(f.dailySave)} aside every day, and collect ${inr(f.udhaarExpected)} of udhaar, most of it is covered. ${loanLine} Shall I start? Say haan.`,
    spoken_ta: `காலை வணக்கம் ${f.owner}. ஜனவரி 6 அன்று பொங்கல் சரக்குக்கு ${inr(f.goalAmount)} தேவை. இப்படியே போனால் ${inr(f.shortfallWithoutPlan)} குறையும். தினமும் ${inr(f.dailySave)} சேமித்து, ${inr(f.udhaarExpected)} கடன் வசூல் செய்தால், பெரும்பகுதி சரியாகிவிடும். தொடங்கட்டுமா? "ஆம்" என்று சொல்லுங்கள்.`,
    actions: [
      { type: "save", title: `Keep ${inr(f.dailySave)} aside every day`, why: `${inr(f.dailySave)} a day for ${f.daysToGoal} days fills the Pongal pot with ${inr(f.potAtGoal)}. You still take home the rest.`, amount: f.dailySave },
      { type: "collect", title: `Collect ${inr(f.udhaarTotal)} of udhaar`, why: `${f.udhaarCustomers} customers owe you. Gentle Paytm reminders usually bring back about ${inr(f.udhaarExpected)}.`, amount: f.udhaarTotal },
      ...(f.loanNeeded ? [{ type: "loan", title: `Planned loan of ${inr(f.loanNeeded)}`, why: `Only the gap that is left. Taken on 16 December, not in a January panic for ${inr(f.loanInsteadOf)}.`, amount: f.loanNeeded }] : []),
    ],
  };
}

const briefCache = new Map();
async function brief(plan) {
  const f = factsFor(plan);
  const key = JSON.stringify(f);
  if (briefCache.has(key)) return briefCache.get(key);
  if (OFFLINE) return fallbackBrief(f);
  const schema = {
    type: "OBJECT",
    properties: {
      spoken_ta: { type: "STRING", description: "What the Soundbox says, in simple spoken Tamil WRITTEN IN TAMIL SCRIPT (தமிழ் எழுத்துக்கள்), never in English letters. Use natural shop Tamil: say கடன் for udhaar and சேமிக்க for saving (for example 'தினமும் ₹600 சேமிக்கலாமா?'). Under 60 words. Mention the shortfall, the daily saving, udhaar and (if any) the loan. End by asking the merchant to say ஆம்." },
      spoken_en: { type: "STRING", description: "The same message in simple Indian English. Under 60 words." },
      actions: { type: "ARRAY", items: { type: "OBJECT", properties: {
        type: { type: "STRING", enum: ["save", "collect", "loan"] },
        title: { type: "STRING", description: "Max 7 words, starts with a verb and includes the rupee amount, e.g. 'Keep Rs 600 aside every day'" },
        why: { type: "STRING", description: "One sentence explaining why, using the facts" },
        amount: { type: "NUMBER", description: "save: dailySave. collect: udhaarTotal. loan: loanNeeded." } }, required: ["type", "title", "why", "amount"] } },
    },
    required: ["spoken_ta", "spoken_en", "actions"],
  };
  const system = `You are Kaasu, a calm and respectful cash-flow assistant for a small Indian shop, speaking through a Paytm Soundbox.
Rules:
- Use ONLY the numbers in FACTS. Never invent or calculate new numbers. Write money as "Rs 12,345".
- Order of preference: the merchant's own savings first, then collecting udhaar, and a loan only for the remaining gap (loanNeeded). If loanNeeded is 0, do not include a loan action.
- Write dates in words, like "6 January" or "16 December", never as 2026-12-16.
- Never pressure. Never promise returns. The merchant decides.
- Tamil must be natural spoken Tamil a shopkeeper in Chennai would use; English words like "Pongal", "udhaar", "Paytm" are fine.`;
  try {
    const { text, model } = await geminiText({
      systemInstruction: { parts: [{ text: system }] },
      contents: [{ role: "user", parts: [{ text: "FACTS:\n" + JSON.stringify(f, null, 1) + "\n\nWrite today's morning brief." }] }],
      generationConfig: { responseMimeType: "application/json", responseSchema: schema, temperature: 0.4 },
    });
    const out = JSON.parse(text);
    const allowed = allowedNumbers(f);
    // Fix amounts by type (the text is still checked below), and keep Tamil in Tamil script
    const want = { save: f.dailySave, collect: f.udhaarTotal, loan: f.loanNeeded };
    out.actions = (out.actions || []).filter(a => want[a.type] !== undefined).map(a => ({ ...a, amount: want[a.type] }));
    const tamilChars = (out.spoken_ta.match(/[஀-௿]/g) || []).length;
    if (tamilChars < out.spoken_ta.length * 0.4) { out.spoken_ta = fallbackBrief(f).spoken_ta; out.taFallback = true; }
    const check = numbersOk([out.spoken_en, ...out.actions.map(a => a.title + " " + a.why)].join(" "), allowed);
    const amountsOk = out.actions.every(a => allowed.has(String(Math.round(a.amount))));
    if (!check.ok || !amountsOk || (!f.loanNeeded && out.actions.some(a => a.type === "loan"))) {
      console.warn("[guardrail] rejected AI brief:", { badNumbers: check.bad, amounts: out.actions.map(a => a.amount), types: out.actions.map(a => a.type) });
      const fb = fallbackBrief(f); fb.source = "guardrail"; fb.rejected = check.bad; return fb;
    }
    const result = { source: model, ...out };
    briefCache.set(key, result);
    return result;
  } catch (e) {
    console.warn("[ai] brief failed, using offline brief:", e.message);
    return fallbackBrief(f);
  }
}

async function ask(question, plan) {
  const f = factsFor(plan);
  if (OFFLINE) return { source: "offline", answer: `I can't reach the AI right now. Your plan: save ${inr(f.dailySave)} a day for Pongal stock of ${inr(f.goalAmount)} due on 6 January.` };
  const system = `You are Kaasu, a friendly cash-flow assistant for ${f.shop}, owned by ${f.owner}.
Language: reply in the same language AND script as the question. English question -> plain English. Tamil script question -> Tamil script. Hindi -> Hindi.
Length: at most 3 short sentences that sound natural when spoken aloud.
Reasoning: protect the Pongal stock plan first. For a new expense, compare it with takeHomeAfterSaving and lowestBalanceWithPlan; if it would put the Pongal plan at risk, suggest waiting until after Pongal week when cash recovers, or paying in small parts. Give a clear recommendation.
Use only numbers from FACTS (write money as "Rs 12,345"). If the question needs a number you don't have, ask for it (for example the price of the fridge). Never give investment advice or promise returns.`;
  try {
    const { text, model } = await geminiText({
      systemInstruction: { parts: [{ text: system }] },
      contents: [{ role: "user", parts: [{ text: "FACTS:\n" + JSON.stringify(f) + "\n\nQUESTION: " + String(question).slice(0, 500) }] }],
      generationConfig: { temperature: 0.3, maxOutputTokens: 300 },
    });
    return { source: model, answer: text.trim() };
  } catch (e) {
    try {
      const { text, model } = await sarvamText(system, `FACTS: ${JSON.stringify(f)}\n\nQUESTION: ${String(question).slice(0, 500)}`);
      console.warn("[ai] Gemini failed, answered with Sarvam");
      return { source: model, answer: text.trim() };
    } catch (e2) {
      return { source: "offline", answer: "The AI is not reachable right now. Please try again in a moment." };
    }
  }
}

// ---- Text to speech (Gemini TTS -> WAV), cached on disk so the demo works offline after one run ----
function wav(pcm, rate = 24000) {
  const h = Buffer.alloc(44);
  h.write("RIFF", 0); h.writeUInt32LE(36 + pcm.length, 4); h.write("WAVE", 8); h.write("fmt ", 12);
  h.writeUInt32LE(16, 16); h.writeUInt16LE(1, 20); h.writeUInt16LE(1, 22); h.writeUInt32LE(rate, 24);
  h.writeUInt32LE(rate * 2, 28); h.writeUInt16LE(2, 32); h.writeUInt16LE(16, 34); h.write("data", 36); h.writeUInt32LE(pcm.length, 40);
  return Buffer.concat([h, pcm]);
}
let geminiTtsBlockedUntil = 0;
async function tts(text) {
  const file = path.join(CACHE, crypto.createHash("sha1").update(TTS_MODEL + text).digest("hex") + ".wav");
  if (fs.existsSync(file)) return fs.readFileSync(file);
  if (OFFLINE) return null;
  let j, last;
  const skipGemini = Date.now() < geminiTtsBlockedUntil;   // quota hit recently: go straight to Sarvam
  for (const m of skipGemini ? [] : TTS_MODELS) {
    try {
      j = await gemini(m, {
        contents: [{ parts: [{ text: "Say warmly and clearly, like a friendly shop assistant: " + text }] }],
        generationConfig: { responseModalities: ["AUDIO"], speechConfig: { voiceConfig: { prebuiltVoiceConfig: { voiceName: "Kore" } } } },
      }, 45000);
      break;
    } catch (e) { last = e; console.warn("[tts]", e.message.slice(0, 120)); if (/ 429/.test(e.message)) geminiTtsBlockedUntil = Date.now() + 15 * 60 * 1000; }
  }
  if (!j) {
    const sv = await sarvamSpeech(text);
    if (sv) { try { fs.writeFileSync(file, sv); } catch {} return sv; }
    throw last || new Error("tts unavailable");
  }
  const part = j.candidates?.[0]?.content?.parts?.find(p => p.inlineData);
  if (!part) return null;
  const rate = Number((part.inlineData.mimeType.match(/rate=(\d+)/) || [])[1] || 24000);
  const buf = wav(Buffer.from(part.inlineData.data, "base64"), rate);
  fs.writeFileSync(file, buf);
  return buf;
}

// ---- HTTP ----
const TYPES = { ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8", ".svg": "image/svg+xml", ".png": "image/png" };
async function readJson(req, limit = 1e5) { let s = ""; for await (const c of req) { s += c; if (s.length > limit) break; } try { return JSON.parse(s || "{}"); } catch { return {}; } }

// ---- NEW: Scheme check. AI reads the distributor bill; plain rules find missed trade-scheme discounts ----
// Illustrative scheme list. In production it would come from brands/distributors (e.g. via ONDC DigiDukaan catalogues).
const SCHEMES = [
  { match: /surf/i, rule: "Buy 10, get 1 free", calc: (it) => Math.floor(it.qty / 10) * it.rate },
  { match: /ghee/i, rule: "3% off on 10 or more", calc: (it) => (it.qty >= 10 ? Math.round(it.qty * it.rate * 0.03) : 0) },
  { match: /salt/i, rule: "2% off on 50 or more", calc: (it) => (it.qty >= 50 ? Math.round(it.qty * it.rate * 0.02) : 0) },
  { match: /marie|sunfeast/i, rule: "₹2 off per pack on 48 or more", calc: (it) => (it.qty >= 48 ? it.qty * 2 : 0) },
];
const SAMPLE_ITEMS = [
  { name: "Surf Excel Easy Wash 1kg", qty: 10, rate: 120, discount: 0 },
  { name: "Aavin Ghee 1L", qty: 12, rate: 640, discount: 0 },
  { name: "Tata Salt 1kg", qty: 50, rate: 26, discount: 26 },
  { name: "Sunfeast Marie 250g", qty: 48, rate: 30, discount: 0 },
  { name: "Aashirvaad Atta 5kg", qty: 10, rate: 265, discount: 0 },
];
const billCache = new Map();
async function readBill(dataUrl) {
  const m = /^data:(image\/[a-z+]+);base64,(.+)$/.exec(dataUrl || ""); if (!m) throw new Error("no image");
  const key = crypto.createHash("sha1").update(m[2]).digest("hex");
  if (billCache.has(key)) return billCache.get(key);
  const { text, model } = await geminiText({
    contents: [{ role: "user", parts: [{ inlineData: { mimeType: m[1], data: m[2] } }, { text: "This is an Indian FMCG distributor bill to a kirana shop. Extract every line item exactly as printed. Use numbers only." }] }],
    generationConfig: { responseMimeType: "application/json", temperature: 0, responseSchema: { type: "OBJECT", properties: {
      distributor: { type: "STRING" }, billNo: { type: "STRING" },
      items: { type: "ARRAY", items: { type: "OBJECT", properties: { name: { type: "STRING" }, qty: { type: "NUMBER" }, rate: { type: "NUMBER" }, discount: { type: "NUMBER" } }, required: ["name", "qty", "rate", "discount"] } } }, required: ["items"] } },
  });
  const out = { ...JSON.parse(text), model }; billCache.set(key, out); return out;
}
async function checkBill(body) {
  let parsed, source;
  const img = body.sample ? "data:image/png;base64," + fs.readFileSync(path.join(PUB, "sample-bill.png")).toString("base64") : body.image;
  try { if (OFFLINE) throw new Error("offline"); parsed = await readBill(img); source = parsed.model; }
  catch (e) {
    console.warn("[bill]", e.message);
    if (!body.sample) return { ok: false, error: "Couldn't read this bill. Try a clearer photo or use the sample bill." };
    parsed = { distributor: "Sri Murugan Agencies", billNo: "SMA/2611/0487", items: SAMPLE_ITEMS }; source = "offline";
  }
  const rows = (parsed.items || []).map((it) => {
    const s = SCHEMES.find((x) => x.match.test(it.name));
    const due = s ? s.calc(it) : 0, got = Math.round(it.discount || 0);
    return { name: it.name, qty: it.qty, rate: it.rate, scheme: s ? s.rule : "No scheme", due, got, missed: Math.max(0, due - got) };
  });
  return { ok: true, source, distributor: parsed.distributor || "Distributor", billNo: parsed.billNo || "", rows, missed: rows.reduce((a, r) => a + r.missed, 0) };
}
function send(res, code, body, type = "application/json") { res.writeHead(code, { "content-type": type, "cache-control": "no-store" }); res.end(type === "application/json" ? JSON.stringify(body) : body); }

// One handler for both the local server and the Vercel function (api/index.mjs).
export async function handler(req, res) {
  const url = new URL(req.url, "http://x");
  try {
    if (url.pathname === "/api/brief" && req.method === "POST") return send(res, 200, await brief(await readJson(req)));
    if (url.pathname === "/api/ask" && req.method === "POST") { const b = await readJson(req); return send(res, 200, await ask(b.question || "", b.plan)); }
    if (url.pathname === "/api/tts" && req.method === "POST") {
      const b = await readJson(req);
      try { const a = await tts(String(b.text || "").slice(0, 1200)); return a ? send(res, 200, a, "audio/wav") : send(res, 503, { error: "tts unavailable" }); }
      catch (e) { console.warn("[tts]", e.message); return send(res, 503, { error: "tts unavailable" }); }
    }
    if (url.pathname === "/api/bill" && req.method === "POST") return send(res, 200, await checkBill(await readJson(req, 8e6)));
    if (url.pathname === "/favicon.ico") { res.writeHead(204); return res.end(); }
    if (url.pathname === "/api/health") return send(res, 200, { ok: true, offline: OFFLINE, gemini: !!KEY, sarvam: !!SARVAM_KEY, models: TEXT_MODELS, tts: TTS_MODEL });
    let p = path.normalize(path.join(PUB, url.pathname === "/" ? "index.html" : url.pathname));
    if (p.startsWith(PUB) && fs.existsSync(p) && fs.statSync(p).isDirectory()) p = path.join(p, "index.html");
    if (!p.startsWith(PUB) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) return send(res, 404, "Not found", "text/plain");
    return send(res, 200, fs.readFileSync(p), TYPES[path.extname(p)] || "application/octet-stream");
  } catch (e) { console.error(e); return send(res, 500, { error: "server error" }); }
}
if (!process.env.VERCEL) http.createServer(handler).listen(PORT, () => console.log(`Kaasu running at http://localhost:${PORT}  (AI: ${OFFLINE ? "offline mode" : "Gemini"})`));
