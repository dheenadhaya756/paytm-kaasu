// Generate the demo-video voiceover with Gemini TTS only (no Sarvam, so no credits are spent).
// Falls back to the offline Windows voice per segment if Gemini is unavailable.
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
for (const line of fs.readFileSync(path.join(ROOT, ".env"), "utf8").split(/\r?\n/)) {
  const m = line.match(/^([A-Z_]+)=(.*)$/); if (m && !process.env[m[1]]) process.env[m[1]] = m[2].trim();
}
const KEY = process.env.LLM_API_KEY;
const MODELS = ["gemini-3.8-flash-tts", "gemini-2.5-flash-preview-tts", "gemini-2.5-pro-preview-tts"];
const OUT = path.join(ROOT, "video", "vo"); fs.mkdirSync(OUT, { recursive: true });
const segs = JSON.parse(fs.readFileSync(path.join(ROOT, "video", "script.json"), "utf8"));

function wav(pcm, rate) {
  const h = Buffer.alloc(44);
  h.write("RIFF", 0); h.writeUInt32LE(36 + pcm.length, 4); h.write("WAVE", 8); h.write("fmt ", 12);
  h.writeUInt32LE(16, 16); h.writeUInt16LE(1, 20); h.writeUInt16LE(1, 22); h.writeUInt32LE(rate, 24);
  h.writeUInt32LE(rate * 2, 28); h.writeUInt16LE(2, 32); h.writeUInt16LE(16, 34); h.write("data", 36); h.writeUInt32LE(pcm.length, 40);
  return Buffer.concat([h, pcm]);
}
async function gemini(text) {
  for (const model of MODELS) {
    try {
      const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`, {
        method: "POST", headers: { "content-type": "application/json", "x-goog-api-key": KEY },
        body: JSON.stringify({
          contents: [{ parts: [{ text: "Narrate this for a short product film. Warm, calm, sincere Indian English, unhurried, with a gentle pause at each full stop: " + text }] }],
          generationConfig: { responseModalities: ["AUDIO"], speechConfig: { voiceConfig: { prebuiltVoiceConfig: { voiceName: "Charon" } } } },
        }),
      });
      if (!r.ok) { console.warn(model, r.status); continue; }
      const j = await r.json(); const part = j.candidates?.[0]?.content?.parts?.find(p => p.inlineData);
      if (!part) continue;
      const rate = Number((part.inlineData.mimeType.match(/rate=(\d+)/) || [])[1] || 24000);
      return { buf: wav(Buffer.from(part.inlineData.data, "base64"), rate), model };
    } catch (e) { console.warn(model, e.message.slice(0, 80)); }
  }
  return null;
}
for (const s of segs) {
  await new Promise(r => setTimeout(r, fs.existsSync(path.join(OUT, s.id + ".wav")) ? 0 : 22000));
  const file = path.join(OUT, s.id + ".wav");
  if (fs.existsSync(file)) { console.log(s.id, "cached"); continue; }
  const g = KEY ? await gemini(s.text) : null;
  if (g) { fs.writeFileSync(file, g.buf); console.log(s.id, g.model); continue; }
  const ps = `Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.SelectVoice('Microsoft Zira Desktop'); $s.Rate = -1; $s.SetOutputToWaveFile('${file.replace(/'/g, "''")}'); $s.Speak([IO.File]::ReadAllText('${path.join(OUT, s.id + ".txt").replace(/'/g, "''")}')); $s.Dispose()`;
  fs.writeFileSync(path.join(OUT, s.id + ".txt"), s.text);
  execFileSync("powershell", ["-NoProfile", "-Command", ps]);
  console.log(s.id, "offline Windows voice");
}
