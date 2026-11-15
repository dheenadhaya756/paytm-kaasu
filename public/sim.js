// Kaasu cash engine. Plain, explainable maths: no AI here.
// Shared by the browser (live slider) and the server (AI brief grounding).

export const SHOP = {
  name: "Murugan Stores",
  owner: "Murugan",
  area: "Velachery, Chennai",
  today: "2026-11-14",
  startBalance: 24000,
  baseSales: 11000,           // average QR collections on a normal day
  costShare: 0.80,            // share of last week's sales paid to distributors every Monday
  ownerBuffer: 8000,          // cash Murugan leaves in the account after his Sunday withdrawal
  weeklyHousehold: 12000,     // the most he takes home in a week
  fixed: [
    { day: 1, amount: 18000, label: "Shop rent" },
    { day: 1, amount: 12000, label: "Helper salary" },
    { day: 10, amount: 3400, label: "Electricity" },
  ],
  goal: { id: "pongal", label: "Pongal stock", amount: 80000, due: "2027-01-06",
          items: "Rice, jaggery, ghee, cashew, sugarcane, pongal pots" },
  udhaar: [
    { name: "Lakshmi", amount: 1240, days: 23, usual: "salary week" },
    { name: "Ravi", amount: 960, days: 31, usual: "month end" },
    { name: "Selvi", amount: 780, days: 18, usual: "month end" },
    { name: "Karthik", amount: 650, days: 40, usual: "irregular" },
    { name: "Fathima", amount: 610, days: 12, usual: "salary week" },
    { name: "Anand", amount: 580, days: 27, usual: "month end" },
  ],
  udhaarRecoveryRate: 0.7,
};

// Illustrative loan and insurance terms for the demo. Real terms come from the lender and the insurer.
export const LOAN = { repayFrom: "2027-01-17", days: 60, costShare: 0.03 };
export const loanDaily = (loan) => Math.ceil((loan * (1 + LOAN.costShare)) / LOAN.days / 10) * 10;
export const COVERS = [
  { id: "loanProtect", name: "Loan protection", premium: 89, term: "Until the loan is repaid",
    covers: ["Hospitalisation for 3 days or more: remaining loan paid off", "Accidental death: remaining loan paid off, family owes nothing"],
    excludes: ["Illness you already had before buying", "Missed payments for any other reason"] },
  { id: "stockCover", name: "Pongal stock cover", premium: 149, term: "16 Dec to 15 Feb", sum: 80000,
    covers: ["Flood and heavy-rain water damage to shop stock", "Fire and short circuit", "Theft after a break-in"],
    excludes: ["Stock that simply expires or doesn't sell", "Damage without photos or a police / fire report where needed"] },
];

const WEEKDAY = [1.25, 0.9, 0.9, 0.95, 1.0, 1.1, 1.3]; // Sun..Sat

export function addDays(iso, n) {
  const d = new Date(iso + "T00:00:00Z");
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
}
export function daysBetween(a, b) {
  return Math.round((new Date(b + "T00:00:00Z") - new Date(a + "T00:00:00Z")) / 86400000);
}

function salesOn(iso, i) {
  const d = new Date(iso + "T00:00:00Z");
  const md = iso.slice(5);
  let f = WEEKDAY[d.getUTCDay()];
  if (md >= "01-11" && md <= "01-16") f *= 2.1;         // Pongal week rush
  if (md === "12-24" || md === "12-31") f *= 1.15;
  const wobble = 1 + 0.06 * Math.sin(i * 1.7) + 0.04 * Math.sin(i * 0.37);
  const normal = SHOP.baseSales * WEEKDAY[d.getUTCDay()] * wobble;
  // Extra Pongal-week sales come from the pre-bought Pongal stock, so they carry no new distributor cost
  return { s: Math.round(SHOP.baseSales * f * wobble), cost: Math.round(normal * SHOP.costShare) };
}

/** Only the gap, plus a Rs 2,000 cushion, rounded up to the next thousand. */
export const loanFor = (gap) => (gap > 0 ? Math.ceil((gap + 2000) / 1000) * 1000 : 0);

export function udhaarTotal() { return SHOP.udhaar.reduce((s, u) => s + u.amount, 0); }
export function udhaarExpected() { return Math.round(udhaarTotal() * SHOP.udhaarRecoveryRate / 10) * 10; }

/**
 * Simulate the next `horizon` days.
 * plan = { dailySave: rupees moved into the Pongal pot each day until the due date,
 *          collectUdhaar: bool, loan: rupees credited 3 weeks before the goal }
 */
export function simulate(plan = {}, horizon = 90) {
  const { dailySave = 0, collectUdhaar = false, loan = 0 } = plan;
  const g = SHOP.goal;
  const loanDay = addDays(g.due, -21);
  let bal = SHOP.startBalance, pot = 0, weekCost = 0, drawn = 0;
  const days = [];
  for (let i = 0; i < horizon; i++) {
    const date = addDays(SHOP.today, i + 1);
    const d = new Date(date + "T00:00:00Z");
    const dom = d.getUTCDate(), dow = d.getUTCDay();
    const { s, cost } = salesOn(date, i);
    bal += s; weekCost += cost;
    if (dow === 1) { bal -= weekCost; weekCost = 0; }  // distributor paid every Monday for last week's stock
    for (const f of SHOP.fixed) if (f.day === dom) bal -= f.amount;
    if (collectUdhaar && i === 9) bal += udhaarExpected();                          // reminders work within ~10 days
    if (loan && date === loanDay) pot += loan;   // loan goes straight into the locked Pongal pot
    if (loan && date >= LOAN.repayFrom && date < addDays(LOAN.repayFrom, LOAN.days)) bal -= loanDaily(loan); // repaid from daily collections after Pongal
    if (date < g.due && dailySave) { const m = Math.min(dailySave, Math.max(0, bal)); bal -= m; pot += m; }
    if (date === g.due) { const fromPot = Math.min(pot, g.amount); pot -= fromPot; bal -= (g.amount - fromPot); }
    if (dow === 0) {                                   // Sunday household withdrawal
      let keep = SHOP.ownerBuffer + Math.round(weekCost * 1.25);   // Monday's distributor bill
      for (let k = 1; k <= 7; k++) {                    // and any rent or salary due this week
        const dd = new Date(addDays(date, k) + "T00:00:00Z").getUTCDate();
        for (const f of SHOP.fixed) if (f.day === dd) keep += f.amount;
      }
      const take = Math.min(SHOP.weeklyHousehold, Math.max(0, bal - keep)); bal -= take; drawn += take;
    }
    days.push({ date, sales: s, balance: Math.round(bal), pot: Math.round(pot) });
  }
  const min = days.reduce((m, x) => (x.balance < m.balance ? x : m), days[0]);
  return { days, minBalance: min.balance, minDate: min.date, shortfall: Math.max(0, -min.balance), drawn };
}

/** The deterministic planner. The AI explains this plan; it never invents the numbers. */
export function recommend() {
  const base = simulate({});
  const daysToGoal = daysBetween(SHOP.today, SHOP.goal.due) - 1;
  const avgWeeklyDraw = Math.round(base.drawn / (90 / 7));
  const dailyFree = Math.round(avgWeeklyDraw / 7);
  const dailySave = Math.max(100, Math.floor((dailyFree * 0.6) / 50) * 50); // never more than ~60% of take-home
  const withSave = simulate({ dailySave, collectUdhaar: true });
  const loan = loanFor(withSave.shortfall);
  const full = simulate({ dailySave, collectUdhaar: true, loan });
  return {
    shop: SHOP, daysToGoal, dailyFree, dailySave,
    udhaarTotal: udhaarTotal(), udhaarExpected: udhaarExpected(), udhaarCount: SHOP.udhaar.length,
    baseline: { shortfall: base.shortfall, minDate: base.minDate },
    afterSaveAndCollect: { shortfall: withSave.shortfall },
    loan, loanDate: addDays(SHOP.goal.due, -21),
    final: { shortfall: full.shortfall, minBalance: full.minBalance },
    potAtGoal: dailySave * daysToGoal,
  };
}

export const inr = (n) => "Rs " + Math.round(n).toLocaleString("en-IN");
