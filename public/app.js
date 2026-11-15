import { SHOP, simulate, recommend, loanFor, inr, udhaarTotal, udhaarExpected, loanDaily, LOAN } from "/sim.js";

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const rec = recommend();
const GOAL = SHOP.goal.amount;
const DAYS = rec.daysToGoal;
const AVG_DAILY_SALES = 11600;
const state = {
  lang: "ta", tab: "Home", brief: null, txFilter: "all",
  // Pongal plan
  dailySave: rec.dailySave, collect: true, tone: "gentle", loanAccepted: false, kfsRead: false,
  active: false, remindersSent: false, loanRequested: false,
  // products
  goals: [], loans: [], reminded: new Set(), udhaar: SHOP.udhaar.map(u => ({ ...u })), rain: false,
  flow: null,   // { id, step, data }
  confirmed: new Set(["Lakshmi", "Selvi", "Fathima", "Anand"]), bharosa: null, staff: null, galla: null,
};
const T = (ta, en) => (state.lang === "ta" ? ta : en);
const owing = () => state.udhaar.filter(u => !u.bharosa).length;
const udhaarSum = () => state.udhaar.filter(u => !u.bharosa).reduce((s, u) => s + u.amount, 0);

// ---------------- numbers for the Pongal plan (all from the cash engine) ----------------
function numbers() {
  const base = simulate({});
  const afterOwn = simulate({ dailySave: state.dailySave, collectUdhaar: state.collect });
  const loanNeeded = loanFor(afterOwn.shortfall);
  const loan = state.loanAccepted ? loanNeeded : 0;
  const final = simulate({ dailySave: state.dailySave, collectUdhaar: state.collect, loan });
  return {
    shortfall: base.shortfall, willHave: GOAL - base.shortfall,
    saved: state.dailySave * DAYS, udhaar: state.collect ? udhaarExpected() : 0,
    loanNeeded, loan, gapAfterOwn: afterOwn.shortfall, finalShort: final.shortfall,
    takeHome: Math.max(0, rec.dailyFree - state.dailySave), repayDaily: loanNeeded ? loanDaily(loanNeeded) : 0,
  };
}
// Daily money already committed to savings and loan repayments
const committed = () => state.goals.reduce((s, g) => s + g.daily, 0) + state.loans.reduce((s, l) => s + l.daily, 0);
const freeDaily = () => Math.max(0, rec.dailyFree - committed());

// ---------- NEW 1: Save Score. Saving on time earns a lower loan rate from the partner lender (illustrative tiers) ----------
function saveScore() {
  let s = 640;
  if (state.active) s += 60;
  s += Math.min(3, state.goals.filter(g => g.id !== "pongal").length) * 20;
  if (state.remindersSent) s += 10;
  return Math.min(900, s);
}
const RATE_TIERS = [{ min: 720, rate: 1.2 }, { min: 680, rate: 1.35 }, { min: 0, rate: 1.5 }];
const rateFor = (score = saveScore()) => RATE_TIERS.find(r => score >= r.min).rate;
const nextTier = (score = saveScore()) => [...RATE_TIERS].reverse().find(r => r.min > score);

// ---------- NEW 2: payday-timed udhaar reminders ----------
const payday = (u) => ({ "salary week": "1 Dec, 10 am", "month end": "30 Nov, 6 pm", "irregular": "Tomorrow, 9 am", "new": "Next Monday" }[u.usual] || "Tomorrow, 9 am");
const paydayWhy = (u) => ({ "salary week": "gets salary on the 1st", "month end": "pays at month end", "irregular": "no fixed pattern", "new": "new customer" }[u.usual] || "");

// ---------------- design system: one line-icon set (24px grid, 1.8 stroke) ----------------
const I = (d) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${d}</svg>`;
const ICON = {
  bell: I('<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.9 1.9 0 0 0 3.4 0"/>'),
  qr: I('<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><path d="M14 14h3v3h-3zM20 14v.01M14 20h.01M17 20h4v-3"/>'),
  down: I('<path d="M17 7 7 17"/><path d="M17 17H7V7"/>'),
  up: I('<path d="M7 17 17 7"/><path d="M7 7h10v10"/>'),
  trend: I('<path d="m22 7-8.5 8.5-5-5L2 17"/><path d="M16 7h6v6"/>'),
  users: I('<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>'),
  piggy: I('<path d="M19 5c-1.5 0-2.8 1.4-3 2-3.5-1.5-11-.3-11 5 0 1.8 0 3 2 4.5V20h4v-2h3v2h4v-4c1-.5 1.7-1 2-2h2v-4h-2c0-1-.5-1.5-1-2V5z"/><path d="M2 9v1c0 1.1.9 2 2 2h1"/><path d="M16 11h.01"/>'),
  landmark: I('<path d="M3 22h18M6 18v-7M10 18v-7M14 18v-7M18 18v-7"/><path d="m12 2 8 5H4z"/>'),
  plus: I('<path d="M12 5v14M5 12h14"/>'),
  minus: I('<path d="M5 12h14"/>'),
  more: I('<circle cx="5" cy="12" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/>'),
  chev: I('<path d="m9 18 6-6-6-6"/>'),
  alert: I('<circle cx="12" cy="12" r="9"/><path d="M12 8v4M12 16h.01"/>'),
  check: I('<circle cx="12" cy="12" r="9"/><path d="m8.5 12 2.5 2.5 4.5-5"/>'),
  truck: I('<path d="M14 18V6H2v12h2M14 9h4l4 4v5h-2"/><circle cx="7" cy="18" r="2"/><circle cx="17" cy="18" r="2"/><path d="M9 18h6"/>'),
  home: I('<path d="m3 10 9-7 9 7v10a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>'),
  user: I('<circle cx="12" cy="8" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/>'),
  zap: I('<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>'),
  box: I('<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="m3 8 9 5 9-5M12 13v8"/>'),
  fridge: I('<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M5 10h14M9 6v1M9 13v3"/>'),
  shield: I('<path d="M12 2 4 5v6c0 5 3.4 9.3 8 11 4.6-1.7 8-6 8-11V5z"/>'),
  book: I('<path d="M4 19.5V5a2 2 0 0 1 2-2h14v16H6.5A2.5 2.5 0 0 0 4 21.5z"/><path d="M8 7h8"/>'),
  wrench: I('<path d="M14.7 6.3a4 4 0 0 0 5 5L22 14l-8 8-2.3-2.3a4 4 0 0 0-5-5L4 12l8-8z"/>'),
  wallet: I('<path d="M3 7a2 2 0 0 1 2-2h13v4"/><path d="M3 7v11a2 2 0 0 0 2 2h15V9H5a2 2 0 0 1-2-2z"/><path d="M16 14h.01"/>'),
  bellRing: I('<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.9 1.9 0 0 0 3.4 0M2 8c0-2 .7-3.8 2-5M22 8c0-2-.7-3.8-2-5"/>'),
  clock: I('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
  speaker: I('<rect x="5" y="3" width="14" height="18" rx="3"/><circle cx="12" cy="14" r="3.5"/><path d="M9 7h6"/>'),
  link: I('<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>'),
  coins: I('<ellipse cx="9" cy="7" rx="6" ry="3"/><path d="M3 7v4c0 1.7 2.7 3 6 3s6-1.3 6-3V7"/><path d="M9 14v3c0 1.7 2.7 3 6 3s6-1.3 6-3v-4c0-1.7-2.7-3-6-3"/>'),
  handshake: I('<path d="m11 17 2 2a1.4 1.4 0 0 0 2-2"/><path d="m14 14 2.5 2.5a1.4 1.4 0 0 0 2-2L15 11"/><path d="m2 12 5-5 4 4 3-3 3 3 5-5"/><path d="M7 7 2 12l6 6 3-3"/>'),
  cash: I('<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/><path d="M6 12h.01M18 12h.01"/>'),
  mic: I('<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10v1a7 7 0 0 0 14 0v-1M12 18v4"/>'),
  gift: I('<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/>'),
  store: I('<path d="M3 9 5 4h14l2 5"/><path d="M4 9v11h16V9"/><path d="M3 9a3 3 0 0 0 6 0 3 3 0 0 0 6 0 3 3 0 0 0 6 0"/><path d="M10 20v-5h4v5"/>'),
  receipt: I('<path d="M5 2v20l3-2 3 2 3-2 3 2 3-2V2l-3 2-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6M9 16h4"/>'),
  camera: I('<path d="M4 7h3l2-3h6l2 3h3a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1z"/><circle cx="12" cy="13" r="4"/>'),
};
const money = (n, sign = "") => {
  const [i, d] = Math.abs(n).toFixed(2).split(".");
  return `${sign}<span class="cur">₹</span>${Number(i).toLocaleString("en-IN")}<span class="dec">.${d}</span>`;
};
const rs = (n) => "₹" + Math.round(n).toLocaleString("en-IN");
const row = (k, v, cls = "") => `<div class="row-kv ${cls}"><span>${k}</span><b>${v}</b></div>`;

// ---------------- screens ----------------
const ENTER = { scrJourney: "push", scrDone: "pop", scrMain: "fade", scrWelcome: "fade", scrLang: "fade" };
function animate(el, cls, ms = 520) { el.classList.remove(cls); void el.offsetWidth; el.classList.add(cls); clearTimeout(el._t); el._t = setTimeout(() => el.classList.remove(cls), ms); }
function showScreen(id) {
  const was = ["scrLang", "scrWelcome", "scrMain", "scrJourney", "scrDone"].find(s => !$(s).hidden);
  ["scrLang", "scrWelcome", "scrMain", "scrJourney", "scrDone"].forEach(s => ($(s).hidden = s !== id));
  $("statusbar").classList.toggle("dark", ["scrJourney", "scrDone", "scrMain"].includes(id));
  if (was !== id) animate($(id), "enter-" + (was === "scrJourney" && id === "scrMain" ? "back" : ENTER[id]));
}
function openSheet(id) { $("scrim").hidden = false; animate($("scrim"), "in", 300); $(id).hidden = false; animate($(id), "in", 450); }
function closeSheet(id) {
  const el = $(id); if (el.hidden) return;
  el.classList.add("out"); $("scrim").classList.add("out");
  setTimeout(() => { el.hidden = true; el.classList.remove("out"); $("scrim").classList.remove("out");
    if (!document.querySelector(".sheet:not([hidden])")) $("scrim").hidden = true; }, 260);
}
function showTab(tab) {
  state.tab = tab;
  ["Home", "Savings", "Loans", "Udhaar"].forEach(t => ($("pane" + t).hidden = t !== tab));
  document.querySelectorAll(".tab[data-tab]").forEach(b => b.classList.toggle("on", b.dataset.tab === tab));
  renderPanes();
  $("pane" + tab).scrollTop = 0;
  animate($("pane" + tab), "enter", 700);
}
function backToMain() { showScreen("scrMain"); showTab(state.tab); }

// ---------------- HOME ----------------
const TX = [
  { who: "Lakshmi", meta: "UPI · 9:12 am", amt: 180, icon: "user" },
  { who: "Walk-in customer", meta: "UPI · 9:05 am", amt: 64, icon: "user" },
  { who: "Sri Murugan Agencies", meta: "Stock bill · 13 Nov", amt: -61240, icon: "truck" },
  { who: "Ravi", meta: "UPI · 8:41 am", amt: 420, icon: "user" },
  { who: "Selvi", meta: "Udhaar repaid · 12 Nov", amt: 200, icon: "users" },
  { who: "TNEB electricity", meta: "Bill · 10 Nov", amt: -3400, icon: "zap" },
  { who: "Shop rent", meta: "1 Nov", amt: -18000, icon: "home" },
];
function renderHome() {
  const n = numbers();
  const covered = state.active && n.finalShort === 0;
  const owe = 64900 + state.loans.reduce((s, l) => s + l.amount, 0);
  const rows = TX.filter(x => state.txFilter === "all" || (state.txFilter === "in" ? x.amt > 0 : x.amt < 0));
  $("paneHome").innerHTML = `
    <div class="z-top">
      <div class="z-head">
        <div class="z-brand"><img class="ptm" src="/brand/paytm-logo.svg" alt="Paytm"><span>Kaasu</span></div>
        <div class="z-icons"><button type="button" class="z-ib" aria-label="Alerts" data-go="alerts">${ICON.bell}</button><button type="button" class="z-ib" aria-label="Show my shop QR" data-go="qr">${ICON.qr}</button></div>
      </div>
      <div class="z-bal-h"><span>Bank balance</span><span class="z-chip">Murugan Stores</span></div>
      <div class="z-bal">${money(24000)}</div>
      <div class="z-tiles">
        <div class="z-tile"><div class="z-t-h"><span class="z-ic g">${ICON.down}</span>Received</div><div class="z-t-v">${money(162400)}</div><div class="z-t-s">This month</div></div>
        <div class="z-tile"><div class="z-t-h"><span class="z-ic b">${ICON.trend}</span>Profit</div><div class="z-t-v">${money(38520)}</div><div class="z-t-s">October</div></div>
        <div class="z-tile"><div class="z-t-h"><span class="z-ic r">${ICON.up}</span>You owe</div><div class="z-t-v">${money(owe)}</div><div class="z-t-s">${state.loans.length ? "Stock bill + loans" : "Stock bill · Mon"}</div></div>
        <div class="z-tile"><div class="z-t-h"><span class="z-ic a">${ICON.users}</span>Udhaar</div><div class="z-t-v">${money(udhaarSum())}</div><div class="z-t-s">${owing()} customers owe you</div></div>
      </div>
      <button type="button" class="z-alert ${covered ? "ok" : ""}" data-go="pongal">
        <span class="z-al-ic">${covered ? ICON.check : ICON.alert}</span>
        <span class="z-al-t"><b>${covered ? "Pongal stock covered" : `Pongal stock: short by ${rs(n.shortfall)}`}</b><small>${covered ? `Saving ${rs(state.dailySave)} a day · plan active` : "Due 6 Jan · Fix it with Kaasu"}</small></span>
        <span class="z-al-go">${ICON.chev}</span>
      </button>
      <div class="z-grow-h">Grow with Kaasu <span class="new">New</span></div>
      <div class="z-grow">
        <button type="button" data-go="flow:fund"><span class="z-ic a lg">${ICON.gift}</span><b>Pongal Fund</b><small>${state.fund ? `${state.fund.joined} customers joined` : "Customers pre-book"}</small></button>
        <button type="button" data-go="flow:circle"><span class="z-ic b lg">${ICON.store}</span><b>Buy together</b><small>${state.circle ? "Order locked · 6% off" : "5 shops nearby"}</small></button>
        <button type="button" data-go="flow:bill"><span class="z-ic g lg">${ICON.receipt}</span><b>Check a bill</b><small>${state.billClaim ? `${rs(state.billClaim)} claimed` : "Find missed discounts"}</small></button>
        <button type="button" data-go="flow:bharosa"><span class="z-ic b lg">${ICON.handshake}</span><b>Bharosa</b><small>${state.bharosa ? `${rs(state.bharosa.paid)} paid to you` : "Get paid for udhaar"}</small></button>
        <button type="button" data-go="flow:staff"><span class="z-ic a lg">${ICON.users}</span><b>Staff advance</b><small>${state.staff ? `${rs(state.staff.amount)} to ${state.staff.name}` : "Ravi asked ₹1,500"}</small></button>
        <button type="button" data-go="flow:galla"><span class="z-ic g lg">${ICON.cash}</span><b>Galla check</b><small>${state.galla ? state.galla.label : "Close the day"}</small></button>
      </div>
    </div>
    ${state.rain ? `<div class="z-rain"><span class="z-ic a lg">${ICON.shield}</span><span><b>Rain Shield active</b><small>Repayments paused 3 days · ₹3,000 payout received</small></span></div>` : ""}
    <div class="z-actions">
      <button type="button" class="z-pill" data-go="tab:Udhaar">${ICON.down}<span>Collect</span></button>
      <button type="button" class="z-pill" data-go="flow:goal">${ICON.plus}<span>Save</span></button>
      <button type="button" class="z-pill" data-go="flow:loan">${ICON.landmark}<span>Borrow</span></button>
    </div>
    <div class="z-sheet">
      <div class="grabber" aria-hidden="true"></div>
      <div class="z-sh-h"><span>Paytm for Business</span><span class="z-count">Your tools</span></div>
      <div class="svc">${[["qr", "Scan QR"], ["speaker", "Soundbox"], ["down", "Settlements"], ["landmark", "Business loan"], ["link", "Payment links"], ["book", "Khata"], ["shield", "Insurance"], ["coins", "Gold"]].map(([i, l]) => `<button type="button" data-go="svc:${l}"><span class="svc-ic">${ICON[i]}</span><small>${l}</small></button>`).join("")}</div>
      <div class="z-sh-h"><span>Transactions</span><span class="z-count">${rows.length} this week</span></div>
      <div class="z-chips">
        <button type="button" class="z-c ${state.txFilter === "all" ? "on" : ""}" data-tx="all">All</button>
        <button type="button" class="z-c ${state.txFilter === "in" ? "on" : ""}" data-tx="in">Received</button>
        <button type="button" class="z-c ${state.txFilter === "out" ? "on" : ""}" data-tx="out">Paid</button>
      </div>
      <div class="z-list">${rows.map(x => `
        <div class="z-row"><span class="z-avatar ${x.amt < 0 ? "out" : ""}">${ICON[x.icon]}</span>
          <span class="z-r-t"><b>${x.who}</b><small>${x.meta}</small></span>
          <span class="z-amt ${x.amt > 0 ? "in" : ""}">${money(x.amt, x.amt > 0 ? "+" : "−")}</span></div>`).join("")}
      </div>
    </div>`;
}

// ---------------- SAVINGS ----------------
function renderSavings() {
  const total = state.goals.reduce((s, g) => s + g.saved, 0);
  const daily = state.goals.reduce((s, g) => s + g.daily, 0);
  $("paneSavings").innerHTML = `
    <div class="p-head"><div class="p-title">Savings</div><button type="button" class="p-add" data-go="flow:goal">${ICON.plus}<span>New goal</span></button></div>
    <div class="p-sum">
      <div><span>Saved so far</span><b>${money(total)}</b></div>
      <div><span>Auto-saving</span><b>${money(daily)}<small> / day</small></b></div>
    </div>
    <div class="pane-body">
      ${scoreCard()}
      ${state.goals.length ? state.goals.map(g => {
        const pct = Math.min(100, Math.round(g.saved / g.target * 100));
        return `<div class="card goal-card">
          <div class="gc-h"><span class="z-ic b lg">${ICON[g.icon]}</span><div class="gc-t"><b>${esc(g.name)}</b><small>${rs(g.daily)} a day · by ${g.by}</small></div><span class="pill good">Active</span></div>
          <div class="gc-amt">${money(g.saved)} <span>of ${rs(g.target)}</span></div>
          <div class="meter"><i class="ok" style="width:${Math.max(pct, 2)}%"></i></div>
          <div class="two"><button type="button" class="btn-grey sm" data-go="flow:add:${g.id}">${ICON.plus} Add money</button><button type="button" class="btn-grey sm" data-go="flow:withdraw:${g.id}">${ICON.minus} Withdraw</button></div>
        </div>`; }).join("")
      : `<div class="empty"><span class="z-ic b xl">${ICON.piggy}</span><b>No savings goals yet</b><p>Put a little aside from each day's QR collections for stock, rent or a new fridge.</p><button type="button" class="btn-black" data-go="flow:goal">Create a savings goal</button></div>`}
      ${!state.active ? `<button type="button" class="z-alert" data-go="pongal"><span class="z-al-ic">${ICON.alert}</span><span class="z-al-t"><b>Suggested: Pongal stock pot</b><small>Kaasu found a ${rs(numbers().shortfall)} gap on 6 Jan</small></span><span class="z-al-go">${ICON.chev}</span></button>` : ""}
      <div class="card"><div class="eyebrow">How savings work</div>
        <ol class="howto"><li>A small amount moves from your day's QR collections at 9 pm.</li><li>It is kept with a licensed partner for that goal.</li><li>Withdraw any time with your PIN. It reaches your bank the same day.</li></ol></div>
    </div>`;
}

function scoreCard() {
  const s = saveScore(), nx = nextTier(s), pct = Math.round((s - 300) / 600 * 100);
  return `<div class="card score">
    <div class="sc-top"><div><div class="eyebrow">Save Score</div><div class="sc-num">${s}<small> / 900</small></div></div>
      <div class="sc-rate"><b>${rateFor(s)}%</b><small>loan rate a month</small></div></div>
    <div class="sc-bar"><i style="width:${pct}%"></i>${RATE_TIERS.slice(0, 2).map(r => `<span style="left:${Math.round((r.min - 300) / 600 * 100)}%"></span>`).join("")}</div>
    <p class="sc-p">${nx ? `Reach <b>${nx.min}</b> to pay <b>${nx.rate}%</b> instead of ${rateFor(s)}%. Every day you save on time adds to your score.` : `Top tier. You get the best rate from the lending partner.`}</p>
    <div class="sc-how"><span>${ICON.check} Save daily on time</span><span>${ICON.check} Keep goals running</span><span>${ICON.check} Collect udhaar</span></div>
  </div>`;
}

// ---------------- LOANS ----------------
function renderLoans() {
  const out = state.loans.reduce((s, l) => s + l.amount, 0);
  const limit = 100000;
  $("paneLoans").innerHTML = `
    <div class="p-head"><div class="p-title">Loans</div><button type="button" class="p-add" data-go="flow:loan">${ICON.plus}<span>New loan</span></button></div>
    <div class="p-sum">
      <div><span>Outstanding</span><b>${money(out)}</b></div>
      <div><span>Eligible up to</span><b>${money(limit)}</b></div>
    </div>
    <div class="pane-body">
      ${rainCard()}
      ${state.loans.length ? state.loans.map(l => `
        <div class="card goal-card">
          <div class="gc-h"><span class="z-ic r lg">${ICON[l.icon]}</span><div class="gc-t"><b>${esc(l.purpose)}</b><small>${rs(l.daily)} a day · ${l.days} days</small></div><span class="pill ${state.rain ? "warn" : "neutral"}">${state.rain ? "Paused · rain" : l.status}</span></div>
          <div class="gc-amt">${money(l.amount)}</div>
          <div class="timeline"><div class="tl ok">Request sent to lending partner</div><div class="tl">Lender reviews and decides</div><div class="tl">Money reaches ${l.to}</div><div class="tl">Repayment from daily QR collections</div></div>
        </div>`).join("")
      : `<div class="empty"><span class="z-ic r xl">${ICON.landmark}</span><b>No loans</b><p>Borrow for stock, equipment or repairs. Kaasu checks the repayment fits your daily collections before you apply.</p><button type="button" class="btn-black" data-go="flow:loan">Apply for a loan</button></div>`}
      <p class="fine">Loans are offered and decided by Paytm's lending partners, not by AI. Rates shown are illustrative; the lender's Key Fact Statement has the final terms.</p>
    </div>`;
}

// ---------------- UDHAAR ----------------
function renderUdhaar() {
  $("paneUdhaar").innerHTML = `
    <div class="p-head"><div class="p-title">Udhaar</div><button type="button" class="p-add" data-go="flow:udhaar">${ICON.plus}<span>Add</span></button></div>
    <div class="p-sum">
      <div><span>Customers owe you</span><b>${money(udhaarSum())}</b></div>
      <div><span>Customers</span><b>${owing()}</b></div>
    </div>
    <div class="pane-body">
      <button type="button" class="bh-card" data-go="flow:bharosa">
        <span class="z-ic b lg">${ICON.handshake}</span>
        <span class="z-al-t"><b>${state.bharosa ? `Bharosa · ${rs(state.bharosa.paid)} paid to you` : `Bharosa · get paid today for ${rs(bharosaList().reduce((s, u) => s + u.amount, 0))}`}</b><small>${state.bharosa ? "Customers now repay Paytm's lending partner" : `${bharosaList().length} trusted customers · they repay Paytm's partner, not you`}</small></span>
        <span class="z-al-go">${ICON.chev}</span>
      </button>
      ${state.remindersSent && !state.udhaarMiss ? `<button type="button" class="z-alert" data-go="flow:miss"><span class="z-al-ic">${ICON.alert}</span><span class="z-al-t"><b>Demo: 10 days later, 3 haven't paid</b><small>See how Kaasu protects the Pongal plan</small></span><span class="z-al-go">${ICON.chev}</span></button>` : ""}
      ${state.udhaarMiss ? `<div class="z-rain" style="margin:0;background:#e9f8f2"><span class="z-ic g lg">${ICON.check}</span><span><b>Unpaid udhaar covered</b><small>${rs(state.udhaarMiss.gap)} handled · Paytm reminds them once more</small></span></div>` : ""}
      ${state.remindersSent ? "" : `<button type="button" class="btn-black" data-go="flow:remind">${ICON.bellRing} Remind everyone</button>`}
      <div class="card list">
        ${state.udhaar.map((u, i) => `
          <div class="z-row"><span class="z-avatar">${ICON.user}</span>
            <span class="z-r-t"><b>${esc(u.name)}${state.confirmed.has(u.name) ? ` <span class="ok-tag">${ICON.check} Confirmed</span>` : ` <span class="wait-tag">Awaiting confirm</span>`}</b><small>${u.days ? u.days + " days · " : ""}${paydayWhy(u)}</small>${u.bharosa ? `<small class="pd">${ICON.check} Repays Paytm's partner by 15 Dec</small>` : `<small class="pd">${ICON.clock} Best time: ${payday(u)}</small>`}</span>
            <span class="u-right"><b>${rs(u.amount)}</b>${u.bharosa ? `<span class="sent">Paid via Bharosa</span>` : state.reminded.has(u.name) ? `<span class="sent">Scheduled · ${payday(u).split(",")[0]}</span>` : `<button type="button" class="mini" data-remind="${i}">Remind</button>`}</span></div>`).join("")}
      </div>
      <p class="fine">Reminders come from Paytm, not from your shop, so customers don't feel you are chasing them. Sent in each customer's pay week, at most once a week, one-tap pay.</p>
    </div>`;
}
function rainCard() {
  return `<div class="card rain ${state.rain ? "on" : ""}">
    <div class="gc-h"><span class="z-ic ${state.rain ? "a" : "b"} lg">${ICON.shield}</span><div class="gc-t"><b>Rain Shield · மழை கவசம்</b><small>${state.rain ? "Active · heavy rain alert in Velachery" : "Watching IMD alerts for 600042 + your sales"}</small></div><span class="pill ${state.rain ? "warn" : "good"}">${state.rain ? "Active" : "On"}</span></div>
    ${state.rain
      ? row("Loan repayments", "Paused 3 days", "good") + row("Protection payout", "₹3,000 received", "good") + row("Repayments restart", "When sales recover")
      : `<p class="muted-p">If there is a flood alert <b>and</b> your sales and nearby shops' sales drop, Kaasu pauses your loan repayments and an insurance payout reaches you. No claim form.</p>
         <button type="button" class="btn-grey sm" data-go="rain">Simulate Chennai red alert</button>`}
  </div>`;
}
function rainEvent() {
  if (state.rain) return toast("Rain Shield is already active");
  state.rain = true;
  $("sbTop").textContent = "RAIN SHIELD ON";
  const ta = "முருகன், வேளச்சேரியில் கனமழை எச்சரிக்கை. இன்று உங்கள் விற்பனை 70% குறைந்துள்ளது. 3 நாள் கடன் தவணை நிறுத்தப்பட்டது. ₹3,000 பாதுகாப்பு தொகை வந்துள்ளது. பாதுகாப்பாக இருங்கள்.";
  const en = "Murugan, heavy rain alert in Velachery. Your sales are down 70% today. Loan repayments are paused for 3 days and ₹3,000 protection money has reached you. Stay safe.";
  setSpeech(state.lang === "ta" ? ta : en, state.lang === "ta" ? en : ""); speak(state.lang === "ta" ? ta : en, state.lang);
  if (!$("scrMain").hidden) showTab("Loans"); else renderPanes();
  toast("IMD red alert + 70% sales drop: repayments paused, ₹3,000 payout");
}

function renderPanes() { renderHome(); renderSavings(); renderLoans(); renderUdhaar(); }

// =============== JOURNEY ENGINE: every flow uses the same steps, header, button and PIN ===============
const kfs = (amount, days, daily) => row("Loan amount", rs(amount)) + row("Lender", "Paytm lending partner (demo)") +
  row("Repayment", `${rs(daily)} a day · ${days} days`) + row("Total repayable", rs(daily * days)) + row("Cost of loan", rs(daily * days - amount)) +
  row("Foreclosure", "Any time, no charge (demo)");
const optGrid = (key, opts, sel) => `<div class="opts">${opts.map(o => `<button type="button" class="opt ${sel === o.v ? "on" : ""}" data-set="${key}" data-val="${o.v}"><span class="z-ic ${o.c || "b"} lg">${ICON[o.i]}</span><b>${o.l}</b>${o.s ? `<small>${o.s}</small>` : ""}</button>`).join("")}</div>`;
const chips = (key, opts, sel) => `<div class="choices n${opts.length}">${opts.map(o => `<button type="button" class="choice ${sel === o.v ? "on" : ""}" data-set="${key}" data-val="${o.v}"><b>${o.l}</b>${o.s ? `<span>${o.s}</span>` : ""}</button>`).join("")}</div>`;

const GOAL_TYPES = [
  { v: "stock", l: "Festival stock", i: "box", s: "Diwali, Pongal, Ramzan" },
  { v: "rent", l: "Shop rent", i: "home", s: "Never miss the 1st" },
  { v: "fridge", l: "Equipment", i: "fridge", s: "Fridge, freezer, shelf" },
  { v: "emergency", l: "Emergency fund", i: "shield", s: "For bad days" },
  { v: "school", l: "School fees", i: "book", s: "Children's fees" },
  { v: "repair", l: "Shop repair", i: "wrench", s: "Paint, roof, shutter" },
];
const LOAN_TYPES = [
  { v: "stock", l: "Stock purchase", i: "box", c: "r" },
  { v: "fridge", l: "Equipment", i: "fridge", c: "r" },
  { v: "repair", l: "Shop repair", i: "wrench", c: "r" },
  { v: "wc", l: "Working capital", i: "wallet", c: "r" },
];
const loanCalc = (amount, days) => {
  const daily = Math.ceil((amount * (1 + rateFor() / 100 * days / 30)) / days / 10) * 10;   // monthly rate from the Save Score tier, illustrative
  // Repayments come out of daily QR settlements, so check them against average daily collections (illustrative limits).
  const existing = state.loans.reduce((s, l) => s + l.daily, 0);
  const share = (daily + existing) / AVG_DAILY_SALES, pct = Math.round(share * 100);
  const base = `All repayments together would be ${pct}% of your average daily collections (${rs(AVG_DAILY_SALES)}).`;
  const fit = share <= 0.05 ? { l: "Comfortable", c: "good", t: base }
    : share <= 0.10 ? { l: "Tight", c: "warn", t: base + " A longer term makes it easier." }
    : { l: "Too high", c: "bad", t: base + " Choose a smaller amount or a longer term." };
  return { daily, fit, pctSales: Math.round(daily / AVG_DAILY_SALES * 100) };
};

const HAMPER = { price: 1200, weeks: 8, items: "Rice 5 kg, jaggery 1 kg, ghee 500 ml, cashew 100 g, moong dal 1 kg, Pongal pot" };
const NEIGHBOURS = [
  { name: "Selvi Stores", d: "300 m" }, { name: "Sri Balaji Provisions", d: "450 m" }, { name: "Anbu Mart", d: "600 m" }, { name: "Kaveri Stores", d: "750 m" },
];
const CIRCLE_ITEMS = [
  { v: "ghee", l: "Aavin ghee 1 L", price: 640, unit: "L" },
  { v: "jaggery", l: "Jaggery 25 kg bag", price: 1450, unit: "bag" },
  { v: "rice", l: "Ponni rice 25 kg", price: 1350, unit: "bag" },
];
const fundCalc = (inv) => { const joined = Math.round(inv * 0.6); const weekly = HAMPER.price / HAMPER.weeks; return { joined, weekly, total: joined * HAMPER.price }; };

const FLOWS = {
  // ---------- NEW A: Pongal Fund. Regulars pre-book a hamper by AutoPay; payments settle T+1 into the shop's partner-bank Pongal pot ----------
  fund: {
    title: "Pongal Fund",
    init: () => ({ invite: 40 }),
    steps: [
      () => ({ h: `<h2 class="j-h">Let your regulars pre-book their Pongal hamper</h2>
        <p class="j-p">Like a traditional Pongal fund, but safe and digital. Customers pay a little every week by AutoPay, and the money buys your Pongal stock.</p>
        <div class="card"><div class="eyebrow">Pongal hamper</div>${row("Price", rs(HAMPER.price))}${row("Customer pays", `${rs(HAMPER.price / HAMPER.weeks)} a week · ${HAMPER.weeks} weeks`)}${row("Contains", HAMPER.items)}${row("Delivered", "13 January, before Bhogi")}</div>` }),
      (d) => { const f = fundCalc(d.invite);
        return { h: `<h2 class="j-h">Invite your regular customers</h2>
          <p class="j-p">Kaasu found your regulars from their Paytm payments at your shop. They get an invite in their Paytm app.</p>
          ${chips("invite", [20, 40, 60].map(v => ({ v, l: v + " regulars", s: v === 40 ? "Recommended" : "" })), d.invite)}
          <div class="card">${row("Expected to join (about 60%)", f.joined + " customers")}${row("Advance by 6 January", rs(f.total), "good")}${row("Your Pongal loan need", f.total >= 11000 ? `${rs(11000)} → ₹0` : rs(Math.max(0, 11000 - f.total)), "good")}</div>
          <div class="preview-l">What Lakshmi sees in her Paytm app</div>
          <div class="bubble"><div class="from">Murugan Stores · Pongal Fund</div><div class="ta">பொங்கல் தொகுப்பு ₹1,200 · வாரம் ₹150 × 8 · 13 ஜனவரி டெலிவரி</div><div class="sub">Pongal hamper ₹1,200 · ₹150 a week by AutoPay · delivered 13 Jan · refund if not delivered</div><span class="pay">Join with AutoPay</span></div>` }; },
      () => ({ h: `<h2 class="j-h">Customers' money stays protected</h2>
        <div class="card">${row("Where the money goes", "Your Pongal pot at Paytm's partner bank, next day")}${row("What it pays for", "Your Pongal stock, paid to the distributor")}${row("If a customer cancels", "Full refund, any time")}${row("If the hamper isn't delivered", "Automatic refund")}${row("Interest or bonus", "None. It's an advance order, not a chit")}</div>
        <p class="fine">Paytm settles each payment to your partner-bank Pongal pot the next day, as RBI requires. The pot stays locked for Pongal stock, so customers trust it and you need no loan for what they pre-booked. It is an advance for goods, never a deposit with returns.</p>`, next: "Launch with PIN" }),
    ],
    pin: (d) => `To invite ${d.invite} regulars to your Pongal Fund`,
    finish(d) { const f = fundCalc(d.invite); state.fund = { joined: f.joined, total: f.total };
      done("Pongal Fund launched", `${d.invite} regulars invited. When about ${f.joined} join, ${rs(f.total)} of your Pongal stock is paid for by customers.`, row("Hamper", rs(HAMPER.price)) + row("Expected advance", rs(f.total)) + row("Held in", "Your partner-bank Pongal pot"), "Home");
      const ta = "முருகன், பொங்கல் நிதி தொடங்கியது. லக்ஷ்மி சேர்ந்தார், இந்த வாரம் ₹150."; setTimeout(() => { $("sbTop").textContent = "FUND +RS 150"; setSpeech(ta, "Pongal Fund is live. Lakshmi joined: ₹150 this week."); speak(ta, "ta"); }, 900); },
  },

  // ---------- NEW B: Buy together. Nearby Paytm shops pool festival orders to reach the distributor's bulk slab ----------
  circle: {
    title: "Buy together",
    init: () => ({ ghee: 12, jaggery: 4, rice: 6 }),
    steps: [
      () => ({ h: `<h2 class="j-h">4 shops near you are ordering Pongal stock</h2>
        <p class="j-p">Order together from Sri Murugan Agencies to reach the bulk price. Each shop pays only its own share, through Paytm.</p>
        <div class="card list">${NEIGHBOURS.map((n, i) => `<div class="z-row"><span class="z-avatar">${ICON.store}</span><span class="z-r-t"><b>${n.name}</b><small>${n.d} away · Paytm merchant</small></span><span class="u-right"><span class="sent">${i < 3 ? "Joined" : "Invited"}</span></span></div>`).join("")}</div>
        <p class="fine">Shops see only the total order, never each other's sales.</p>` }),
      (d) => { const mine = CIRCLE_ITEMS.reduce((s, it) => s + it.price * d[it.v], 0), save = Math.round(mine * 0.06);
        return { h: `<h2 class="j-h">Add your Pongal order</h2>
          ${CIRCLE_ITEMS.map(it => `<div class="eyebrow">${it.l} · ${rs(it.price)}</div>${chips(it.v, (it.v === "ghee" ? [6, 12, 24] : [2, 4, 6]).map(v => ({ v, l: v + " " + it.unit })), d[it.v])}`).join("")}
          <div class="fit good"><span class="z-ic g lg">${ICON.check}</span><div><b>Bulk price unlocked: 6% off</b><small>Together the circle orders ${rs(mine * 5)}, above the distributor's ${rs(100000)} slab. You save ${rs(save)}.</small></div></div>` }; },
      (d) => { const mine = CIRCLE_ITEMS.reduce((s, it) => s + it.price * d[it.v], 0), save = Math.round(mine * 0.06);
        return { h: `<h2 class="j-h">Review your share</h2>
          <div class="card">${CIRCLE_ITEMS.map(it => row(it.l, `${d[it.v]} × ${rs(it.price)}`)).join("")}${row("Your order", rs(mine))}${row("Circle discount (6%)", "−" + rs(save), "good")}${row("You pay", rs(mine - save))}${row("Paid from", "Your Pongal pot, on delivery")}${row("Delivery", "4 January, shared van")}</div>`, next: "Join with PIN" }; },
    ],
    pin: (d) => `To join the buying circle for ${rs(CIRCLE_ITEMS.reduce((s, it) => s + it.price * d[it.v], 0) * 0.94)}`,
    finish(d) { const mine = CIRCLE_ITEMS.reduce((s, it) => s + it.price * d[it.v], 0); state.circle = { save: Math.round(mine * 0.06) };
      done("You joined the buying circle", `Order locks when the 4th shop joins. You save ${rs(state.circle.save)}.`, row("Shops in circle", "4 of 5") + row("Your saving", rs(state.circle.save)) + row("Delivery", "4 January"), "Home"); },
  },

  // ---------- NEW C: Check a bill. AI reads the distributor bill, rules find missed trade-scheme discounts ----------
  bill: {
    title: "Check a bill",
    init: () => ({ result: null, loading: false }),
    steps: [
      (d) => ({ h: `<h2 class="j-h">Did your distributor pass on every scheme?</h2>
        <p class="j-p">Brands run offers like "buy 10, get 1 free". Some never reach the shop. Take a photo of a distributor bill and Kaasu checks it.</p>
        <label class="upload"><input type="file" accept="image/*" capture="environment" id="billFile" hidden>${ICON.camera}<b>Take or upload a bill photo</b><small>JPG or PNG</small></label>
        <button type="button" class="btn-grey" id="billSample">Use a sample bill (Sri Murugan Agencies)</button>
        ${d.loading ? `<div class="fit warn"><span class="z-ic a lg">${ICON.clock}</span><div><b>Reading the bill…</b><small>AI is reading each line item.</small></div></div>` : ""}
        ${d.error ? `<p class="fine" style="color:#d1264f">${esc(d.error)}</p>` : ""}`, block: !d.result, next: "See result" }),
      (d) => { const r = d.result;
        return { h: `<h2 class="j-h">${r.missed ? `${rs(r.missed)} of discounts missing` : "All schemes were applied"}</h2>
          <p class="j-p">${esc(r.distributor)}${r.billNo ? " · " + esc(r.billNo) : ""} · ${r.source.startsWith("gemini") ? "read by AI" : "sample result"}</p>
          <div class="card">${r.rows.map(x => row(`${esc(x.name)} <small>${x.qty} × ${rs(x.rate)} · ${x.scheme}</small>`, x.missed ? `−${rs(x.missed)}` : "OK", x.missed ? "bad" : "good")).join("")}</div>
          ${r.missed ? `<div class="preview-l">Message to the distributor</div><div class="bubble"><div class="ta">வணக்கம், பில் ${esc(r.billNo)}-ல் ${rs(r.missed)} தள்ளுபடி சேர்க்கப்படவில்லை. அடுத்த பில்லில் சரி செய்ய முடியுமா? நன்றி, முருகன் ஸ்டோர்ஸ்.</div><div class="sub">Hello, bill ${esc(r.billNo)} is missing ${rs(r.missed)} of scheme discounts. Can you adjust it in the next bill? Thanks, Murugan Stores.</div></div>` : ""}`,
          next: r.missed ? "Send claim to distributor" : "Done" }; },
    ],
    finish(d) { state.billClaim = (state.billClaim || 0) + d.result.missed;
      done(d.result.missed ? "Claim sent" : "Bill checked", d.result.missed ? `${rs(d.result.missed)} claim sent to ${d.result.distributor}. Kaasu will check the next bill for the credit.` : "Every scheme was passed on.", row("Missed discounts found", rs(d.result.missed)) + row("Total claimed so far", rs(state.billClaim)), "Home"); },
  },

  // ---------- Pongal plan (from the Home alert) ----------
  pongal: {
    title: "Pongal plan",
    steps: [
      () => { const n = numbers(); return { h: `<h2 class="j-h">Your Pongal stock needs ${rs(GOAL)}</h2>
        <p class="j-p">Kaasu looked at your Paytm collections and last year's Pongal. Here is where you stand.</p>
        <div class="card">${row("Items", SHOP.goal.items)}${row("Amount needed", rs(GOAL))}${row("Due date", "6 January 2027")}${row("You'll have at today's pace", rs(n.willHave))}${row("Short by", rs(n.shortfall), "bad")}</div>
        <p class="fine">Kaasu plans in this order: your own savings first, then money owed to you, and a loan only for what's left.</p>`, next: "Make a plan" }; },
      () => { const n = numbers(); return { h: `<h2 class="j-h">How much can you keep aside each day?</h2>
        <p class="j-p">It moves from your day's QR collections into a locked Pongal pot.</p>
        ${chips("dailySave", [400, 600, 800].map(v => ({ v, l: rs(v), s: v === rec.dailySave ? "Recommended" : v < rec.dailySave ? "Lighter" : "Faster" })), state.dailySave)}
        <div class="card">${row("Saved by 6 January", rs(n.saved))}${row("Left for home each day", rs(n.takeHome))}${row("Withdraw", "Any time, same day")}</div>` }; },
      () => ({ h: `<h2 class="j-h">Collect what customers owe</h2>
        <p class="j-p">${state.udhaar.length} customers owe you ${rs(udhaarSum())}. Paytm sends the reminder in its own name, so it never feels like you are asking.</p>
        ${toneSeg()}${preview()}
        <div class="card">${row("Customers reminded", state.udhaar.length)}${row("Expected back in 10 days", rs(udhaarExpected()))}</div>`,
        next: `Send ${state.udhaar.length} reminders`, alt: "Skip for now" }),
      () => { const n = numbers(); if (!n.loanNeeded) return { h: `<h2 class="j-h">No loan needed</h2><p class="j-p">Your savings and udhaar cover the Pongal stock.</p>` };
        return { h: `<h2 class="j-h">Cover the last ${rs(n.gapAfterOwn)}</h2>
        <p class="j-p">A planned loan now costs less than a hurried one in January. Repayment starts on 17 January, after Pongal sales.</p>
        <div class="card"><div class="eyebrow">Key facts (illustrative)</div>${kfs(n.loanNeeded, LOAN.days, n.repayDaily)}</div>${consent()}`,
        next: "Request this loan", alt: "Continue without a loan", needConsent: true }; },
      () => { const n = numbers(); const ok = n.finalShort === 0; return { h: `<h2 class="j-h">Review your plan</h2>
        <div class="card">${row(`Save ${rs(state.dailySave)} a day`, rs(n.saved))}${row("Udhaar expected back", state.collect ? rs(n.udhaar) : "Skipped")}${row("Planned loan", n.loan ? rs(n.loan) : "None")}${row("Pongal stock needed", rs(GOAL))}${row("Result", ok ? "Fully covered" : `Still short by ${rs(n.finalShort)}`, ok ? "good" : "bad")}</div>
        <p class="fine">You can also confirm by saying "haan" or pressing the button on your Soundbox.</p>`, next: "Confirm with PIN" }; },
    ],
    onNext(step, skip) {
      if (step === 2) { state.collect = !skip; if (!skip) { state.remindersSent = true; state.udhaar.forEach(u => state.reminded.add(u.name)); } }
      if (step === 3 && numbers().loanNeeded) state.loanAccepted = !skip;
    },
    pin: () => `To save ${rs(state.dailySave)} a day${numbers().loan ? ` and request a ${rs(numbers().loan)} loan` : ""}`,
    finish() { activatePongal(); },
  },

  // ---------- New savings goal ----------
  goal: {
    title: "New savings goal",
    init: () => ({ type: null, amount: 25000, months: 3 }),
    steps: [
      (d) => ({ h: `<h2 class="j-h">What are you saving for?</h2><p class="j-p">Pick one. You can have several goals.</p>${optGrid("type", GOAL_TYPES, d.type)}`, block: !d.type }),
      (d) => { const days = d.months * 30, daily = Math.ceil(d.amount / days / 10) * 10, share = daily / Math.max(1, freeDaily());
        return { h: `<h2 class="j-h">How much, and by when?</h2>
          <div class="eyebrow">Amount</div>${chips("amount", [10000, 25000, 50000].map(v => ({ v, l: rs(v) })), d.amount)}
          <div class="eyebrow">By</div>${chips("months", [1, 3, 6].map(v => ({ v, l: v === 1 ? "1 month" : v + " months" })), d.months)}
          <div class="card">${row("Auto-save each day", rs(daily))}${row("Your free cash each day", rs(freeDaily()))}${row("Kaasu check", share <= 0.6 ? "Comfortable" : "Too much, choose a later date", share <= 0.6 ? "good" : "bad")}</div>`, block: share > 0.6 }; },
      (d) => { const t = GOAL_TYPES.find(x => x.v === d.type); const days = d.months * 30, daily = Math.ceil(d.amount / days / 10) * 10;
        return { h: `<h2 class="j-h">Review your goal</h2>
          <div class="card">${row("Goal", t.l)}${row("Target", rs(d.amount))}${row("By", byDate(d.months))}${row("Auto-save", `${rs(daily)} a day at 9 pm`)}${row("From", "Your Paytm QR collections")}${row("Kept with", "Licensed partner (demo)")}${row("Withdraw", "Any time, with your PIN")}</div>`, next: "Confirm with PIN" }; },
    ],
    pin: (d) => `To auto-save ${rs(Math.ceil(d.amount / (d.months * 30) / 10) * 10)} a day for ${GOAL_TYPES.find(x => x.v === d.type).l.toLowerCase()}`,
    finish(d) {
      const t = GOAL_TYPES.find(x => x.v === d.type); const daily = Math.ceil(d.amount / (d.months * 30) / 10) * 10;
      state.goals.push({ id: "g" + Date.now(), name: t.l, icon: t.i, target: d.amount, daily, by: byDate(d.months), saved: 0 });
      done("Savings goal created", `${rs(daily)} will be saved every day at 9 pm.`, row("Goal", t.l) + row("Target", rs(d.amount)) + row("By", byDate(d.months)), "Savings");
    },
  },

  // ---------- New loan ----------
  loan: {
    title: "New loan",
    init: () => ({ purpose: null, amount: 25000, days: 90, consent: false }),
    steps: [
      (d) => ({ h: `<h2 class="j-h">What is the loan for?</h2><p class="j-p">This helps the lender and Kaasu suggest the right size.</p>${optGrid("purpose", LOAN_TYPES, d.purpose)}`, block: !d.purpose }),
      (d) => { const c = loanCalc(d.amount, d.days);
        return { h: `<h2 class="j-h">How much do you need?</h2>
          <div class="eyebrow">Amount</div>${chips("amount", [10000, 25000, 50000, 100000].map(v => ({ v, l: v >= 100000 ? "₹1 lakh" : rs(v) })), d.amount)}
          <div class="eyebrow">Repay over</div>${chips("days", [30, 60, 90].map(v => ({ v, l: v + " days" })), d.days)}
          <div class="score-line"><span class="z-ic b lg">${ICON.trend}</span><div><b>Save Score ${saveScore()} · ${rateFor()}% a month</b><small>${rateFor() < 1.5 ? `You save regularly, so you pay less than the standard 1.5%.` : `Start a savings goal to unlock a lower rate.`}</small></div></div>
          <div class="fit ${c.fit.c}"><span class="z-ic ${c.fit.c === "good" ? "g" : c.fit.c === "warn" ? "a" : "r"} lg">${c.fit.c === "good" ? ICON.check : ICON.alert}</span><div><b>Kaasu check: ${c.fit.l}</b><small>${rs(c.daily)} a day from your QR collections. ${c.fit.t}</small></div></div>`, block: c.fit.c === "bad" }; },
      (d) => { const c = loanCalc(d.amount, d.days);
        return { h: `<h2 class="j-h">Key facts</h2><p class="j-p">Please read these before you apply.</p>
          <div class="card"><div class="eyebrow">Key fact statement (illustrative)</div>${row("Purpose", LOAN_TYPES.find(x => x.v === d.purpose).l)}${row("Interest", `${rateFor()}% a month · Save Score ${saveScore()}`)}${kfs(d.amount, d.days, c.daily)}${row("Repaid from", "Daily QR settlement")}</div>${consent(d.consent)}`, needConsent: true, next: "Continue" }; },
      (d) => { const c = loanCalc(d.amount, d.days);
        return { h: `<h2 class="j-h">Review and apply</h2>
          <div class="card">${row("Loan", rs(d.amount))}${row("Daily repayment", rs(c.daily))}${row("Term", d.days + " days")}${row("Money goes to", "Your bank account")}${row("Decision by", "Lending partner")}</div>
          <p class="fine">Applying does not affect your Kaasu savings. The lender may ask for more details.</p>`, next: "Apply with PIN" }; },
    ],
    pin: (d) => `To apply for a ${rs(d.amount)} loan`,
    finish(d) {
      const c = loanCalc(d.amount, d.days); const t = LOAN_TYPES.find(x => x.v === d.purpose);
      state.loans.push({ purpose: t.l, icon: t.i, amount: d.amount, days: d.days, daily: c.daily, status: "Under review", to: "your bank account" });
      done("Loan request sent", "The lending partner will review it and reply in the app.", row("Amount", rs(d.amount)) + row("Daily repayment", rs(c.daily)) + row("Status", "Under review"), "Loans");
    },
  },

  // ---------- Add money / withdraw from a goal ----------
  add: {
    title: "Add money",
    init: (id) => ({ id, amount: 500 }),
    steps: [(d) => { const g = state.goals.find(x => x.id === d.id);
      return { h: `<h2 class="j-h">Add to ${esc(g.name)}</h2><p class="j-p">From your Paytm balance, right now.</p>${chips("amount", [200, 500, 1000, 2000].map(v => ({ v, l: rs(v) })), d.amount)}
        <div class="card">${row("Goal", esc(g.name))}${row("Saved so far", rs(g.saved))}${row("After this", rs(g.saved + d.amount))}</div>`, next: "Add with PIN" }; }],
    pin: (d) => `To add ${rs(d.amount)} to your savings`,
    finish(d) { const g = state.goals.find(x => x.id === d.id); g.saved += d.amount; done("Money added", `${rs(d.amount)} added to ${g.name}.`, row("Saved so far", rs(g.saved)) + row("Target", rs(g.target)), "Savings"); },
  },
  withdraw: {
    title: "Withdraw",
    init: (id) => ({ id, amount: 500 }),
    steps: [(d) => { const g = state.goals.find(x => x.id === d.id);
      return { h: `<h2 class="j-h">Withdraw from ${esc(g.name)}</h2><p class="j-p">It reaches your bank account today.</p>${g.saved ? chips("amount", [200, 500, 1000].filter(v => v <= g.saved).map(v => ({ v, l: rs(v) })), d.amount) : ""}
        <div class="card">${row("Available", rs(g.saved))}</div>${g.saved ? "" : `<p class="fine">Nothing saved yet. The first auto-save happens tonight at 9 pm.</p>`}`, block: !g.saved, next: "Withdraw with PIN" }; }],
    pin: (d) => `To withdraw ${rs(d.amount)} to your bank`,
    finish(d) { const g = state.goals.find(x => x.id === d.id); g.saved = Math.max(0, g.saved - d.amount); done("Withdrawal requested", `${rs(d.amount)} will reach your bank today.`, row("Left in goal", rs(g.saved)), "Savings"); },
  },

  // ---------- Udhaar: remind everyone, add new ----------
  remind: {
    title: "Remind customers",
    steps: [() => ({ h: `<h2 class="j-h">Remind ${state.udhaar.length} customers</h2><p class="j-p">Paytm sends each reminder in its own name, when that customer usually has money. Each customer sees only their own amount.</p>
      <div class="card"><div class="eyebrow">Smart timing</div>${state.udhaar.map(u => row(`${esc(u.name)} <small>${paydayWhy(u)}</small>`, payday(u))).join("")}</div>${toneSeg()}${preview()}
      <div class="card">${row("Total owed", rs(udhaarSum()))}${row("Expected back in 10 days", rs(udhaarExpected()))}</div>`, next: "Schedule reminders" })],
    finish() { state.remindersSent = true; state.udhaar.forEach(u => state.reminded.add(u.name)); done("Reminders scheduled", "Paytm sends each customer a reminder in their pay week, in Paytm's name, with a one-tap Pay button.", row("Customers", state.udhaar.length) + row("Expected back", rs(udhaarExpected())), "Udhaar"); },
  },
  udhaar: {
    title: "Add udhaar",
    init: () => ({ name: "Kumar", amount: 200 }),
    steps: [(d) => ({ h: `<h2 class="j-h">Who took items on credit?</h2>
      <div class="eyebrow">Customer</div>${chips("name", ["Kumar", "Priya", "Arjun"].map(v => ({ v, l: v })), d.name)}
      <div class="eyebrow">Amount</div>${chips("amount", [100, 200, 500].map(v => ({ v, l: rs(v) })), d.amount)}
      <p class="fine">Tip: at closing time just tell your Soundbox, "Kumar 200 udhaar".</p>`, next: "Continue" }),
      (d) => ({ h: `<h2 class="j-h">${esc(d.name)} confirms it in Paytm</h2>
        <p class="j-p">Both of you agree on the same amount, so there are no arguments later. Every confirmed entry builds ${esc(d.name)}'s Bharosa trail.</p>
        <div class="preview-l">What ${esc(d.name)} sees</div>
        <div class="bubble paytm"><div class="from"><img src="/brand/paytm-logo.svg" alt="Paytm" style="height:13px;vertical-align:-2px"> · Confirm udhaar</div><div>Murugan Stores added <b>${rs(d.amount)}</b> to your udhaar today.</div><div class="sub">Is this right? Confirmed udhaar helps you get credit later.</div><span class="pay">Yes, confirm</span> <span class="pay ghost">Not mine</span></div>`, next: "Save and send for confirmation" })],
    finish(d) { state.udhaar.push({ name: d.name, amount: d.amount, days: 0, usual: "new" });
      done("Udhaar saved", `${d.name} owes you ${rs(d.amount)}. Paytm asked ${d.name} to confirm.`, row("Total owed to you", rs(udhaarSum())) + row("Status", "Waiting for confirmation"), "Udhaar");
      setTimeout(() => { state.confirmed.add(d.name); renderPanes(); toast(`${d.name} confirmed ${rs(d.amount)} in Paytm ✓`); }, 2200); },
  },
};
const UNPAID = ["Ravi", "Karthik", "Anand"];
const missCalc = () => {
  const unpaid = state.udhaar.filter(u => UNPAID.includes(u.name)), paid = state.udhaar.filter(u => !UNPAID.includes(u.name) && u.days);
  const got = paid.reduce((s, u) => s + u.amount, 0), expected = udhaarExpected(), gap = Math.max(0, expected - got);
  const daysLeft = 37, extraDaily = Math.ceil(gap / daysLeft / 10) * 10;
  return { unpaid, paid, got, expected, gap, extraDaily, owed: unpaid.reduce((s, u) => s + u.amount, 0) };
};
FLOWS.miss = {
  title: "Udhaar not repaid",
  init: () => ({ fix: null }),
  steps: [
    () => { const m = missCalc();
      return { h: `<h2 class="j-h">${m.unpaid.length} customers haven't paid yet</h2>
        <p class="j-p">Paytm's reminders went out in their pay week. ${m.paid.length} customers paid; ${m.unpaid.length} did not. Here is what it means for Pongal.</p>
        <div class="card list">${m.unpaid.map(u => `<div class="z-row"><span class="z-avatar out">${ICON.user}</span><span class="z-r-t"><b>${esc(u.name)}</b><small>${u.days + 10} days unpaid · ${paydayWhy(u)}</small></span><span class="u-right"><b>${rs(u.amount)}</b></span></div>`).join("")}</div>
        <div class="card">${row("Udhaar the plan expected", rs(m.expected))}${row("Collected so far", rs(m.got))}${row("Pongal plan now short by", rs(m.gap), "bad")}</div>
        <p class="fine">Your Pongal stock is still safe. Pick how Kaasu should cover the ${rs(m.gap)}.</p>`, next: "Choose a fix" }; },
    (d) => { const m = missCalc();
      const opts = [
        { v: "save", l: `Save ${rs(m.extraDaily)} more a day`, i: "piggy", s: `${rs(state.dailySave + m.extraDaily)} a day until 6 Jan. No new loan.` },
        { v: "loan", l: `Add ${rs(Math.ceil(m.gap / 1000) * 1000)} to the Pongal loan`, i: "landmark", c: "r", s: "Keeps today's saving the same. Lender decides." },
      ];
      if (state.fund) opts.unshift({ v: "fund", l: "Use the Pongal Fund advance", i: "gift", c: "a", s: `Customers' pre-bookings already cover ${rs(state.fund.total)}.` });
      return { h: `<h2 class="j-h">How should Kaasu cover ${rs(m.gap)}?</h2>${optGrid("fix", opts, d.fix)}
        <div class="card">${row("Second reminder", "From Paytm, next pay week")}${row("New udhaar for them", "Pause suggested")}</div>`, block: !d.fix, next: "Continue" }; },
    (d) => { const m = missCalc();
      const what = d.fix === "save" ? `Save ${rs(state.dailySave + m.extraDaily)} a day` : d.fix === "loan" ? `Pongal loan +${rs(Math.ceil(m.gap / 1000) * 1000)}` : "Pongal Fund covers it";
      return { h: `<h2 class="j-h">Back on track</h2><div class="card">${row("Shortfall from unpaid udhaar", rs(m.gap))}${row("Fix", what)}${row("Second reminder", "From Paytm, next pay week")}${row("Pongal stock", "Covered", "good")}</div>`, next: d.fix === "fund" ? "Confirm" : "Confirm with PIN" }; },
  ],
  pin: (d) => (d.fix === "fund" ? null : d.fix === "save" ? `To save ${rs(missCalc().extraDaily)} more a day for Pongal` : `To add ${rs(Math.ceil(missCalc().gap / 1000) * 1000)} to your Pongal loan request`),
  finish(d) { const m = missCalc();
    if (d.fix === "save") { state.dailySave += m.extraDaily; const g = state.goals.find(x => x.id === "pongal"); if (g) { g.daily = state.dailySave; g.target = state.dailySave * DAYS; } }
    if (d.fix === "loan") { const l = state.loans.find(x => x.pongal); const add = Math.ceil(m.gap / 1000) * 1000; if (l) l.amount += add; else state.loans.unshift({ pongal: true, purpose: "Pongal stock", icon: "box", amount: add, days: 60, daily: Math.ceil(add * 1.03 / 60 / 10) * 10, status: "Under review", to: "the Pongal pot on 16 Dec" }); }
    state.udhaarMiss = { fix: d.fix, gap: m.gap };
    done("Pongal plan back on track", `${rs(m.gap)} of unpaid udhaar is covered. Paytm will remind ${m.unpaid.map(u => u.name).join(", ")} once more.`, row("Fix", d.fix === "save" ? `+${rs(m.extraDaily)} a day saving` : d.fix === "loan" ? "Added to Pongal loan" : "Pongal Fund advance") + row("Pongal stock", "Covered"), "Udhaar"); },
};
// ===== NEW: Bharosa. Confirmed udhaar becomes a credit trail; Paytm Postpaid's partner pays the shop =====
const bharosaList = () => state.udhaar.filter(u => state.confirmed.has(u.name) && !UNPAID.includes(u.name) && !u.bharosa && u.days);
const TRAIL = { Lakshmi: [14, 14], Selvi: [9, 9], Fathima: [11, 10], Anand: [6, 4] };
FLOWS.bharosa = {
  title: "Bharosa",
  init: () => ({}),
  steps: [
    () => { const L = bharosaList(), tot = L.reduce((s, u) => s + u.amount, 0);
      return { h: `<h2 class="j-h">Get paid today for ${rs(tot)} of udhaar</h2>
        <p class="j-p">These customers confirmed every udhaar in their Paytm app and always paid you back. Paytm's lending partner can pay you now.</p>
        <div class="card list">${L.map(u => { const [c, p] = TRAIL[u.name] || [5, 5]; return `<div class="z-row"><span class="z-avatar">${ICON.user}</span><span class="z-r-t"><b>${esc(u.name)}</b><small>Bharosa trail: ${c} confirmed · ${p} repaid on time</small></span><span class="u-right"><b>${rs(u.amount)}</b><span class="sent">Trusted</span></span></div>`; }).join("")}</div>
        <p class="fine">Customers with unconfirmed or late udhaar stay with you as normal.</p>`, block: !L.length, next: "How it works" }; },
    () => { const L = bharosaList(), u = L[0] || { name: "Lakshmi", amount: 1240 };
      return { h: `<h2 class="j-h">Fair for you and your customers</h2>
        <div class="card">${row("Who pays you now", "Paytm Postpaid's lending partner")}${row("Customer repays", "The lender, in 30 days, no interest")}${row("Customer agrees", "In their Paytm app, with key facts")}${row("Your role", "You vouch. You don't guarantee.")}${row("If a customer says no", "The udhaar stays with you")}</div>
        <div class="preview-l">What ${esc(u.name)} sees</div>
        <div class="bubble paytm"><div class="from"><img src="/brand/paytm-logo.svg" alt="Paytm" style="height:13px;vertical-align:-2px"> Postpaid</div><div>Move your Murugan Stores udhaar of <b>${rs(u.amount)}</b> to Paytm Postpaid?</div><div class="sub">Repay by 15 Dec · no interest · key facts inside</div><span class="pay">Review and accept</span></div>` }; },
    () => { const L = bharosaList(), tot = L.reduce((s, u) => s + u.amount, 0), fee = Math.round(tot * 0.02);
      return { h: `<h2 class="j-h">Review</h2><div class="card">${row("Customers", L.length)}${row("Udhaar moved", rs(tot))}${row("Partner fee (illustrative 2%)", "−" + rs(fee))}${row("You receive", rs(tot - fee), "good")}${row("When", "As each customer accepts")}</div>`, next: "Send with PIN" }; },
  ],
  pin: () => "To send Bharosa requests to your trusted customers",
  finish() { const L = bharosaList(), tot = L.reduce((s, u) => s + u.amount, 0), fee = Math.round(tot * 0.02);
    state.bharosa = { paid: 0, total: tot - fee };
    done("Bharosa requests sent", "When each customer accepts in their Paytm app, the lending partner pays you.", row("Customers asked", L.length) + row("You'll receive", rs(tot - fee)), "Udhaar");
    L.forEach((u, k) => setTimeout(() => { u.bharosa = true; state.bharosa.paid += Math.round(u.amount * 0.98);
      $("sbTop").textContent = `RS ${Math.round(u.amount * 0.98)} RECEIVED`; renderPanes(); toast(`${u.name} accepted · ${rs(Math.round(u.amount * 0.98))} paid to you`); }, 1800 + k * 1500)); },
};

// ===== NEW: Staff Saathi. Helper wage advance from the shop's own Kaasu, recovered on payday =====
const HELPER = { name: "Ravi Kumar", salary: 9000, daysWorked: 15 };
FLOWS.staff = {
  title: "Staff advance",
  init: () => { setTimeout(() => { $("sbTop").textContent = "ADVANCE REQUEST"; setSpeech("ரவி ₹1,500 முன்பணம் கேட்கிறார். போனில் பாருங்கள்.", "Ravi is asking for a ₹1,500 advance. Check your phone."); }, 200); return { amount: 1500 }; },
  steps: [
    () => { const earned = HELPER.salary / 30 * HELPER.daysWorked;
      return { h: `<h2 class="j-h">Ravi asked for an advance</h2>
        <p class="j-p">Ravi said "₹1,500 advance" to the Soundbox. He has earned it already this month.</p>
        <div class="card">${row("Helper", HELPER.name)}${row("Monthly salary", rs(HELPER.salary))}${row(`Earned so far (${HELPER.daysWorked} days)`, rs(earned))}${row("Can advance up to (50%)", rs(earned / 2), "good")}${row("Advances this month", "₹0")}</div>` }; },
    (d) => ({ h: `<h2 class="j-h">How much should Ravi get?</h2>
      ${chips("amount", [500, 1000, 1500, 2000].map(v => ({ v, l: rs(v) })), d.amount)}
      <div class="card">${row("Paid from", "Your Kaasu savings · no interest")}${row("Ravi gets it", "On his UPI, in seconds")}${row("Recovered", "From his 1 Dec salary")}${row("Ravi's 1 Dec salary", rs(HELPER.salary - d.amount))}</div>
      <p class="fine">Deductions stay within the Code on Wages limit (50% of wages), with Ravi's consent recorded in Paytm.</p>` }),
    (d) => ({ h: `<h2 class="j-h">Review</h2><div class="card">${row("To", HELPER.name)}${row("Advance", rs(d.amount))}${row("From", "Kaasu savings")}${row("Recovered on", "1 December")}</div>`, next: "Pay with PIN" }),
  ],
  pin: (d) => `To pay Ravi a ${rs(d.amount)} advance`,
  finish(d) { state.staff = { name: "Ravi", amount: d.amount };
    done("Advance paid", `${rs(d.amount)} sent to Ravi's UPI. It will be recovered from his 1 Dec salary.`, row("Ravi's earned balance", rs(HELPER.salary / 2 - d.amount)) + row("Next salary", rs(HELPER.salary - d.amount)), "Home");
    const ta = `ரவிக்கு ${inr(d.amount)} முன்பணம் அனுப்பப்பட்டது.`; setSpeech(ta, `Advance of ${inr(d.amount)} sent to Ravi.`); $("sbTop").textContent = "ADVANCE PAID"; },
};

// ===== NEW: Galla check. Spoken cash count vs expected cash; patterns, never accusations =====
const EXPECTED_CASH = 3260;
FLOWS.galla = {
  title: "Galla check",
  init: () => { setTimeout(() => { $("sbTop").textContent = "COUNT YOUR CASH"; setSpeech("முருகன், கடை மூடும் நேரம். கல்லாவில் எவ்வளவு பணம் இருக்கிறது?", "Murugan, closing time. How much cash is in the galla?"); }, 200); return { counted: null }; },
  steps: [
    (d) => ({ h: `<h2 class="j-h">Closing time. Count the galla.</h2>
      <p class="j-p">Say the amount to your Soundbox. Kaasu compares it with what should be there.</p>
      <div class="mic-big">${ICON.mic}</div>
      <div class="eyebrow">What Murugan said (demo)</div>${chips("counted", [3240, 3050].map(v => ({ v, l: rs(v) })), d.counted)}`, block: d.counted == null, next: "Check" }),
    (d) => { const diff = d.counted - EXPECTED_CASH, ok = Math.abs(diff) <= 60;
      return { h: `<h2 class="j-h">${ok ? "Galla matches" : `${rs(Math.abs(diff))} ${diff < 0 ? "less" : "more"} than expected`}</h2>
        <div class="card">${row("Today's sales", "₹11,240")}${row("Paid by UPI (71%)", "₹7,980")}${row("Cash expected", rs(EXPECTED_CASH))}${row("Cash counted", rs(d.counted))}${row("Difference", (diff < 0 ? "−" : "+") + rs(Math.abs(diff)), ok ? "good" : "bad")}</div>
        ${ok ? `<div class="fit good"><span class="z-ic g lg">${ICON.check}</span><div><b>All good</b><small>A small difference like this is normal change-giving.</small></div></div>`
        : `<div class="fit warn"><span class="z-ic a lg">${ICON.alert}</span><div><b>Usual reasons</b><small>Udhaar given but not logged · loose items sold without counting · wrong change. Want to log udhaar now?</small></div></div>
           <div class="card">${row("Last 14 days", "Short 3 times")}${row("When", "All between 6 and 9 pm")}${row("Suggestion", "Count the galla at the 6 pm handover too")}</div>`}
        <p class="fine">Kaasu shows patterns, never blames a person. Your helpers' data stays private.</p>`, next: "Save today's count" }; },
  ],
  finish(d) { const diff = d.counted - EXPECTED_CASH; state.galla = { label: Math.abs(diff) <= 60 ? "Today matched ✓" : `${rs(Math.abs(diff))} short today` };
    done("Day closed", state.galla.label === "Today matched ✓" ? "Cash matched. See you tomorrow, Murugan." : "Saved. Kaasu will watch the evening pattern.", row("Counted", rs(d.counted)) + row("Expected", rs(EXPECTED_CASH)), "Home"); $("sbTop").textContent = "DAY CLOSED"; },
};
const byDate = (m) => ({ 1: "14 December", 3: "14 February", 6: "14 May" }[m]);
const consent = (on) => `<label class="check"><input type="checkbox" id="consent" ${on ?? state.kfsRead ? "checked" : ""}> <span>I have read the key facts. I understand the lending partner makes the final decision.</span></label>`;
const TONES = {
  gentle: { t: "Gentle", d: "A polite note with no deadline. Best for regulars who are a little late." },
  friendly: { t: "Festive", d: "A warm Pongal greeting with a one-tap Pay button. Best just before a festival." },
};
const toneSeg = () => `<div class="eyebrow">Reminder style</div><div class="opts" role="radiogroup" aria-label="Reminder style">${Object.entries(TONES).map(([k, v]) => `<button type="button" role="radio" aria-checked="${state.tone === k}" class="opt tone-opt ${state.tone === k ? "on" : ""}" data-tone="${k}"><span class="radio" aria-hidden="true"></span><b>${v.t}</b><small>${v.d}</small></button>`).join("")}</div>`;
function preview() {
  const l = state.udhaar[0];
  const body = state.tone === "gentle"
    ? `<div class="ta">Paytm நினைவூட்டல்: முருகன் ஸ்டோர்ஸ்-ல் ${rs(l.amount)} நிலுவை உள்ளது. வசதியான போது ஒரு தட்டில் செலுத்தலாம்.</div><div class="sub">Paytm reminder: ${rs(l.amount)} is pending at Murugan Stores. Pay whenever convenient, in one tap.</div>`
    : `<div class="ta">பொங்கல் வருகிறது! முருகன் ஸ்டோர்ஸ் கணக்கில் ${rs(l.amount)} நிலுவை. ஒரு தட்டில் செலுத்தி பண்டிகையை சுலபமாக்குங்கள்.</div><div class="sub">Pongal is coming! Your Murugan Stores balance is ${rs(l.amount)}. Clear it in one tap.</div>`;
  return `<div class="preview-l">What ${l.name} sees: a reminder from Paytm, not from the shop</div><div class="bubble paytm"><div class="from"><img src="/brand/paytm-logo.svg" alt="Paytm" style="height:13px;vertical-align:-2px"> · Payment reminder</div>${body}<span class="pay">Pay ${rs(l.amount)}</span></div>`;
}

function startFlow(id, arg) {
  const f = FLOWS[id];
  state.flow = { id, step: 0, data: f.init ? f.init(arg) : {} };
  if (id === "pongal" && state.active) state.flow.step = f.steps.length - 1;
  renderFlow(); showScreen("scrJourney");
}
function renderFlow() {
  const fl = state.flow, f = FLOWS[fl.id], total = f.steps.length;
  const v = f.steps[fl.step](fl.data);
  $("jTitle").textContent = f.title;
  $("jStep").textContent = total > 1 ? `Step ${fl.step + 1} of ${total}` : "";
  $("jBar").style.width = ((fl.step + 1) / total * 100) + "%";
  $("jBack").style.visibility = fl.step > 0 ? "visible" : "hidden";
  const key = fl.id + ":" + fl.step;
  $("jBody").innerHTML = v.h;
  if (renderFlow.last !== key) { $("jBody").scrollTop = 0; animate($("jBody"), (renderFlow.dir || 1) > 0 ? "step-fwd" : "step-back", 420); }
  renderFlow.last = key; renderFlow.dir = 1;
  const consentOn = fl.id === "pongal" ? state.kfsRead : fl.data.consent;
  $("jNext").textContent = v.next || "Continue";
  $("jNext").disabled = !!v.block || (v.needConsent && !consentOn);
  $("jAlt").hidden = !v.alt; $("jAlt").textContent = v.alt || "";
}
function flowNext(skip) {
  const fl = state.flow, f = FLOWS[fl.id];
  if (f.onNext) f.onNext(fl.step, skip);
  if (fl.step < f.steps.length - 1) { fl.step++; return renderFlow(); }
  const pinText = f.pin ? f.pin(fl.data) : null;
  if (pinText) requirePin(pinText, () => f.finish(fl.data)); else f.finish(fl.data);
}
function done(title, text, summary, tab) {
  $("doneH").textContent = title; $("doneP").textContent = text; $("doneSummary").innerHTML = summary;
  state.tab = tab || state.tab; renderPanes(); showScreen("scrDone");
}

// ---------------- Pongal activation ----------------
const CONFIRM = {
  ta: (n) => `சரி முருகன்! தினமும் ${inr(n)} பொங்கல் உண்டியலில் சேர்க்கிறேன். பொங்கல் சரக்குக்கு பணம் தயார்.`,
  en: (n) => `Done, Murugan. I'll keep ${inr(n)} aside every day in the Pongal pot. Your Pongal stock is planned.`,
};
function activatePongal() {
  const n = numbers();
  state.active = true;
  state.goals = state.goals.filter(g => g.id !== "pongal");
  state.goals.unshift({ id: "pongal", name: "Pongal stock", icon: "box", target: n.saved, daily: state.dailySave, by: "6 January", saved: 0 });
  state.loans = state.loans.filter(l => !l.pongal);
  if (state.loanAccepted && n.loanNeeded) { state.loanRequested = true; state.loans.unshift({ pongal: true, purpose: "Pongal stock", icon: "box", amount: n.loan, days: LOAN.days, daily: n.repayDaily, status: "Under review", to: "the Pongal pot on 16 Dec" }); }
  $("sbTop").textContent = "PONGAL PLAN ON";
  state.tab = "Home";
  done("Your Pongal plan is active", n.finalShort === 0 ? "Pongal stock of ₹80,000 is fully covered." : `Still short by ${rs(n.finalShort)}. Kaasu will keep watching.`,
    row("Daily saving", rs(state.dailySave)) + row("Udhaar reminders", state.remindersSent ? "Sent" : "Not sent") + row("Loan request", state.loanRequested ? rs(n.loan) + " · lender decides" : "None"), "Home");
  const t = CONFIRM[state.lang](state.dailySave);
  setSpeech(t, state.lang === "ta" ? CONFIRM.en(state.dailySave) : ""); speak(t, state.lang);
}
function approveFromSoundbox() {
  if (state.active) return toast("Your Pongal plan is already active");
  state.collect = true; state.remindersSent = true; state.udhaar.forEach(u => state.reminded.add(u.name));
  state.loanAccepted = numbers().loanNeeded > 0; state.kfsRead = true;
  if ($("scrMain").hidden && $("scrJourney").hidden) { showScreen("scrMain"); showTab("Home"); }
  setSpeech(T("உங்கள் போனில் PIN போட்டு உறுதி செய்யுங்கள்.", "Please confirm with your PIN on your phone."), state.lang === "ta" ? "Please confirm with your PIN on your phone." : "");
  requirePin(FLOWS.pongal.pin(), activatePongal);
}

// ---------------- PIN: nothing moves without it ----------------
let pin = "", pinDone = null;
function requirePin(what, cb) { pin = ""; pinDone = cb; $("pinWhat").textContent = what; drawPin(); openSheet("pinSheet"); }
function drawPin() { document.querySelectorAll(".pin-dots i").forEach((d, i) => d.classList.toggle("f", i < pin.length)); }
$("keypad").addEventListener("click", (e) => {
  const b = e.target.closest("button"); if (!b) return;
  if (b.dataset.k === "cancel") { closeSheet("pinSheet"); pinDone = null; return toast("Cancelled. Nothing was changed."); }
  if (b.dataset.k === "del") pin = pin.slice(0, -1); else if (pin.length < 4) pin += b.textContent;
  drawPin();
  if (pin.length === 4) setTimeout(() => { closeSheet("pinSheet"); const cb = pinDone; pinDone = null; cb && cb(); }, 250);
});

// ---------------- brief + Soundbox ----------------
function localBrief() {
  const n = numbers();
  return { source: "engine",
    spoken_ta: `காலை வணக்கம் முருகன். ஜனவரி 6 அன்று பொங்கல் சரக்குக்கு ${inr(GOAL)} தேவை. இப்படியே போனால் ${inr(n.shortfall)} குறையும். தினமும் ${inr(state.dailySave)} சேமித்து, கடன் வசூல் செய்தால், பெரும்பகுதி சரியாகிவிடும். தொடங்கட்டுமா? "ஆம்" என்று சொல்லுங்கள்.`,
    spoken_en: `Good morning Murugan. Pongal stock of ${inr(GOAL)} is due on 6 January. At this pace you will be short by ${inr(n.shortfall)}. Keep ${inr(state.dailySave)} aside every day and collect your udhaar, and most of it is covered. Shall I start? Say haan.` };
}
function setSpeech(main, sub) { $("sbText").textContent = main; $("sbText").classList.toggle("ta", /[஀-௿]/.test(main)); $("sbTextEn").textContent = sub || ""; }
function showBrief() {
  if (state.active) return setSpeech(CONFIRM[state.lang](state.dailySave), state.lang === "ta" ? CONFIRM.en(state.dailySave) : "");
  const b = state.brief || localBrief();
  setSpeech(state.lang === "ta" ? b.spoken_ta : b.spoken_en, state.lang === "ta" ? b.spoken_en : "");
}
async function loadBrief() {
  state.brief = localBrief(); showBrief();
  try { const r = await fetch("/api/brief", { method: "POST", body: JSON.stringify({ dailySave: state.dailySave }) }); const b = await r.json();
    if (b.source !== "offline") { state.brief = b; showBrief(); warmVoice(); } } catch { /* keep local */ }
}
let currentAudio = null;
function setWave(mode) { $("sbWave").className = "sb-wave" + (mode ? " " + mode : ""); }
let muted = false;
function stopVoice() {
  if (currentAudio) { currentAudio.pause(); currentAudio = null; }
  if ("speechSynthesis" in window) speechSynthesis.cancel();
  setWave("");
}
// Voice: audio is fetched ahead and kept ready, so playback starts the moment the merchant taps.
const voiceCache = new Map();               // text -> Promise<object URL | null>
function getVoice(text) {
  if (!text) return Promise.resolve(null);
  if (!voiceCache.has(text)) voiceCache.set(text, fetch("/api/tts", { method: "POST", body: JSON.stringify({ text }) })
    .then(r => (r.ok ? r.blob() : null)).then(b => (b && b.size > 1000 ? URL.createObjectURL(b) : null)).catch(() => null));
  return voiceCache.get(text);
}
let pendingAudio = null;
document.addEventListener("pointerdown", () => { if (pendingAudio) { const a = pendingAudio; pendingAudio = null; a.play().catch(() => {}); } }, true);
async function speak(text, lang) {
  stopVoice();
  if (muted) return;                       // Voice switched off: show text only
  setWave("live");
  const url = await getVoice(text);
  if (url) {
    currentAudio = new Audio(url); currentAudio.onended = () => setWave("");
    try { await currentAudio.play(); return; }
    catch (e) { if (e && e.name === "NotAllowedError") { pendingAudio = currentAudio; toast("Tap anywhere to hear the Soundbox"); return; } }
  }
  if ("speechSynthesis" in window) { const u = new SpeechSynthesisUtterance(text); u.lang = lang === "ta" ? "ta-IN" : "en-IN";
    const v = speechSynthesis.getVoices().find(v => v.lang.startsWith(u.lang.slice(0, 2))); if (v) u.voice = v; u.onend = () => setWave(""); speechSynthesis.speak(u); } else setWave("");
}
function warmVoice() { const b = state.brief; if (!b) return; [b.spoken_ta, b.spoken_en].forEach(getVoice); }
const YES = /(haan|han|haa|ஆம்|ஆமா|சரி|sari|aam|yes|ok|okay|हाँ|हां)/i;
function listen(onText, lang) {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) { toast("Voice input isn't available in this browser."); return false; }
  const r = new SR(); r.lang = lang === "ta" ? "ta-IN" : "en-IN"; r.interimResults = false;
  r.onresult = (e) => onText(e.results[0][0].transcript); r.onerror = () => onText(null); r.start(); return r;
}
let lastHaan = 0;
function sayHaan() {
  if (Date.now() - lastHaan < 600) return approveFromSoundbox();
  lastHaan = Date.now(); setWave("listen"); $("sbHint").textContent = "Listening…";
  const ok = listen((t) => { setWave("");
    if (!t) { $("sbHint").textContent = "Couldn't hear you. Double-press to approve."; return; }
    $("sbHint").textContent = `Heard: "${t}"`; if (YES.test(t)) approveFromSoundbox(); else toast("Didn't catch a yes. Try again."); }, state.lang);
  if (!ok) setWave("");
}
function pressButton() {
  const b = $("pressBtn"); b.classList.add("pressed"); setTimeout(() => b.classList.remove("pressed"), 220);
  $("sbTop").textContent = "BUTTON: YES"; $("sbHint").textContent = "Button pressed. Confirm with your PIN on the phone.";
  approveFromSoundbox();
}

// ---------------- voice agent ----------------
function addMsg(text, who, src) {
  const d = document.createElement("div"); d.className = "msg " + who + (/[஀-௿]/.test(text) ? " ta" : ""); d.textContent = text;
  if (src) { const s = document.createElement("span"); s.className = "src"; s.textContent = src; d.appendChild(s); }
  $("convo").appendChild(d); $("convo").scrollTop = 1e6; return d;
}
async function ask(q) {
  q = (q || "").trim(); if (!q) return; addMsg(q, "me"); const wait = addMsg("Thinking…", "bot");
  try { const r = await fetch("/api/ask", { method: "POST", body: JSON.stringify({ question: q, plan: { dailySave: state.dailySave } }) }); const a = await r.json();
    wait.remove(); addMsg(a.answer, "bot", a.source.startsWith("gemini") ? "AI answer · from your payments" : "Offline answer"); speak(a.answer, /[஀-௿]/.test(a.answer) ? "ta" : "en");
  } catch { wait.textContent = "Couldn't reach Kaasu. Try again."; }
}

// ---------------- misc ----------------
let tt; function toast(t) { const el = $("toast"); el.textContent = t; el.hidden = false; clearTimeout(tt); tt = setTimeout(() => (el.hidden = true), 3200); }
(function drawQR() {
  let seed = 7; const rnd = () => ((seed = (seed * 9301 + 49297) % 233280) / 233280);
  const N = 23, c = 90 / N, on = new Set();
  const finder = (x, y) => { for (let i = 0; i < 7; i++) for (let j = 0; j < 7; j++) if (i === 0 || i === 6 || j === 0 || j === 6 || (i > 1 && i < 5 && j > 1 && j < 5)) on.add((x + i) + "," + (y + j)); };
  finder(0, 0); finder(N - 7, 0); finder(0, N - 7);
  const res = (i, j) => (i < 8 && j < 8) || (i > N - 9 && j < 8) || (i < 8 && j > N - 9);
  for (let i = 0; i < N; i++) for (let j = 0; j < N; j++) if (!res(i, j) && rnd() < .47) on.add(i + "," + j);
  $("qrGroup2").innerHTML = $("qrGroup").innerHTML = [...on].map(k => { const [i, j] = k.split(",").map(Number); return `<rect x="${(i * c).toFixed(2)}" y="${(j * c).toFixed(2)}" width="${c.toFixed(2)}" height="${c.toFixed(2)}" fill="#0a0a0f"/>`; }).join("");
})();

// ---------------- wire up ----------------
const WELCOME = { en: "Your shop's cash, planned for you. Every day, every festival.", ta: "உங்கள் கடையின் பணம், உங்களுக்காக திட்டமிடப்பட்டது." };
function setLang(l) {
  state.lang = l;
  document.querySelectorAll(".sb-controls .seg button").forEach(x => x.classList.toggle("on", x.dataset.lang === l));
  $("welcomeH").textContent = WELCOME[l]; $("welcomeH").classList.toggle("ta", l === "ta"); showBrief();
}
document.querySelectorAll("[data-pick]").forEach(b => b.addEventListener("click", () => {
  const p = b.dataset.pick; setLang(p === "ta" ? "ta" : "en");
  if (p !== "ta" && p !== "en") toast("Demo voice is in Tamil and English. More languages coming.");
  showScreen("scrWelcome");
}));
$("getStarted").addEventListener("click", () => { showScreen("scrMain"); showTab("Home"); });
$("haveAccount").addEventListener("click", () => { showScreen("scrMain"); showTab("Home"); });
document.querySelectorAll(".tab[data-tab]").forEach(b => b.addEventListener("click", () => showTab(b.dataset.tab)));
$("voiceTab").addEventListener("click", () => openSheet("voiceSheet"));
$("closeVoice").addEventListener("click", () => closeSheet("voiceSheet"));
$("scrim").addEventListener("click", () => { closeSheet("voiceSheet"); closeSheet("qrSheet"); });
$("closeQr").addEventListener("click", () => closeSheet("qrSheet"));
$("scrMain").addEventListener("click", (e) => {
  const tx = e.target.closest("[data-tx]"); if (tx) { state.txFilter = tx.dataset.tx; renderHome(); return; }
  const rm = e.target.closest("[data-remind]");
  if (rm) { const u = state.udhaar[Number(rm.dataset.remind)]; state.reminded.add(u.name); renderUdhaar(); return toast(`Reminder for ${u.name} scheduled for ${payday(u)}, when ${paydayWhy(u)}`); }
  const go = e.target.closest("[data-go]")?.dataset.go; if (!go) return;
  if (go === "pongal") return startFlow("pongal");
  if (go.startsWith("svc:")) return toast(`${go.slice(4)}: existing Paytm for Business feature`);
  if (go === "rain") return rainEvent();
  if (go === "qr") return openSheet("qrSheet");
  if (go === "alerts") return toast(state.active ? "Pongal plan on track. Next auto-save tonight at 9 pm." : "1 alert: Pongal stock is short by ₹32,520.");
  if (go.startsWith("tab:")) return showTab(go.slice(4));
  if (go.startsWith("flow:")) { const [, id, arg] = go.split(":"); return startFlow(id, arg); }
});
$("jNext").addEventListener("click", () => flowNext(false));
$("jAlt").addEventListener("click", () => flowNext(true));
$("jBack").addEventListener("click", () => { state.flow.step = Math.max(0, state.flow.step - 1); renderFlow.dir = -1; renderFlow(); });
$("jClose").addEventListener("click", backToMain);
async function runBill(payload) {
  const d = state.flow.data; d.loading = true; d.error = null; renderFlow();
  try { const r = await (await fetch("/api/bill", { method: "POST", body: JSON.stringify(payload) })).json();
    d.loading = false; if (!r.ok) { d.error = r.error; return renderFlow(); } d.result = r; state.flow.step = 1; renderFlow();
  } catch { d.loading = false; d.error = "Couldn't reach Kaasu. Try again."; renderFlow(); }
}
$("jBody").addEventListener("change", (e) => {
  if (e.target.id !== "billFile" || !e.target.files[0]) return;
  const fr = new FileReader(); fr.onload = () => runBill({ image: fr.result }); fr.readAsDataURL(e.target.files[0]);
});
$("jBody").addEventListener("click", (e) => {
  if (e.target.closest("#billSample")) return runBill({ sample: true });
  const s = e.target.closest("[data-set]");
  if (s) {
    const key = s.dataset.set, raw = s.dataset.val, val = isNaN(Number(raw)) ? raw : Number(raw);
    if (state.flow.id === "pongal" && key === "dailySave") { state.dailySave = val; loadBrief(); } else state.flow.data[key] = val;
    return renderFlow();
  }
  const t = e.target.closest("[data-tone]"); if (t) { state.tone = t.dataset.tone; renderFlow(); }
});
$("jBody").addEventListener("change", (e) => {
  if (e.target.id !== "consent") return;
  if (state.flow.id === "pongal") state.kfsRead = e.target.checked; else state.flow.data.consent = e.target.checked;
  renderFlow();
});
$("doneHome").addEventListener("click", backToMain);

document.querySelectorAll(".sb-controls .seg button").forEach(b => b.addEventListener("click", () => setLang(b.dataset.lang)));
$("playBrief").addEventListener("click", () => { showBrief(); speak($("sbText").textContent, state.lang); });
$("sayHaan").addEventListener("click", sayHaan);
$("pressBtn").addEventListener("click", pressButton);
$("pressBtn2").addEventListener("click", pressButton);
$("rainBtn").addEventListener("click", rainEvent);
$("stopBtn").addEventListener("click", () => { stopVoice(); toast("Voice stopped"); });
$("stopBtn2").addEventListener("click", () => { stopVoice(); toast("Voice stopped"); });
$("muteBtn").addEventListener("click", () => {
  muted = !muted; if (muted) stopVoice();
  $("muteBtn").textContent = muted ? "Voice: Off" : "Voice: On";
  $("muteBtn").setAttribute("aria-pressed", String(muted)); $("muteBtn").classList.toggle("off", muted);
  toast(muted ? "Voice off. Soundbox and voice agent will show text only." : "Voice on");
});
$("askBtn").addEventListener("click", () => { ask($("askInput").value); $("askInput").value = ""; });
$("askInput").addEventListener("keydown", (e) => { if (e.key === "Enter") { ask(e.target.value); e.target.value = ""; } });
document.querySelectorAll(".voice-sheet .sug").forEach(b => b.addEventListener("click", () => {
  if (b.id === "closingNote") {
    const ta = "முருகன், இன்று கடை முடிந்தது. இன்று கல்லாவில் எவ்வளவு பணம் வந்தது? யாருக்காவது கடன் கொடுத்தீர்களா?";
    const en = "Murugan, closing time. How much cash came in today? Did you give anyone udhaar?";
    addMsg(T(ta, en), "bot"); speak(T(ta, en), state.lang);
    setTimeout(() => addMsg("Cash 3,000. Lakshmi 200 udhaar.", "me"), 1500);
    setTimeout(() => addMsg(T("சரி. இன்றைய கல்லா ₹3,000, லக்ஷ்மிக்கு ₹200 கடன் குறித்துக்கொண்டேன்.", "Noted: ₹3,000 cash today and ₹200 udhaar for Lakshmi. Your plan is updated."), "bot"), 2600);
    return;
  }
  ask(b.textContent);
}));
// Ask AI by voice: proper dictation. Keeps listening through pauses, shows words live,
// sends when the merchant taps again or goes quiet for ~2.5 s after speaking.
const dict = { rec: null, on: false, text: "", silence: null, idle: null };
function dictStop(send) {
  if (!dict.on) return; dict.on = false;
  clearTimeout(dict.silence); clearTimeout(dict.idle);
  try { dict.rec && dict.rec.stop(); } catch {}
  $("askMic").classList.remove("listening"); $("micLabel").textContent = "Tap and ask";
  const q = dict.text.trim(); dict.text = "";
  if (send && q) { $("askInput").value = ""; ask(q); }
}
function dictStart() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) { toast("Voice input needs Chrome or Edge. You can type instead."); $("askInput").focus(); return; }
  stopVoice();                                       // don't let the Soundbox voice be heard as the question
  dict.on = true; dict.text = ""; $("askInput").value = "";
  $("askMic").classList.add("listening"); $("micLabel").textContent = "Listening… tap to send";
  const begin = () => {
    const r = new SR(); dict.rec = r;
    r.lang = state.lang === "ta" ? "ta-IN" : "en-IN"; r.continuous = true; r.interimResults = true; r.maxAlternatives = 1;
    let finalPart = dict.text;
    r.onresult = (e) => {
      let interim = "";
      for (let i = e.resultIndex; i < e.results.length; i++) {
        const tr = e.results[i][0].transcript;
        if (e.results[i].isFinal) finalPart += (finalPart ? " " : "") + tr.trim(); else interim += tr;
      }
      dict.text = finalPart; $("askInput").value = (finalPart + " " + interim).trim();
      clearTimeout(dict.idle); clearTimeout(dict.silence);
      dict.silence = setTimeout(() => { dict.text = $("askInput").value; dictStop(true); }, 2500);
    };
    r.onerror = (e) => {
      if (e.error === "not-allowed" || e.error === "service-not-allowed") { toast("Please allow the microphone for this site, then tap again."); dictStop(false); }
      else if (e.error === "audio-capture") { toast("No microphone found. You can type instead."); dictStop(false); }
    };
    r.onend = () => { if (dict.on) { try { begin(); } catch { dictStop(true); } } };   // Chrome ends sessions on its own: keep going
    r.start();
  };
  try { begin(); } catch { dictStop(false); return; }
  dict.idle = setTimeout(() => { if (dict.on && !$("askInput").value.trim()) { toast("Didn't hear anything. Tap the mic and speak."); dictStop(false); } }, 12000);
}
$("askMic").addEventListener("click", () => (dict.on ? (dict.text = $("askInput").value, dictStop(true)) : dictStart()));
$("closeVoice").addEventListener("click", () => dictStop(false));
$("resetBtn").addEventListener("click", () => { location.hash = ""; location.reload(); });
fetch("/api/health").then(r => r.json()).then(h => { $("aiStatus").textContent = h.offline ? "AI: offline mode" : ["Gemini", h.sarvam && "Sarvam"].filter(Boolean).join(" + ") + " connected"; $("aiStatus").className = "chip" + (h.offline ? " off" : ""); })
  .catch(() => { $("aiStatus").textContent = "AI: offline mode"; $("aiStatus").className = "chip off"; });

renderPanes(); loadBrief();
if (location.hash === "#home") { showScreen("scrMain"); showTab("Home"); }

// ---- fit the whole demo to any screen ----
// Wide screens: device | phone | controls, zoomed to fit the window with no scrolling.
// Narrow or portrait screens: stacked, and on phones the app fills the screen.
(function fitStage() {
  const stage = document.querySelector(".stage"), top = document.querySelector(".topbar");
  const W = 1180, H = 900;
  function fit() {
    const w = innerWidth, h = innerHeight, wide = w >= 900 && w / h > 1.05;
    document.body.classList.toggle("fit-stage", wide);
    document.body.classList.toggle("mobile", !wide && w < 600);
    if (wide) {
      const avail = h - (top ? top.offsetHeight : 56) - 12;
      const z = Math.min((w - 32) / W, avail / H, 1.25);
      stage.style.zoom = z.toFixed(3);
    } else stage.style.zoom = "";
  }
  addEventListener("resize", fit); addEventListener("orientationchange", fit); fit();
})();
