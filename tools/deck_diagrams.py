# Simple-diagram versions of slides 3 to 9. Exec'd by deck_bento.py (shares sl, S, CSS, I, ic, C1, C2, CTX, pain, cap, src).
I.update({
 "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 "moon": '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
 "gift": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
 "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="17" cy="20" r="1.5"/><path d="M3 4h2l2.5 11h11L21 7H6.2"/>',
 "bill": '<path d="M5 2v20l3-2 3 2 3-2 3 2 3-2V2l-3 2-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6M9 16h4"/>',
 "star": '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z"/>',
 "umbrella": '<path d="M12 3a9 9 0 0 1 9 9H3a9 9 0 0 1 9-9zM12 12v7a2 2 0 0 0 4 0"/>',
 "bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4zM10 21h4"/>',
 "hand": '<path d="M7 11V6a1.5 1.5 0 0 1 3 0v4M10 10V4.5a1.5 1.5 0 0 1 3 0V10M13 10V5.5a1.5 1.5 0 0 1 3 0V12M16 9.5a1.5 1.5 0 0 1 3 0V15a6 6 0 0 1-6 6h-1a6 6 0 0 1-5-2.7L4.3 14a1.5 1.5 0 0 1 2.5-1.6L7 13"/>',
 "cash": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/><path d="M6 12h.01M18 12h.01"/>',
 "home2": '<path d="M3 21h18M5 21V9l7-5 7 5v12"/><path d="M9 21v-6h6v6"/>',
 "cpu": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/><path d="M10 10h4v4h-4z"/>',
 "down": '<path d="M12 4v14M6 12l6 6 6-6"/>',
 "warn": '<path d="M12 3 2 20h20zM12 10v4M12 17h.01"/>',
})
def icn(name, bg="var(--pale)", fg="var(--navy)", size=40):
    return f'<span class="ic" style="background:{bg};color:{fg};width:{size}px;height:{size}px;border-radius:{size*0.3:.0f}px;flex:none"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" style="width:{size*0.52:.0f}px;height:{size*0.52:.0f}px">{I[name]}</svg></span>'

CSS += """
/* ---- simple diagrams ---- */
.s:not([data-sec="Title"]) .amb i:nth-child(3) { display: none; }
.hd { display: flex; justify-content: space-between; align-items: flex-end; gap: 24px; }
.hd .t { font-size: 38px; }
.dg { position: relative; }
.dg svg.wires { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; pointer-events: none; }
.wire { fill: none; stroke: #9cc9e6; stroke-width: 2; }
.dark .wire, .c-navy .wire { stroke: rgba(255,255,255,.28); }
.wire.flow2 { stroke: var(--sky); stroke-dasharray: 3 9; animation: dash 1.2s linear infinite; }
.s.on .wire.draw { stroke-dasharray: 600; stroke-dashoffset: 600; animation: wireIn 1.3s var(--ease) both; animation-delay: calc(.4s + var(--i, 0) * 120ms); }
@keyframes wireIn { to { stroke-dashoffset: 0; } }
.nd { position: absolute; display: flex; align-items: center; gap: 12px; border-radius: 16px; padding: 12px 16px; font-size: 14.5px; font-weight: 600; line-height: 1.25; }
.nd small { display: block; font-size: 12px; font-weight: 500; opacity: .7; margin-top: 2px; }
.nd.w { background: #fff; color: var(--ink); box-shadow: 0 0 0 1px var(--line), 0 10px 24px -18px rgba(1,43,114,.5); }
.nd.p { background: var(--pale); color: var(--navy); }
.nd.n { background: var(--navy); color: #fff; }
.nd.k { background: var(--sky); color: #fff; }
.nd.g { background: rgba(255,255,255,.08); color: #fff; box-shadow: inset 0 0 0 1px rgba(255,255,255,.14); }
.nd.r { background: #fde6ec; color: #b0173f; }
.s.on .nd { animation: rise .8s var(--ease) both; animation-delay: calc(.25s + var(--i, 0) * 110ms); }
.s .nd { opacity: 0; }
.pill-n { width: 26px; height: 26px; border-radius: 50%; display: grid; place-items: center; font-size: 12.5px; font-weight: 800; background: var(--sky); color: #fff; flex: none; }
/* need vs have */
.nh { display: grid; gap: 18px; }
.nh-row { display: grid; grid-template-columns: 150px 1fr; gap: 14px; align-items: center; }
.nh-row > span { font-size: 13.5px; font-weight: 600; color: var(--ink-2); line-height: 1.3; }
.nh-track { height: 46px; display: flex; gap: 2px; }
.nh-track i { display: flex; align-items: center; padding: 0 14px; color: #fff; font-style: normal; font-size: 16px; font-weight: 600; white-space: nowrap; transform-origin: left; }
.nh-track i:first-child { border-radius: 4px 0 0 4px; } .nh-track i:last-child { border-radius: 0 4px 4px 0; }
.gap-h { background: repeating-linear-gradient(135deg, #fde6ec 0 8px, #f9cdd8 8px 16px) !important; color: #b0173f !important; box-shadow: inset 0 0 0 1.5px #e0345c; }
.s.on .nh-track i { animation: grow 1.1s var(--ease) both; animation-delay: calc(.45s + var(--i, 0) * 200ms); }
.axis { display: grid; grid-template-columns: 150px 1fr; gap: 14px; font-size: 11.5px; color: var(--muted); }
.axis div { display: flex; justify-content: space-between; border-top: 1px solid var(--line); padding-top: 6px; }
/* loop */
.loop-ring { position: absolute; border-radius: 50%; border: 2px dashed rgba(255,255,255,.25); }
.s.on .loop-ring { animation: spin 40s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.loop-dot { position: absolute; width: 12px; height: 12px; margin: -6px; border-radius: 50%; background: var(--sky); box-shadow: 0 0 14px var(--sky); offset-rotate: 0deg; }
.s.on .loop-dot { animation: orbit 8s linear infinite; }
@keyframes orbit { to { offset-distance: 100%; } }
/* step ladder */
.ladder { display: grid; gap: 10px; }
.ladder > div { display: grid; grid-template-columns: 40px 1fr auto; gap: 14px; align-items: center; border-radius: 16px; padding: 14px 18px; }
.ladder b { font-size: 15.5px; display: block; } .ladder .v { font-size: 22px; font-weight: 500; letter-spacing: -.02em; white-space: nowrap; font-variant-numeric: tabular-nums; }
/* feature columns */
.fcol { height: 470px; border-radius: 20px; padding: 22px; display: flex; flex-direction: column; gap: 10px; }
.fcol h3 { margin: 0 0 4px; font-size: 19px; font-weight: 600; letter-spacing: -.02em; display: flex; align-items: center; gap: 12px; }
.fi { flex: 1; display: grid; grid-template-columns: 40px 1fr auto; gap: 12px; align-items: center; background: #fff; border-radius: 14px; padding: 12px 14px; box-shadow: 0 0 0 1px var(--line); }
.fi b { font-size: 14.5px; color: var(--ink); display: block; } .fi .mini { margin-top: 2px; line-height: 1.35; }
.fi .kpi { font-size: 17px; font-weight: 600; color: var(--navy); white-space: nowrap; font-variant-numeric: tabular-nums; }
.fcol.navy { background: var(--navy); color: #fff; } .fcol.pale { background: var(--pale); color: var(--navy); } .fcol.sky { background: linear-gradient(160deg, #00baf2, #0a9bd0); color: #fff; }
/* matrix */
.mtx { position: relative; border-radius: 18px; background: #fff; box-shadow: 0 0 0 1px var(--line); }
.mtx .q { position: absolute; display: grid; place-items: center; font-size: 11.5px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: #b7c3d4; }
.mtx .pt { position: absolute; display: flex; align-items: center; gap: 7px; font-size: 12.5px; font-weight: 600; color: var(--ink-2); white-space: nowrap; transform: translate(-7px, -50%); }
.mtx .pt i { width: 14px; height: 14px; border-radius: 50%; background: #c9d3e1; box-shadow: 0 0 0 3px #fff; flex: none; }
.mtx .pt.us { font-size: 15px; color: var(--navy); font-weight: 700; } .mtx .pt.us i { width: 22px; height: 22px; background: #1F5FD1; box-shadow: 0 0 0 6px rgba(31,95,209,.18); }
.mtx .pt.l { flex-direction: row-reverse; transform: translate(calc(-100% + 7px), -50%); }
.s.on .mtx .pt { animation: rise .7s var(--ease) both; animation-delay: calc(.5s + var(--i, 0) * 80ms); }
.s.on .mtx .pt.us i { animation: pulse 2.4s 1.4s ease-in-out infinite; }
@keyframes pulse { 50% { box-shadow: 0 0 0 12px rgba(31,95,209,.08); } }
/* equation */
.eq { display: grid; grid-template-columns: 1fr 30px 1fr 30px 1fr 30px 1.15fr; align-items: stretch; }
.eq .op { display: grid; place-items: center; font-size: 26px; font-weight: 300; color: var(--sky); }
.donut { position: relative; width: 150px; height: 150px; }
.donut svg { transform: rotate(-90deg); }
.s.on .donut .arc { animation: arcIn 1.4s var(--ease) both .5s; }
@keyframes arcIn { from { stroke-dasharray: 0 400; } }
"""

def wires(paths, w, h, cls="wire draw"):
    return f'<svg class="wires" viewBox="0 0 {w} {h}" preserveAspectRatio="none" aria-hidden="true">' + "".join(f'<path class="{cls}" style="--i:{k}" d="{d}"/>' for k, d in enumerate(paths)) + '</svg>'

def node(x, y, w, cls, body, k, h=None, extra=""):
    hh = f"height:{h}px;" if h else ""
    return f'<div class="nd {cls}" style="left:{x}px;top:{y}px;width:{w}px;{hh}--i:{k};{extra}">{body}</div>'

# ============ 3 · PROBLEM: need vs have + why the gap ============
need, have = 80000, 47480
causes = [("cal", "Festival stock is paid early", "Weeks before festival sales arrive"), ("home", "Profit goes home every Sunday", "Before the big bill comes"),
          ("users", "Udhaar stays unpaid", "Asking regulars feels risky"), ("warn", "Credit comes late", "Found in a panic, at a bad price")]
cause_nodes = "".join(node(0, 8 + k * 92, 300, "g", f'{icn(a, "rgba(255,255,255,.12)", "#fff", 38)}<div>{b}<small>{c}</small></div>', k) for k, (a, b, c) in enumerate(causes))
cause_wires = wires([f"M300 {44 + k*92} C 350 {44 + k*92}, 340 182, 392 182" for k in range(4)], 560, 380)
sl[33] = S("", "One shop, one date, one number. The bar shows the gap; the diagram shows why it happens: timing, not sales.", f'''
<div class="hd"><div><div class="eb a">Problem statement</div><h2 class="t a d1">Murugan sells ₹11,240 a day. On 6 January he is ₹32,520 short.</h2></div></div>
<div class="grid" style="grid-template-columns:1fr 1.05fr;gap:16px;margin-top:22px;height:500px">
  <div class="c c-white a d2" style="padding:26px;display:flex;flex-direction:column">
    <div class="eb">The Pongal stock bill · 6 January</div>
    <div class="nh" style="margin-top:14px">
      <div class="nh-row"><span>Needs</span><div class="nh-track"><i style="width:100%;background:var(--navy);--i:0">₹80,000</i></div></div>
      <div class="nh-row"><span>Will have at today's pace</span><div class="nh-track"><i style="width:{have/need*100:.1f}%;background:#1F5FD1;--i:1">₹47,480</i><i class="gap-h" style="width:{(need-have)/need*100:.1f}%;--i:2">−₹32,520</i></div></div>
    </div>
    <div class="axis" style="margin-top:10px"><span></span><div><span>₹0</span><span>₹40,000</span><span>₹80,000</span></div></div>
    <div class="bubble" style="margin-top:auto;box-shadow:none;background:var(--mist)"><span class="ta">"வியாபாரம் நல்லா இருக்கு. ஆனா தேவைப்படும் நாள்ல பணம் இல்ல."</span><small>"Business is good. The money isn't there on the day I need it." · Murugan Stores, Velachery, Chennai</small></div>
    <div class="grid" style="grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px">
      <div class="c c-pale" style="padding:12px 14px"><div class="big" style="font-size:26px">₹11,240</div><div class="mini">Sales a day</div></div>
      <div class="c c-pale" style="padding:12px 14px"><div class="big" style="font-size:26px">53 days</div><div class="mini">Left to fix it</div></div>
      <div class="c c-pale" style="padding:12px 14px"><div class="big" style="font-size:26px">₹35,000</div><div class="mini">Usual panic loan</div></div>
    </div>
  </div>
  <div class="c c-navy a d3" style="padding:26px">
    <div class="eb">Why the gap · timing, not sales</div>
    <div class="dg" style="height:380px;margin-top:14px">
      {cause_wires}{cause_nodes}
      {node(392, 128, 150, "k", '<div style="text-align:center;width:100%">Cash gap<small style="opacity:.9">−₹32,520</small></div>', 4, extra="justify-content:center")}
      {node(392, 250, 150, "r", '<div style="text-align:center;width:100%">Panic loan<small style="opacity:.85">₹35,000 at the worst price</small></div>', 5)}
      <svg class="wires" viewBox="0 0 560 380" aria-hidden="true"><path class="wire flow2" d="M467 200 V 246" /></svg>
    </div>
  </div>
</div>''')

# ============ 4 · WHY IT MATTERS: reach chain + donut + pressure bars ============
chain = [("4.9 Cr", "Paytm merchants", "Q4 FY26"), ("1.64 Cr", "Soundboxes on counters", "+27 lakh in a year"), ("₹7.1 L Cr", "Merchant payments a quarter", "+26% a year")]
chain_html = "".join(node(0, k * 108, 270, "w" if k else "n", f'<div><div class="big" style="font-size:30px;{"color:#fff" if not k else "color:var(--navy)"}">{a}</div><div style="margin-top:4px">{b}<small>{c}</small></div></div>', k) for k, (a, b, c) in enumerate(chain))
chain_w = wires([f"M135 {84 + k*108} V {108 + k*108}" for k in range(2)], 270, 320)
sl[34] = S("", "Paytm already reaches these shops, and kiranas still sell almost all grocery. But their money is under pressure. Hover a bar for its value.", f'''
<div class="hd"><div><div class="eb a">Why it matters · research data</div><h2 class="t a d1">Payments are solved. Money isn't.</h2></div><span class="mini a d1" style="max-width:430px;text-align:right">Sources: Paytm Q2 FY27 &amp; Q4 FY26 results, Redseer, NPCI, PwC × Kirana Club (508 stores), Datum, CPM India (4,593 stores), AICPDF, Outlook Business</span></div>
<div class="grid" style="grid-template-columns:300px 270px 1fr;gap:16px;margin-top:22px;height:500px">
  <div class="c c-pale a d2" style="padding:22px 15px">
    <div class="eb" style="padding:0 0 0 0">1 · Paytm already reaches them</div>
    <div class="dg" style="height:320px;margin-top:10px">{chain_w}{chain_html}</div>
    <div class="mini" style="margin-top:22px">85% of Paytm merchant loans already go to device owners.</div>
  </div>
  <div class="c c-white a d3" style="padding:22px;display:flex;flex-direction:column;align-items:center;text-align:center">
    <div class="eb" style="align-self:flex-start">2 · Kiranas own grocery</div>
    <div class="donut" style="margin-top:34px"><svg viewBox="0 0 150 150" width="150" height="150"><circle cx="75" cy="75" r="60" fill="none" stroke="{CTX}" stroke-width="18"/><circle class="arc" cx="75" cy="75" r="60" fill="none" stroke="{C1}" stroke-width="18" stroke-dasharray="{0.91*377:.0f} 377" data-tip="Kiranas: 91%"/></svg>
      <div style="position:absolute;inset:0;display:grid;place-items:center"><div class="big" style="font-size:38px;color:var(--ink)">91%</div></div></div>
    <div class="lbl" style="margin-top:18px">of India's grocery is still sold by kiranas</div>
    <div class="legend" style="justify-content:center"><span><i style="background:{C1}"></i>Kiranas</span><span><i style="background:{CTX}"></i>Others</span></div>
    <div class="mini" style="margin-top:auto">Redseer · 20.7 bn UPI payments a month (NPCI)</div>
  </div>
  <div class="c c-white chart a d4"><div class="eb">3 · But their money is under pressure</div><div class="mini" style="margin-bottom:12px">Share of stores or buyers, surveys 2024–2026</div>
    {"".join(f'<div class="hb" data-tip="{l}: {v}%" style="grid-template-columns:1fr;gap:4px;padding:7px 0"><span class="hb-l" style="font-weight:500">{l}</span><span style="display:flex;align-items:center;gap:10px"><span class="hb-track" style="flex:1"><i class="bar" style="width:{v}%;background:{C1}"></i></span><span class="hb-v">{v}%</span></span></div>' for l, v in pain)}
    <div class="mini" style="margin-top:auto">About 2 lakh kiranas closed (AICPDF claim) · ₹25–30 lakh crore MSME credit gap</div>
  </div>
</div>''')

# ============ 5 · SOLUTION: the daily loop + closing the gap in order ============
R, CX, CY = 140, 280, 215
pts = [(CX, CY - R), (CX + R, CY), (CX, CY + R), (CX - R, CY)]
loop_items = [("sun", "7 am · Soundbox speaks", "Today's plan, in Tamil"), ("mic", "He says “aam”", "Or presses OK on older boxes"), ("phone", "UPI PIN confirms", "Money moves only after the PIN"), ("moon", "9 pm · auto-save", "Into the partner-bank pot")]
offs = [(-105, -70), (-60, -36), (-105, -2), (-140, -36)]
loop_nodes = "".join(node(max(0, x + dx), y + dy, 210 if k % 2 == 0 else 200, "g", f'{icn(a, "var(--sky)", "#fff", 36)}<div>{b}<small>{c}</small></div>', k) for k, ((x, y), (dx, dy), (a, b, c)) in enumerate(zip(pts, offs, loop_items)))
sl[35] = S("dark", "Kaasu, Tamil for money. The daily loop on the left, and on the right how the gap closes: own money first, udhaar back, loan only for what is left.", f'''
<div class="hd"><div><div class="eb a">How we solve it · Paytm Kaasu</div><h2 class="t a d1" style="color:#fff">Kaasu plans the shop's cash, 53 days ahead.</h2></div><p class="p a d1" style="max-width:360px;text-align:right">காசு, Tamil for money. On the Soundbox and the Paytm for Business app he already uses. No new hardware.</p></div>
<div class="grid" style="grid-template-columns:560px 1fr;gap:20px;margin-top:20px;height:500px">
  <div class="dg a d2" style="height:440px">
    <div class="loop-ring" style="left:{CX-R}px;top:{CY-R}px;width:{2*R}px;height:{2*R}px"></div>
    <div class="loop-dot" style="left:0;top:0;offset-path:path('M {CX} {CY-R} A {R} {R} 0 1 1 {CX-0.01} {CY-R}')"></div>
    <img src="img/coin.svg" alt="" style="position:absolute;left:{CX-70}px;top:{CY-70}px;width:140px">
    <div style="position:absolute;left:{CX-80}px;top:{CY+66}px;width:160px;text-align:center;font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--sky-2)">Every day</div>
    {loop_nodes}
  </div>
  <div class="a d3" style="display:flex;flex-direction:column">
    <div class="eb">Closing the ₹32,520 gap, in order</div>
    <div class="ladder" style="margin-top:6px">
      <div class="st" style="background:rgba(255,255,255,.08)"><span class="pill-n">1</span><div><b>His own money first</b><span class="mini">₹600 a day × 52 days</span></div><span class="v">₹31,200</span></div>
      <div class="st" style="background:rgba(255,255,255,.08)"><span class="pill-n">2</span><div><b>Udhaar back on payday</b><span class="mini">Paytm reminds, not the shop</span></div><span class="v">₹3,370</span></div>
      <div class="st" style="background:#fff;color:var(--ink)"><span class="pill-n" style="background:var(--navy)">3</span><div><b style="color:var(--navy)">Loan only for what is left</b><span class="mini" style="color:var(--muted)">₹190 a day from 17 Jan, after festival sales</span></div><span class="v" style="color:var(--navy)">₹11,000</span></div>
    </div>
    <div class="grid" style="grid-template-columns:1fr 1fr;gap:10px;margin-top:14px">
      <div class="c c-sky" style="padding:16px 18px"><div class="big" style="font-size:34px">−69%</div><div class="lbl">Smaller loan than the ₹35,000 panic loan</div></div>
      <div class="c c-glass" style="padding:16px 18px"><div class="big" style="font-size:34px">₹0</div><div class="lbl">Customers' Pongal pre-bookings can take the loan to zero</div></div>
    </div>
  </div>
</div>''')

# ============ 6 · FEATURES: three jobs, nine features ============
groups = [
  ("navy", "cash", "Brings money in", [("gift", "Pongal pre-booking", "Regulars pre-pay festival hampers; settles T+1", "24 joined"), ("cart", "Buy together", "4 nearby shops pool orders", "6% off"), ("bill", "Check a bill", "AI reads distributor bills for missed discounts", "₹446")]),
  ("pale", "shield", "Protects the shop", [("star", "Save Score", "Regular savers get cheaper loans", "1.2%/mo"), ("umbrella", "Rain Shield", "IMD red alert pauses repayments, pays cover", "₹3,000"), ("bell", "Payday udhaar", "Paytm reminds each customer on payday", "₹3,370")]),
  ("sky", "users", "Helps the people around it", [("hand", "Bharosa", "Confirmed udhaar paid to the shop today", "₹2,577"), ("users", "Staff advance", "Helper asks the Soundbox; no interest", "≤50% wage"), ("cash", "Galla check", "Spoken cash count vs expected, no blame", "₹210 found")]),
]
def fcol(cls, hic, title, items, k):
    hb, hf = ("rgba(255,255,255,.14)", "#fff") if cls != "pale" else ("#fff", "var(--navy)")
    return f'''<div class="fcol {cls} a d{k+2}"><h3>{icn(hic, hb, hf, 38)}{title}</h3>''' + "".join(
        f'<div class="fi st">{icn(a, "var(--pale)", "var(--navy)", 40)}<div><b>{b}</b><div class="mini">{c}</div></div><span class="kpi">{d}</span></div>' for a, b, c, d in items) + "</div>"
sl[36] = S("", "Nine features, grouped by the job they do. The live demo shows each one; the first six were not found in any earlier Paytm hackathon entry or product.", f'''
<div class="hd"><div><div class="eb a">How we solve it · features</div><h2 class="t a d1">Nine features. Three jobs.</h2></div><span class="tag sky a d1">All nine run in the live demo</span></div>
<div class="grid" style="grid-template-columns:repeat(3,1fr);gap:16px;margin-top:22px">{"".join(fcol(c, h, t, it, k) for k, (c, h, t, it) in enumerate(groups))}</div>
<div class="mini a d5" style="margin-top:14px">Partly exists elsewhere: customer-visible khata (PhonePe), Paytm Postpaid, wage advances (Square, GajiGesa abroad), POS cash-drawer tools. Kaasu adds per-entry confirmation, udhaar takeover, voice on the Soundbox and patterns instead of blame.</div>''')

# ============ 7 · ARCHITECTURE: four lanes, one flow ============
lanes = [("Shop", "w", [("phone", "Paytm Soundbox", "Tamil voice · OK button"), ("home2", "Business app", "Journeys · UPI PIN"), ("users", "Customers' Paytm app", "Confirm udhaar · pre-book")]),
         ("Paytm platform", "p", [("cloud", "Soundbox fleet", "4G SIM · OTA updates"), ("book", "Merchant account", "Payment history · KYC"), ("rupee", "UPI + Payment Aggregator", "Settles T+1")]),
         ("Kaasu service", "n", [("chart", "Cash engine", "Rules compute every rupee"), ("cpu", "AI layer", "Gemini · Sarvam voice"), ("shield", "Guardrail + consent", "Numbers checked · DPDP log")]),
         ("Regulated partners", "w", [("bank", "Partner bank", "Savings pots"), ("rupee", "NBFC / bank lenders", "Loans with KFS"), ("umbrella", "Insurer + IMD", "Rain Shield")])]
LW, GAP = 262, 40
arch_nodes, arch_heads = "", ""
for li, (title, cls, items) in enumerate(lanes):
    x = li * (LW + GAP)
    arch_heads += f'<div style="position:absolute;left:{x}px;top:0;width:{LW}px;font-size:11.5px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#0089c2">{li+1} · {title}</div>'
    for k, (a, b, c) in enumerate(items):
        bg, fg = ("rgba(255,255,255,.14)", "#fff") if cls == "n" else ("var(--pale)" if cls == "w" else "#fff", "var(--navy)")
        arch_nodes += node(x, 30 + k * 96, LW, cls, f'{icn(a, bg, fg, 36)}<div>{b}<small>{c}</small></div>', li * 3 + k, h=80)
arch_w = []
for li in range(3):
    x1, x2 = li * (LW + GAP) + LW, (li + 1) * (LW + GAP)
    for k in range(3):
        y = 70 + k * 96
        arch_w.append(f"M{x1} {y} H {x2}")
arch_svg = wires(arch_w, 4 * LW + 3 * GAP, 330, "wire flow2")
steps = ["Payments flow in", "Engine plans, AI explains", "He says yes, PIN confirms", "Partners move the money"]
step_html = "".join(f'<div style="position:absolute;left:{k*(LW+GAP)}px;top:330px;width:{LW}px;display:flex;align-items:center;gap:10px;font-size:13.5px;font-weight:600;color:var(--navy)"><span class="pill-n">{k+1}</span>{s}</div>' for k, s in enumerate(steps))
rbi = [("RBI-ready by design", "Paytm distributes; regulated partners hold money and lend"), ("Digital Lending Directions 2025", "KFS + APR, cooling-off, direct disbursal and repayment"), ("Payment Aggregator rules 2025", "Pre-bookings settle to the shop T+1, never held in escrow"), ("DPDP Act · Code on Wages", "Consent for reminders; deductions within the 50% limit")]
sl[29] = S("", "Left to right: the shop, Paytm's existing platform, the Kaasu service, and the regulated partners who hold money and lend. Money only moves after the merchant's PIN.", f'''
<div class="hd"><div><div class="eb a">Architecture and tech stack</div><h2 class="t a d1">Kaasu runs on what Paytm already has.</h2></div><span class="tag sky a d1">Node.js · Vercel · Gemini · Sarvam AI</span></div>
<div class="dg a d2" style="height:360px;margin-top:24px;width:{4*LW+3*GAP}px">{arch_heads}<div style="position:absolute;left:0;top:0;right:0;height:330px">{arch_svg}</div>{arch_nodes}{step_html}</div>
<div class="grid a d4" style="grid-template-columns:repeat(4,1fr);gap:10px;margin-top:24px">
  {"".join(f'<div class="c {"c-navy" if k==0 else "c-white"}" style="padding:12px 14px;display:flex;gap:10px;align-items:flex-start">{icn("shield" if k==0 else "check", "rgba(255,255,255,.14)" if k==0 else "#dff5ec", "#fff" if k==0 else "var(--green)", 30)}<div><b style="font-size:13px">{a}</b><div class="mini" style="margin-top:2px">{b}</div></div></div>' for k, (a, b) in enumerate(rbi))}
</div>''')

# ============ 8 · COMPETITION: 2x2 map + USP ============
MW, MH = 600, 470
players = [("Paytm Kaasu", .8, .86, True, True), ("Square · Shopify (US)", .66, .58, False, True), ("“Money SOS” (2026 hackathon)", .36, .66, False, False),
           ("Pine Labs agents", .72, .36, False, True), ("Reelo / LoyalStack", .64, .1, False, False), ("KiranaPro Vani", .5, .22, False, False),
           ("BharatPe assistant", .38, .3, False, True), ("Paytm AI Soundbox", .22, .42, False, False), ("OkCredit / Khatabook", .14, .14, False, False), ("PhonePe Business", .08, .06, False, False)]
pad = 46
def px(fx, fy): return pad + fx * (MW - 2 * pad), (MH - pad) - fy * (MH - 2 * pad)
pts_html = "".join(f'<div class="pt{" us" if us else ""}{" l" if left else ""}" style="left:{px(fx,fy)[0]:.0f}px;top:{px(fx,fy)[1]:.0f}px;--i:{k}"><i></i>{n}</div>' for k, (n, fx, fy, us, left) in enumerate(players))
usp6 = ["Plans ahead, doesn't just answer", "Own money first, loan only the gap", "On 1.64 Cr devices already on counters", "Paytm asks for udhaar, not the shop", "Maths decides, AI explains, PIN moves money", "Tamil voice; OK button on older boxes"]
sl[37] = S("dark", "Everyone answers. Few act. Nobody else plans the shop's cash ahead, by voice, on the counter. Top right is empty except for Kaasu.", f'''
<div class="grid" style="grid-template-columns:{MW}px 1fr;gap:26px;height:100%">
  <div class="a d1" style="display:flex;flex-direction:column">
    <div class="eb">Competition map</div>
    <div class="mtx" style="width:{MW}px;height:{MH}px;margin-top:6px">
      <svg width="{MW}" height="{MH}" style="position:absolute;inset:0" aria-hidden="true"><path d="M{MW/2} {pad-20} V {MH-pad+10} M {pad-10} {MH/2} H {MW-pad+20}" stroke="#e3eaf3" stroke-width="1.5"/>
        <path d="M{pad} {MH-pad+18} H {MW-pad+14}" stroke="#9cb0c9" stroke-width="1.5" marker-end="url(#ah)"/><path d="M{pad-18} {MH-pad} V {pad-14}" stroke="#9cb0c9" stroke-width="1.5" marker-end="url(#ah)"/>
        <defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 10 5 0 10z" fill="#9cb0c9"/></marker></defs></svg>
      <div class="q" style="left:{MW/2}px;top:{pad-10}px;right:{pad}px;height:40px;place-items:end;color:#1F5FD1">Plans ahead + acts</div>
      <div style="position:absolute;left:{pad}px;bottom:4px;right:{pad}px;text-align:center;font-size:12px;font-weight:600;color:var(--muted)">Does more for the shop →</div>
      <div style="position:absolute;left:4px;top:{pad}px;bottom:{pad}px;writing-mode:vertical-rl;transform:rotate(180deg);text-align:center;font-size:12px;font-weight:600;color:var(--muted)">Looks ahead at cash →</div>
      {pts_html}
    </div>
    <div class="mini" style="margin-top:10px;color:rgba(255,255,255,.6)">Placed from public product information and 12 earlier Paytm Build for India entries, Nov 2026. Our reading, not a measurement.</div>
  </div>
  <div style="display:flex;flex-direction:column">
    <div class="eb a">USP</div>
    <h2 class="t a d1" style="font-size:38px;color:#fff">Others answer questions. Kaasu plans the cash.</h2>
    <div class="grid a d2" style="grid-template-columns:1fr 1fr;gap:10px;margin-top:22px">
      {"".join(f'<div class="c c-glass" style="padding:14px 16px"><span style="font-size:24px;color:var(--sky-2);font-weight:300">0{k+1}</span><div class="lbl" style="margin-top:4px">{u}</div></div>' for k, u in enumerate(usp6))}
    </div>
    <div class="c c-sky a d3" style="margin-top:auto;padding:16px 18px"><div class="lbl" style="margin:0">Idea chosen from 10 we scored: 19/20 on uniqueness, impact, Paytm fit and feasibility. A sales chatbot scored 13.</div></div>
  </div>
</div>''')

# ============ 9 · BUSINESS MODEL: same canvas, maths as a visual equation ============
eq_cards = [("Kaasu plan", "₹49 a month × 12 = ₹588 a shop", "× 10,00,000 shops", "₹58.8 Cr"),
            ("Loan fee", "3,00,000 loans × ₹11,000 = ₹330 Cr lent", "× 3% distribution fee", "₹9.9 Cr"),
            ("Bharosa fee", "₹31,200 udhaar a shop a year", "× 10,00,000 × 2% partner fee", "₹62.4 Cr")]
eq = '<div class="eq st" style="grid-column:1/11;grid-row:3">'
for k, (h, a, b, r) in enumerate(eq_cards):
    eq += f'<div class="c-white" style="border-radius:16px;padding:12px 14px"><h4 style="color:#0089c2">{k+1} · {h}</h4><div class="mathl">{a}</div><div class="mathl">{b}</div><div class="mathr">{r}</div></div><div class="op">{"+" if k < 2 else "="}</div>'
eq += '''<div style="border-radius:16px;padding:12px 16px;background:var(--sky);color:#fff"><h4 style="color:#fff;opacity:.85">Total a year · 10 lakh shops</h4><div style="font-size:32px;font-weight:500;letter-spacing:-.03em;line-height:1.1">₹131.1 Cr</div><div class="mathl" style="color:rgba(255,255,255,.92);margin-top:4px">− AI cost ₹15 × 12 × 10 lakh = ₹18 Cr → <b>₹113 Cr net</b></div></div></div>'''
s9 = sl[30]
a0 = s9.index('<div class="st" style="grid-column:1/11;grid-row:3;padding:0;display:grid;grid-template-columns:1fr 1fr 1fr 1.15fr;gap:10px">')
a1 = s9.index('</div>\n</div>\n<div class="mini a d3"')
sl[30] = s9[:a0] + eq + "\n" + s9[a1 + len("</div>\n"):]
