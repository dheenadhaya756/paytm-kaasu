"""Paytm Kaasu deck, modern bento style: white slides, mono pill tags, lime keyword highlights,
blue / navy / lime tiles, arrow chips, gradient cover. 10 slides. Writes public/deck/index.html."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "deck", "index.html")

CSS = r"""
:root { --blue: #1F5FD1; --sky: #00BAF2; --navy: #002E6E; --lime: #D7F75B; --lime-2: #c4ea2f; --ink: #0d0f14; --ink-2: #4a5161; --muted: #8a91a0; --line: #e6e8ee; --bg: #f4f5f8;
  --font: "Inter", -apple-system, "Segoe UI", sans-serif; --mono: "JetBrains Mono", ui-monospace, monospace; --tamil: "Anek Tamil", sans-serif; --ease: cubic-bezier(.22, 1, .36, 1); color-scheme: light; }
* { box-sizing: border-box; }
html, body { margin: 0; height: 100%; overflow: hidden; background: #c9ccd4; font-family: var(--font); color: var(--ink); -webkit-font-smoothing: antialiased; }
button { font: inherit; cursor: pointer; }
.stage { position: fixed; inset: 0; display: grid; place-items: center; }
.deck { position: relative; width: 1280px; height: 720px; transform-origin: center; }
.s { position: absolute; inset: 0; background: #fff; overflow: hidden; border-radius: 6px; box-shadow: 0 30px 70px -30px rgba(10,20,50,.45);
  opacity: 0; visibility: hidden; transform: translateX(30px) scale(.985); transition: opacity .7s var(--ease), transform .9s var(--ease), visibility 0s .7s; }
.s.on { opacity: 1; visibility: visible; transform: none; transition: opacity .7s var(--ease), transform .9s var(--ease), visibility 0s; }
.s.past { transform: translateX(-30px) scale(.985); }
.in { position: absolute; inset: 40px 56px 44px; }
/* chrome */
.tagp { position: absolute; left: 56px; top: 36px; display: inline-flex; align-items: center; height: 22px; padding: 0 11px; border-radius: 99px; background: var(--ink); color: #fff; font: 600 10px/1 var(--mono); letter-spacing: .1em; text-transform: uppercase; z-index: 2; }
.brand { position: absolute; right: 56px; top: 40px; font: 500 10px/1 var(--mono); letter-spacing: .12em; text-transform: uppercase; color: var(--ink-2); z-index: 2; }
.brand::before { content: "↳ "; }
.pg { position: absolute; right: 56px; bottom: 26px; font: 500 10px/1 var(--mono); color: var(--muted); letter-spacing: .1em; z-index: 2; }
.dark .tagp { background: #fff; color: var(--navy); } .dark .brand, .dark .pg { color: rgba(255,255,255,.75); }
/* type */
h1, h2 { margin: 0; font-weight: 500; letter-spacing: -.035em; line-height: 1.08; text-wrap: balance; }
h2 { font-size: 40px; }
.hl { background: var(--lime); border-radius: 10px; padding: 0 .16em; margin: 0 -.04em; box-decoration-break: clone; -webkit-box-decoration-break: clone; }
.hl.b { background: var(--blue); color: #fff; }
.body { font-size: 14px; line-height: 1.55; color: var(--ink-2); margin: 0; }
.sm { font-size: 12px; line-height: 1.45; color: var(--muted); }
.k { font-size: 11px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; }
.num { font-weight: 500; letter-spacing: -.04em; line-height: 1; font-variant-numeric: tabular-nums; }
.ta { font-family: var(--tamil); letter-spacing: 0; }
/* tiles */
.t { position: absolute; border-radius: 22px; padding: 22px; overflow: hidden; }
.t.blue { background: var(--blue); color: #fff; } .t.navy { background: var(--navy); color: #fff; } .t.lime { background: var(--lime); color: var(--ink); }
.t.sky { background: var(--sky); color: #fff; } .t.grey { background: var(--bg); } .t.line { background: #fff; box-shadow: inset 0 0 0 1.5px var(--ink); } .t.soft { background: #fff; box-shadow: inset 0 0 0 1px var(--line); }
.t.blue .sm, .t.navy .sm, .t.sky .sm { color: rgba(255,255,255,.78); } .t.lime .sm { color: rgba(13,15,20,.68); }
.t.img { padding: 0; background: linear-gradient(160deg, #e9f6fd, #cdeefc); }
.arrow { position: absolute; width: 34px; height: 34px; border-radius: 50%; display: grid; place-items: center; background: #fff; color: var(--ink); box-shadow: inset 0 0 0 1.5px var(--ink); transition: transform .4s var(--ease); }
.arrow svg { width: 15px; height: 15px; }
.t:hover .arrow { transform: rotate(45deg); }
.arrow.solid { background: var(--ink); color: #fff; box-shadow: none; }
.pill { display: inline-flex; align-items: center; gap: 8px; height: 30px; padding: 0 6px 0 14px; border-radius: 99px; font-size: 12.5px; font-weight: 600; }
.pill i { width: 22px; height: 22px; border-radius: 50%; display: grid; place-items: center; font-style: normal; font-size: 12px; }
.chip { display: inline-flex; align-items: center; height: 26px; padding: 0 12px; border-radius: 99px; font-size: 11.5px; font-weight: 600; box-shadow: inset 0 0 0 1px rgba(255,255,255,.55); color: #fff; }
.rowl { display: grid; grid-template-columns: 1fr 30px; align-items: center; gap: 12px; padding: 11px 0; border-bottom: 1px solid var(--line); font-size: 13px; color: var(--ink-2); }
.rowl b { color: var(--ink); font-weight: 600; }
.rowl .ar { width: 26px; height: 26px; border-radius: 50%; background: var(--ink); color: #fff; display: grid; place-items: center; }
.rowl .ar svg { width: 12px; height: 12px; }
.ic { width: 38px; height: 38px; border-radius: 12px; display: grid; place-items: center; }
.ic svg { width: 19px; height: 19px; }
/* cover */
.cover { background: radial-gradient(120% 140% at 20% 10%, #00BAF2 0%, #1F5FD1 38%, #0c3fa8 62%, #002E6E 100%); color: #fff; }
.cover .wave { position: absolute; border-radius: 50%; filter: blur(60px); opacity: .55; }
.s.on .wave { animation: drift 14s ease-in-out infinite alternate; }
@keyframes drift { to { transform: translate(-80px, 50px) scale(1.15); } }
/* motion */
.s .a { opacity: 0; }
.s.on .a { animation: rise .9s var(--ease) both; animation-delay: calc(.12s + var(--d, 0) * 90ms); }
@keyframes rise { from { opacity: 0; transform: translateY(18px) scale(.985); filter: blur(4px); } to { opacity: 1; transform: none; filter: none; } }
.s.on .grow { animation: grow 1.2s var(--ease) both; animation-delay: calc(.5s + var(--d, 0) * 90ms); transform-origin: left; }
.s.on .growy { animation: growy 1.2s var(--ease) both; animation-delay: calc(.45s + var(--d, 0) * 80ms); transform-origin: bottom; }
@keyframes grow { from { transform: scaleX(0); } } @keyframes growy { from { transform: scaleY(0); } }
.s.on .float { animation: float 6s ease-in-out infinite; } @keyframes float { 50% { transform: translateY(-8px); } }
.t { transition: transform .45s var(--ease), box-shadow .45s var(--ease); }
.t.hov:hover { transform: translateY(-4px); box-shadow: 0 22px 40px -22px rgba(10,20,50,.45); }
.flow { stroke-dasharray: 3 8; animation: dash 1.2s linear infinite; } @keyframes dash { to { stroke-dashoffset: -22; } }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: .01ms !important; animation-delay: 0s !important; transition-duration: .01ms !important; } .s .a { opacity: 1; } }
/* hud */
.hud { position: fixed; left: 0; right: 0; bottom: 0; display: flex; align-items: center; justify-content: space-between; padding: 10px 18px; font-size: 12px; color: #3b4150; z-index: 10; }
.hud button { border: 0; background: rgba(13,15,20,.08); color: var(--ink); border-radius: 10px; padding: 7px 12px; font-size: 12.5px; font-weight: 600; }
.bar { position: fixed; left: 0; top: 0; height: 3px; background: var(--blue); transition: width .5s var(--ease); z-index: 10; }
.dots { display: flex; gap: 5px; } .dots i { width: 6px; height: 6px; border-radius: 50%; background: rgba(13,15,20,.22); cursor: pointer; transition: width .3s var(--ease), background .3s; }
.dots i.on { width: 20px; border-radius: 4px; background: var(--blue); }
.notes { position: fixed; right: 16px; top: 16px; width: 340px; background: rgba(13,15,20,.92); color: #eef; border-radius: 14px; padding: 14px 16px; font-size: 13.5px; line-height: 1.5; z-index: 11; }
.tip { position: fixed; z-index: 30; pointer-events: none; background: var(--ink); color: #fff; font-size: 12px; font-weight: 600; padding: 6px 9px; border-radius: 8px; opacity: 0; transition: opacity .15s; white-space: nowrap; }
.tip.on { opacity: 1; }
"""

ARW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12 12 4M5.5 4H12v6.5"/></svg>'
ICONS = {
 "gift": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
 "cart": '<circle cx="9" cy="20" r="1.5"/><circle cx="17" cy="20" r="1.5"/><path d="M3 4h2l2.5 11h11L21 7H6.2"/>',
 "bill": '<path d="M5 2v20l3-2 3 2 3-2 3 2 3-2V2l-3 2-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6M9 16h4"/>',
 "star": '<path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z"/>',
 "umbrella": '<path d="M12 3a9 9 0 0 1 9 9H3a9 9 0 0 1 9-9zM12 12v7a2 2 0 0 0 4 0"/>',
 "bell": '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4zM10 21h4"/>',
 "hand": '<path d="M7 11V6a1.5 1.5 0 0 1 3 0v4M10 10V4.5a1.5 1.5 0 0 1 3 0V10M13 10V5.5a1.5 1.5 0 0 1 3 0V12M16 9.5a1.5 1.5 0 0 1 3 0V15a6 6 0 0 1-6 6h-1a6 6 0 0 1-5-2.7L4.3 14a1.5 1.5 0 0 1 2.5-1.6L7 13"/>',
 "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-3.5 3-6 7-6s7 2.5 7 6M16 4a3.5 3.5 0 0 1 0 7M18 14c2.5.7 4 2.8 4 6"/>',
 "cash": '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/>',
 "phone": '<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/>',
 "cloud": '<path d="M7 18a4 4 0 0 1-.5-8A6 6 0 0 1 18 9a4.5 4.5 0 0 1-1 9z"/>',
 "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
 "cpu": '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
 "shield": '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/>',
 "bank": '<path d="M3 10 12 4l9 6M5 10v8M9 10v8M15 10v8M19 10v8M3 20h18"/>',
 "rupee": '<path d="M7 4h10M7 9h10M7 4c6 0 6 10 0 10l8 6"/>',
 "home": '<path d="M3 21h18M5 21V9l7-5 7 5v12"/><path d="M9 21v-6h6v6"/>',
 "book": '<path d="M4 19.5V5a2 2 0 0 1 2-2h14v16H6.5A2.5 2.5 0 0 0 4 21.5z"/>',
 "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
 "mic": '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10v1a7 7 0 0 0 14 0v-1M12 18v4"/>',
 "moon": '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
 "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
}
def ic(name, bg="#fff", fg="var(--ink)", size=38):
    return f'<span class="ic" style="background:{bg};color:{fg};width:{size}px;height:{size}px"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg></span>'
def arrow(x, y, solid=False, pos="right"):
    side = f"right:{x}px" if pos == "right" else f"left:{x}px"
    return f'<span class="arrow{" solid" if solid else ""}" style="{side};top:{y}px">{ARW}</span>'
def T(x, y, w, h, cls, body, d=0, extra=""):
    return f'<div class="t {cls} a hov" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;--d:{d};{extra}">{body}</div>'
def A(x, y, w, body, d=0, extra=""):
    return f'<div class="a" style="position:absolute;left:{x}px;top:{y}px;width:{w}px;--d:{d};{extra}">{body}</div>'

slides = []
def slide(tag, notes, body, cls="", n=None):
    k = len(slides) + 1
    slides.append(f'<section class="s {cls}" data-notes="{notes}"><span class="tagp">{tag}</span><span class="brand">Paytm Kaasu</span><span class="pg">{k:02d} / 10</span><div class="in">{body}</div></section>\n')

# 1 ─ COVER
slide("Paytm Buildathon · Track 1", "Hi, I'm Dheena. This is Paytm Kaasu: every shop's cash, planned.", f'''
<div class="wave" style="width:620px;height:620px;right:-160px;top:-200px;background:#59d2f7"></div>
<div class="wave" style="width:520px;height:520px;left:-180px;bottom:-240px;background:#0a2f9a;animation-direction:alternate-reverse"></div>
{A(0, 30, 300, '<img src="/brand/paytm-logo-white.svg" alt="Paytm" style="height:26px;margin-top:24px">', 0)}
<img class="a float" src="img/coin.svg" alt="" style="position:absolute;right:60px;top:110px;width:330px;--d:3">
{A(0, 190, 700, '<h1 style="font-size:84px;letter-spacing:-.05em;line-height:.98">Every shop\'s cash, <span class="hl" style="color:var(--ink)">planned.</span></h1>', 1)}
{A(0, 408, 560, '<p class="body" style="color:rgba(255,255,255,.85);font-size:16px">An AI cash-flow partner for kirana shops, on the Paytm Soundbox and the Paytm for Business app. Savings, udhaar and smart loans, in the shop\'s own language.</p>', 2)}
{A(0, 544, 900, '<div style="display:flex;gap:10px;flex-wrap:wrap"><span class="chip">Savings pots</span><span class="chip">Udhaar back</span><span class="chip">Gap-only loans</span><span class="chip">5 languages</span><span class="chip">RBI-ready</span></div>', 3)}
{A(838, 556, 330, '<div style="text-align:right;font-size:13px;color:rgba(255,255,255,.8)">Presented by<br><b style="color:#fff;font-size:15px">Dheena Dhayalan R</b></div>', 4)}''', "cover dark")

# 2 ─ ABOUT ME (no client names)
slide("About me", "Ten seconds about me, then straight to the problem.", f'''
{A(0, 60, 480, '<h2 style="font-size:46px">Hi, I\'m<br><span class="hl">Dheena Dhayalan R</span></h2>', 0)}
{A(0, 200, 430, '<p class="body" style="font-size:15px">Engineering graduate and Forward Deployed Designer at Rock Paper Scissors, a fintech design agency. I build products end to end: research, design and working code.</p>', 1)}
{A(0, 330, 430, '<div class="sm k" style="color:var(--ink)">What I bring to Kaasu</div>' + "".join(f'<div class="rowl"><span><b>{a}</b> · {b}</span><span class="ar">{ARW}</span></div>' for a, b in [("Engineering", "patented hardware and systems"), ("Fintech design", "lending, wealth and insurance products"), ("Shipping", "this demo, live, in 5 languages")]), 2)}
{T(500, 60, 320, 260, "blue", f'<div class="num" style="font-size:96px">8</div><div style="font-size:17px;font-weight:600;margin-top:10px">Patents in engineering</div><div class="sm" style="margin-top:6px">Granted and filed</div>{arrow(20, 20, pos="right")}', 1)}
{T(836, 60, 332, 260, "lime", f'<div class="num" style="font-size:80px">₹25L+</div><div style="font-size:17px;font-weight:600;margin-top:16px">Won for IEEE projects</div><div class="sm" style="margin-top:6px">Prize money and grants</div>{arrow(20, 20, True)}', 2)}
{T(500, 336, 320, 260, "line", f'<div class="k" style="color:var(--blue)">Research</div><div class="num" style="font-size:44px;margin-top:16px">Elsevier</div><div style="font-size:15px;font-weight:600;margin-top:10px">Book chapter author</div><div class="sm" style="margin-top:4px">MIT Square</div>{arrow(20, 20)}', 3)}
{T(836, 336, 332, 260, "navy", f'<div class="k" style="color:var(--sky)">Track record</div><div class="num" style="font-size:44px;margin-top:16px">Hackathons</div><div style="font-size:15px;font-weight:600;margin-top:10px">Winner, several times</div><img src="/brand/rps-logo-white.svg" alt="Rock Paper Scissors" style="position:absolute;left:22px;bottom:24px;height:15px;opacity:.85">{arrow(20, 20)}', 4)}''')

# 3 ─ PROBLEM
causes = [("Festival stock is paid early", "Weeks before festival sales arrive"), ("Profit goes home every Sunday", "Before the big bill comes"), ("Udhaar stays unpaid", "Asking regulars feels risky"), ("Credit comes late", "A ₹35,000 panic loan at the worst price")]
slide("Problem statement", "One shop, one date, one number. Business is fine; the timing of cash is broken.", f'''
{A(0, 60, 560, '<h2>Murugan sells ₹11,240 a day. On 6 January he is <span class="hl">₹32,520 short.</span></h2>', 0)}
{A(0, 236, 470, '<div class="bubble" style="background:var(--bg);border-radius:18px;padding:16px 18px"><div class="ta" style="font-size:17px;font-weight:600;line-height:1.45">"வியாபாரம் நல்லா இருக்கு. ஆனா தேவைப்படும் நாள்ல பணம் இல்ல."</div><div class="sm" style="margin-top:6px">"Business is good. The money isn\'t there on the day I need it." · Murugan Stores, Velachery, Chennai</div></div>', 1)}
{A(0, 390, 470, '<div class="sm k" style="color:var(--ink)">Why: timing, not sales</div>' + "".join(f'<div class="rowl"><span><b>0{k+1} · {a}</b> · {b}</span><span class="ar">{ARW}</span></div>' for k, (a, b) in enumerate(causes)), 2)}
{T(560, 60, 612, 350, "soft", '<div class="k" style="color:var(--ink)">The Pongal stock bill · 6 January</div><div class="sm">Needs vs what he will have at today\'s pace</div>'
  + '<div style="display:flex;align-items:flex-end;gap:60px;height:230px;margin:26px 0 0 40px;border-bottom:1.5px solid var(--ink);padding:0 30px">'
  + '<div style="width:110px;height:100%;display:flex;flex-direction:column;justify-content:flex-end;align-items:center"><span style="font-weight:600;font-size:15px;margin-bottom:8px">₹80,000</span><i class="growy" style="display:block;width:46px;height:100%;background:var(--ink);border-radius:6px 6px 0 0;--d:0"></i></div>'
  + '<div style="width:110px;height:100%;display:flex;flex-direction:column;justify-content:flex-end;align-items:center"><span style="font-weight:600;font-size:15px;margin-bottom:8px">₹47,480</span><i class="growy" style="display:block;width:46px;height:59%;background:var(--blue);border-radius:6px 6px 0 0;--d:2"></i></div>'
  + '<div style="flex:1;height:100%;position:relative"><div class="a" style="position:absolute;left:0;bottom:59%;top:0;width:150px;border-radius:12px;background:repeating-linear-gradient(135deg,#fde6ec 0 7px,#fbd2dc 7px 14px);box-shadow:inset 0 0 0 1.5px #e0345c;display:grid;place-items:center;color:#b0173f;font-weight:700;font-size:17px;--d:6">−₹32,520 gap</div></div></div>'
  + '<div style="display:flex;gap:96px;margin:8px 0 0 70px" class="sm"><span>Needs</span><span>Will have</span></div>', 1)}
{T(560, 426, 300, 170, "blue", '<div class="num" style="font-size:52px">53</div><div style="font-weight:600;margin-top:10px">days left to fix it</div><div class="sm" style="margin-top:4px">Today is 15 November</div>' + arrow(18, 18), 3)}
{T(876, 426, 296, 170, "lime", '<div class="num" style="font-size:52px">₹35,000</div><div style="font-weight:600;margin-top:10px">the usual panic loan</div><div class="sm" style="margin-top:4px">Taken late, at the worst price</div>' + arrow(18, 18, True), 4)}''')

# 4 ─ WHY IT MATTERS
pain = [("Buyers moved ¼ of kirana shopping online", 82), ("Kiranas saw food and FMCG sales fall", 52), ("Fall in Tier 1 footfall", 28), ("Kiranas planning any tech spend", 22), ("Small businesses reaching formal credit", 14)]
cols = "".join(f'<div style="flex:1;height:100%;display:flex;flex-direction:column;justify-content:flex-end;align-items:center" data-tip="{l}: {v}%"><span style="font-size:13px;font-weight:600;margin-bottom:6px">{v}%</span><i class="growy" style="display:block;width:26px;height:{v}%;background:{"var(--blue)" if k == 0 else "var(--ink)"};border-radius:5px 5px 0 0;--d:{k}"></i></div>' for k, (l, v) in enumerate(pain))
labs = "".join(f'<div style="flex:1;text-align:center;font-size:10.5px;line-height:1.3;color:var(--ink-2)">{l}</div>' for l, v in pain)
slide("Market research", "Paytm already reaches these shops. Kiranas still sell almost all grocery. But their money is under pressure.", f'''
{A(0, 60, 520, '<h2>Payments are solved. <span class="hl">Money isn\'t.</span></h2>', 0)}
{A(0, 176, 450, '<p class="body">Paytm already sits on the counter of India\'s kiranas, and kiranas still sell almost all of India\'s grocery. Yet the shops are under pressure and only a few reach formal credit.</p>', 1)}
{T(0, 300, 220, 296, "blue", '<div class="num" style="font-size:52px">1.64<span style="font-size:24px"> Cr</span></div><div style="font-weight:600;margin-top:12px">Soundboxes on counters</div><div class="sm" style="margin-top:6px">+27 lakh in a year · 4.9 Cr Paytm merchants</div>' + arrow(18, 18), 2)}
{T(236, 300, 220, 296, "lime", '<div class="num" style="font-size:52px">91%</div><div style="font-weight:600;margin-top:12px">of grocery still sold by kiranas</div><div class="sm" style="margin-top:6px">Redseer · 20.7 bn UPI payments a month</div>' + arrow(18, 18, True), 3)}
{T(490, 60, 682, 536, "soft", f'<div class="k">Kiranas under pressure</div><div class="sm">Share of stores or buyers, surveys 2024–2026 · hover a bar</div><div style="display:flex;gap:18px;height:300px;margin-top:30px;border-bottom:1.5px solid var(--ink);padding:0 10px">{cols}</div><div style="display:flex;gap:18px;padding:10px 10px 0">{labs}</div><div class="sm" style="position:absolute;left:22px;right:22px;bottom:20px">Sources: Paytm Q2 FY27 &amp; Q4 FY26, Redseer, NPCI, PwC × Kirana Club (508 stores), Datum, CPM India (4,593 stores), AICPDF, Outlook Business · ₹25–30 lakh crore MSME credit gap</div>', 1)}''')

# 5 ─ SOLUTION
loop = [("sun", "7 am", "Soundbox speaks today's plan"), ("mic", "He says “aam”", "Or presses OK on older boxes"), ("phone", "UPI PIN", "Money moves only after the PIN"), ("moon", "9 pm", "Auto-saves into a partner-bank pot")]
slide("Solution", "Kaasu, Tamil for money. A daily loop on the Soundbox, and the gap closed in order: own money, udhaar, then a small loan.", f'''
{A(0, 60, 470, '<h2>Meet <span class="hl">Paytm Kaasu</span>, the shop\'s cash planner.</h2>', 0)}
{A(0, 196, 440, '<p class="body"><span class="ta">காசு</span> means money. Kaasu sees the festival gap 53 days early and plans it on the Soundbox and app the shop already uses. No new hardware.</p>', 1)}
{A(0, 300, 440, '<div class="sm k" style="color:var(--ink)">Every day</div>' + "".join(f'<div class="rowl" style="grid-template-columns:40px 1fr"><span>{ic(i, "var(--bg)", "var(--blue)", 32)}</span><span><b>{a}</b> · {b}</span></div>' for i, a, b in loop), 2)}
{T(470, 60, 330, 350, "img", '<img class="float" src="img/soundbox-on.png" alt="Paytm Soundbox speaking" style="position:absolute;left:50%;top:50%;height:300px;transform:translate(-50%,-50%)">', 1)}
{T(816, 60, 356, 350, "img", '<img src="img/p-short.png" alt="Pongal plan screen" style="position:absolute;left:50%;top:26px;width:250px;transform:translateX(-50%);border-radius:26px;box-shadow:0 20px 40px -20px rgba(0,46,110,.5)">', 2)}
{T(470, 426, 230, 170, "blue", '<div class="sm k" style="color:rgba(255,255,255,.8)">1 · Own money</div><div class="num" style="font-size:36px;margin-top:12px">₹31,200</div><div class="sm" style="margin-top:6px">₹600 a day × 52 days</div>', 3)}
{T(716, 426, 220, 170, "navy", '<div class="sm k" style="color:rgba(255,255,255,.8)">2 · Udhaar back</div><div class="num" style="font-size:36px;margin-top:12px">₹3,370</div><div class="sm" style="margin-top:6px">Paytm reminds on payday</div>', 4)}
{T(952, 426, 220, 170, "lime", '<div class="sm k">3 · Loan, gap only</div><div class="num" style="font-size:36px;margin-top:12px">₹11,000</div><div class="sm" style="margin-top:6px">−69% vs the panic loan</div>', 5)}''')

# 6 ─ FEATURES
groups = [("blue", "Brings money in", [("gift", "Pongal pre-booking", "24 joined"), ("cart", "Buy together", "6% off"), ("bill", "Check a bill", "₹446 found")]),
          ("navy", "Protects the shop", [("star", "Save Score", "1.2% a month"), ("umbrella", "Rain Shield", "₹3,000 cover"), ("bell", "Payday udhaar", "₹3,370 back")]),
          ("lime", "Helps the people around it", [("hand", "Bharosa", "₹2,577 today"), ("users", "Staff advance", "No interest"), ("cash", "Galla check", "₹210 found")])]
fhtml = ""
for k, (cls, title, items) in enumerate(groups):
    x = 380 + k * 268
    onlime = cls == "lime"
    rows = "".join(f'<div style="display:flex;align-items:center;gap:12px;padding:12px 0;border-top:1px solid {"rgba(13,15,20,.14)" if onlime else "rgba(255,255,255,.18)"}">{ic(i, "rgba(255,255,255,.65)" if onlime else "rgba(255,255,255,.14)", "var(--ink)" if onlime else "#fff", 34)}<div><b style="font-size:14.5px">{a}</b><div class="sm">{b}</div></div></div>' for i, a, b in items)
    btn = f'<span class="pill" style="position:absolute;left:22px;bottom:22px;background:{"var(--ink)" if onlime else "#fff"};color:{"#fff" if onlime else "var(--ink)"}">{["Grow", "Protect", "Support"][k]}<i style="background:{"var(--lime)" if onlime else "var(--blue)"};color:{"var(--ink)" if onlime else "#fff"}">→</i></span>'
    fhtml += T(x, 60, 252, 536, cls, f'<span style="display:grid;place-items:center;width:28px;height:28px;border-radius:50%;background:{"var(--ink)" if onlime else "#fff"};color:{"#fff" if onlime else "var(--ink)"};font-size:12px;font-weight:700">{k+1}</span><div style="font-size:21px;font-weight:600;letter-spacing:-.02em;line-height:1.15;margin:18px 0 18px">{title}</div>{rows}{btn}', k + 1)
slide("Features", "Nine features grouped by the job they do. All nine run in the live demo.", f'''
{A(0, 60, 340, '<h2>Nine features. <span class="hl">Three jobs.</span></h2>', 0)}
{A(0, 196, 330, '<p class="body">Each feature turns the shop\'s own Paytm payments into money in hand, protection, or help for the people around the counter.</p>', 1)}
{A(0, 330, 330, '<div class="sm">The first six were not found in any earlier Paytm hackathon entry or product. The last three extend ideas that partly exist (PhonePe Khata, Paytm Postpaid, wage advances abroad).</div>', 2)}
{A(0, 556, 330, '<span class="pill" style="background:var(--lime)">All nine in the live demo<i style="background:var(--ink);color:#fff">↗</i></span>', 3)}
{fhtml}''')

# 7 ─ ARCHITECTURE
lanes = [("Shop", "soft", [("phone", "Paytm Soundbox", "Voice · OK button"), ("home", "Business app", "Journeys · UPI PIN"), ("users", "Customers' app", "Confirm · pre-book")]),
         ("Paytm", "grey", [("cloud", "Soundbox fleet", "4G · OTA updates"), ("book", "Merchant account", "Payments · KYC"), ("rupee", "UPI + PA", "Settles T+1")]),
         ("Kaasu", "blue", [("chart", "Cash engine", "Rules compute every rupee"), ("cpu", "AI layer", "Gemini · Sarvam voice"), ("shield", "Guardrail", "Numbers checked · consent")]),
         ("Partners", "lime", [("bank", "Partner bank", "Savings pots"), ("rupee", "NBFC / bank lenders", "Loans with KFS"), ("umbrella", "Insurer + IMD", "Rain Shield")])]
LW, G = 278, 18
ahtml = ""
for li, (name, cls, items) in enumerate(lanes):
    x = li * (LW + G)
    dark = cls == "blue"
    rows = "".join(f'<div style="display:flex;align-items:center;gap:12px;padding:10px 0;{"border-top:1px solid " + ("rgba(255,255,255,.2)" if dark else "rgba(13,15,20,.1)") if j else ""}">{ic(i, "rgba(255,255,255,.16)" if dark else "#fff", "#fff" if dark else "var(--ink)", 34)}<div><b style="font-size:14px">{a}</b><div class="sm">{b}</div></div></div>' for j, (i, a, b) in enumerate(items))
    ahtml += T(x, 200, LW, 250, cls, f'<div style="display:flex;justify-content:space-between;align-items:center"><span class="k" style="color:{"#fff" if dark else "var(--ink)"}">{li+1} · {name}</span></div><div style="margin-top:10px">{rows}</div>', li + 1)
    if li < 3:
        ahtml += f'<svg class="a" style="position:absolute;left:{x+LW-4}px;top:312px;width:{G+8}px;height:26px;--d:{li+2};z-index:3;overflow:visible" viewBox="0 0 26 26"><circle cx="13" cy="13" r="12" fill="var(--ink)"/><path d="M8 13h10M14 9l4 4-4 4" stroke="#fff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'
rbi = [("Digital Lending Directions 2025", "KFS + APR, cooling-off, direct disbursal and repayment"), ("Payment Aggregator rules 2025", "Pre-bookings settle to the shop T+1, never escrow"), ("Partner-bank savings", "Paytm distributes; regulated partners hold money"), ("DPDP Act · Code on Wages", "Consent for reminders; deductions within 50%")]
slide("Architecture", "Left to right: the shop, Paytm's existing platform, the Kaasu service, and regulated partners. Money only moves after the merchant's PIN.", f'''
{A(0, 60, 640, '<h2>Built on what <span class="hl">Paytm already runs.</span></h2>', 0)}
{A(700, 72, 472, '<p class="body" style="text-align:right">Payments flow in, the engine plans and the AI explains, the merchant says yes and the PIN confirms, then regulated partners move the money.</p>', 1)}
{ahtml}
{A(0, 470, 1172, '<div class="k" style="margin-bottom:4px">RBI-ready by design</div><div style="display:grid;grid-template-columns:1fr 1fr;column-gap:40px">' + "".join(f'<div class="rowl"><span><b>{a}</b> · {b}</span><span class="ar">{ARW}</span></div>' for a, b in rbi) + '</div><div class="sm" style="margin-top:10px">Stack: Node.js · Vercel · Gemini 3.5 Flash-Lite · Sarvam Bulbul + Saaras · voice in Tamil, Hindi, Malayalam, Kannada and English</div>', 6)}''')

# 8 ─ COMPETITION + USP
MW, MH, pad = 600, 440, 44
players = [("Paytm Kaasu", .8, .86, True, True), ("Square · Shopify (US)", .66, .58, False, True), ("“Money SOS” (2026 hackathon)", .36, .66, False, False),
           ("Pine Labs agents", .74, .38, False, True), ("Reelo / LoyalStack", .64, .1, False, False), ("KiranaPro Vani", .5, .22, False, False),
           ("BharatPe assistant", .38, .3, False, True), ("Paytm AI Soundbox", .22, .44, False, False), ("OkCredit / Khatabook", .14, .14, False, False), ("PhonePe Business", .08, .04, False, False)]
def pxy(fx, fy): return pad + fx * (MW - 2 * pad), (MH - pad) - fy * (MH - 2 * pad)
pts = ""
for k, (n, fx, fy, us, left) in enumerate(players):
    x, y = pxy(fx, fy)
    dot = f'<i style="width:{22 if us else 13}px;height:{22 if us else 13}px;border-radius:50%;background:{"var(--blue)" if us else "#c3c8d2"};{"box-shadow:0 0 0 7px rgba(31,95,209,.18);" if us else ""}flex:none"></i>'
    lab = f'<span style="font-size:{15 if us else 12.5}px;font-weight:{700 if us else 600};color:{"var(--ink)" if us else "var(--ink-2)"}">{n}</span>'
    pts += f'<div class="a" style="position:absolute;left:{x:.0f}px;top:{y:.0f}px;display:flex;align-items:center;gap:8px;white-space:nowrap;transform:translate({"calc(-100% + 7px)" if left else "-7px"},-50%);--d:{k+2}">{lab + dot if left else dot + lab}</div>'
usp = ["Plans ahead, doesn't just answer", "Own money first, loan only the gap", "On 1.64 Cr devices already on counters", "Paytm asks for udhaar, not the shop", "Maths decides, AI explains, PIN moves money", "Voice in 5 languages; OK button on older boxes"]
slide("Competition", "Everyone answers. Few act. Nobody else plans the shop's cash ahead, by voice, on the counter. Top right is ours.", f'''
{T(0, 60, MW, MH + 96, "grey", f'<div class="k">Competition map</div><div class="sm">Our reading of public product information, Nov 2026</div><div style="position:absolute;left:0;top:96px;width:{MW}px;height:{MH}px">'
  + f'<svg width="{MW}" height="{MH}" style="position:absolute;inset:0"><path d="M{MW/2} {pad-14} V {MH-pad+8} M {pad-8} {MH/2} H {MW-pad+14}" stroke="#d5d9e1" stroke-width="1.5" stroke-dasharray="4 5"/><path d="M{pad} {MH-pad+16} H {MW-pad+16}" stroke="var(--ink)" stroke-width="1.5"/><path d="M{pad-16} {MH-pad} V {pad-16}" stroke="var(--ink)" stroke-width="1.5"/></svg>'
  + f'<span class="tagp" style="position:absolute;left:auto;right:{pad}px;top:{pad-34}px;background:var(--lime);color:var(--ink)">Plans ahead + acts</span>'
  + f'<div class="sm" style="position:absolute;left:{pad}px;right:{pad}px;bottom:2px;text-align:center;color:var(--ink)">Does more for the shop →</div>'
  + f'<div class="sm" style="position:absolute;left:2px;top:{pad}px;bottom:{pad}px;writing-mode:vertical-rl;transform:rotate(180deg);text-align:center;color:var(--ink)">Looks ahead at cash →</div>{pts}</div>', 0)}
{A(640, 60, 532, '<h2>Others answer questions. <span class="hl">Kaasu plans the cash.</span></h2>', 1)}
{A(640, 210, 532, '<div class="k" style="margin-bottom:2px">Our USP</div>' + "".join(f'<div class="rowl"><span><b>0{k+1}</b> · {u}</span><span class="ar">{ARW}</span></div>' for k, u in enumerate(usp)), 2)}
{T(640, 516, 532, 80, "blue", '<div style="font-weight:600;font-size:14px;line-height:1.4;padding-right:50px">Chosen from 10 ideas we scored: 19/20 on uniqueness, impact, Paytm fit and feasibility.</div>' + arrow(22, 23), 3)}''')

# 9 ─ BUSINESS MODEL
canvas = [("Key partners", "Partner banks · NBFC and bank lenders · Postpaid lender · IRDAI insurers · Gemini, Sarvam AI"), ("Key activities", "Cash-flow engine · voice briefs · udhaar reminders · loan and insurance distribution"),
          ("Value proposition", "Sees the festival gap 53 days early · own money first, loan only the gap · voice on a device he already has"), ("Channels", "Paytm Soundbox · Business app · customers' Paytm app · field sales"), ("Customer segments", "Kiranas with a Soundbox · their customers · shop helpers · lenders and insurers")]
cv = "".join(T(k * 236, 186, 228, 168, ["soft", "grey", "navy", "grey", "soft"][k], f'<div class="k" style="color:{"var(--sky)" if k == 2 else "var(--blue)"}">{a}</div><div style="font-size:12.5px;line-height:1.5;margin-top:10px">{b}</div>', k + 1) for k, (a, b) in enumerate(canvas))
rev = [("blue", "1 · Kaasu plan", "₹49 a month × 12 × 10 lakh shops", "₹58.8 Cr"), ("blue", "2 · Loan fee", "3 lakh loans × ₹11,000 × 3%", "₹9.9 Cr"), ("blue", "3 · Bharosa fee", "₹31,200 udhaar × 10 lakh × 2%", "₹62.4 Cr")]
eq = ""
for k, (cls, h, m, r) in enumerate(rev):
    eq += T(k * 252, 386, 226, 210, cls, f'<div class="sm k" style="color:rgba(255,255,255,.85)">{h}</div><div class="num" style="font-size:40px;margin-top:22px">{r}</div><div class="sm" style="margin-top:12px">{m}</div>', k + 6)
    eq += f'<div class="a" style="position:absolute;left:{k*252+226}px;top:470px;width:26px;text-align:center;font-size:24px;font-weight:300;--d:{k+6}">{"+" if k < 2 else "="}</div>'
eq += T(756, 386, 416, 210, "lime", '<div class="sm k">Total a year · 10 lakh shops</div><div class="num" style="font-size:64px;margin-top:14px">₹131.1 Cr</div><div style="font-size:13.5px;margin-top:14px;font-weight:500">− AI cost ₹15 × 12 × 10 lakh = ₹18 Cr → <b>₹113 Cr net</b></div>' + arrow(20, 20, True), 9)
slide("Business model", "The canvas on top, the exact maths below. 10 lakh shops is about 6% of Soundboxes; prices and take rates are our assumptions for a pilot.", f'''
{A(0, 60, 700, '<h2>How Kaasu makes <span class="hl">₹131 Cr a year.</span></h2>', 0)}
{A(760, 72, 412, '<p class="sm" style="text-align:right">10 lakh shops = about 6% of 1.64 Cr Soundboxes. Prices, take rates and adoption are our assumptions to test in a pilot. Not counted: insurance commission, deposit referrals, more UPI on Paytm.</p>', 1)}
{cv}{eq}''')

# 10 ─ THANK YOU
src = "Paytm Q2 FY27 &amp; Q4 FY26 results · YourStory · Analytics India Magazine · Redseer · NPCI via Inc42 · PwC × Kirana Club (Upstox) · Datum Intelligence · AICPDF (Business Standard) · CPM India (Mediabrief) · Grant Thornton Bharat · Outlook Business · Business Today · Sarvam AI · RBI Digital Lending Directions 2025 · RBI Payment Aggregator Master Direction 2025 · DPDP Act 2023 · Code on Wages 2019"
slide("Thank you", "Close on the ask, then stop.", f'''
<div class="wave" style="width:620px;height:620px;right:-200px;bottom:-260px;background:#59d2f7"></div>
{A(0, 30, 300, '<img src="/brand/paytm-logo-white.svg" alt="Paytm" style="height:24px;margin-top:24px">', 0)}
{A(0, 110, 760, '<h1 style="font-size:70px;letter-spacing:-.05em;line-height:1">Let\'s pilot it in Chennai <span class="hl" style="color:var(--ink)">this Pongal.</span></h1>', 1)}
{T(0, 340, 250, 150, "lime", '<div class="num" style="font-size:46px">1,000</div><div style="font-weight:600;margin-top:10px">Chennai shops in the pilot</div>', 2)}
{T(266, 340, 250, 150, "glass", '<div class="num" style="font-size:46px">−69%</div><div style="font-weight:600;margin-top:10px">Smaller festival loan</div>', 3, "background:rgba(255,255,255,.12);box-shadow:inset 0 0 0 1px rgba(255,255,255,.25)")}
{T(532, 340, 250, 150, "glass", '<div class="num" style="font-size:46px">₹0</div><div style="font-weight:600;margin-top:10px">New hardware needed</div>', 4, "background:rgba(255,255,255,.12);box-shadow:inset 0 0 0 1px rgba(255,255,255,.25)")}
{T(814, 60, 354, 420, "soft", '<div class="k" style="color:var(--blue)">Try it</div>' + "".join(f'<div class="rowl"><span><b>{a}</b><br>{b}</span><span class="ar">{ARW}</span></div>' for a, b in [("Live demo", "paytm-kaasu.vercel.app"), ("Pitch deck", "paytm-kaasu.vercel.app/deck"), ("Code", "github.com/dheenadhaya756/paytm-kaasu"), ("Film", "paytm-kaasu.vercel.app/media/kaasu-film.mp4")]) + '<div style="margin-top:18px;font-size:13px;color:var(--ink-2)">Dheena Dhayalan R</div>', 5)}
{A(0, 540, 1168, f'<div style="font-size:10.5px;line-height:1.5;color:rgba(255,255,255,.7)"><b style="color:#fff">Sources, research 14–15 Nov 2026:</b> {src}</div>', 6)}''', "cover dark")

JS = r"""
const $ = (id) => document.getElementById(id);
const deck = $("deck"), slides = [...deck.children]; let i = 0;
function fit() { const k = Math.min(innerWidth / 1300, (innerHeight - 50) / 740); deck.style.transform = `scale(${k})`; }
const tip = document.createElement("div"); tip.className = "tip"; document.body.appendChild(tip);
document.addEventListener("mouseover", (e) => { const t = e.target.closest("[data-tip]"); if (!t) { tip.classList.remove("on"); return; } tip.textContent = t.dataset.tip; tip.classList.add("on"); });
document.addEventListener("mousemove", (e) => { tip.style.left = (e.clientX + 14) + "px"; tip.style.top = (e.clientY + 14) + "px"; });
function countUp(s) {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  s.querySelectorAll(".num").forEach((el) => {
    const n = el.firstChild; if (!n || n.nodeType !== 3) return; if (!el.dataset.orig) el.dataset.orig = n.nodeValue;
    const m = el.dataset.orig.match(/^([^\d]*)([\d][\d,]*\.?\d*)(.*)$/); if (!m) return;
    const [, pre, num, post] = m, dec = (num.split(".")[1] || "").length, comma = num.includes(","), to = parseFloat(num.replace(/,/g, "")), t0 = performance.now();
    const f = (v) => comma ? Math.round(v).toLocaleString("en-IN") : v.toFixed(dec);
    const st = (t) => { const k = Math.min(1, (t - t0) / 1100), e = 1 - Math.pow(1 - k, 3); n.nodeValue = pre + f(to * e) + post; if (k < 1) requestAnimationFrame(st); else n.nodeValue = el.dataset.orig; };
    requestAnimationFrame(st);
  });
}
function show(n) {
  i = Math.max(0, Math.min(slides.length - 1, n));
  slides.forEach((s, j) => { s.classList.toggle("on", j === i); s.classList.toggle("past", j < i); });
  [...$("dots").children].forEach((d, j) => d.classList.toggle("on", j === i));
  $("bar").style.width = ((i + 1) / slides.length * 100) + "%";
  $("notes").textContent = slides[i].dataset.notes || "";
  try { history.replaceState(null, "", "#" + (i + 1)); } catch {}
  countUp(slides[i]);
}
slides.forEach((s, j) => { const d = document.createElement("i"); d.onclick = () => show(j); $("dots").appendChild(d); });
addEventListener("keydown", (e) => {
  if (["ArrowRight", "PageDown", " "].includes(e.key)) { e.preventDefault(); show(i + 1); }
  else if (["ArrowLeft", "PageUp"].includes(e.key)) { e.preventDefault(); show(i - 1); }
  else if (/^n$/i.test(e.key)) $("notes").hidden = !$("notes").hidden;
  else if (/^f$/i.test(e.key)) fs();
});
let tx = null; addEventListener("touchstart", (e) => (tx = e.touches[0].clientX)); addEventListener("touchend", (e) => { if (tx == null) return; const d = e.changedTouches[0].clientX - tx; if (Math.abs(d) > 50) show(i + (d < 0 ? 1 : -1)); tx = null; });
function fs() { const d = document.documentElement; if (!document.fullscreenElement) d.requestFullscreen?.().catch(() => {}); else document.exitFullscreen(); }
$("prev").onclick = () => show(i - 1); $("next").onclick = () => show(i + 1); $("fs").onclick = fs;
addEventListener("resize", fit); fit();
show((parseInt(location.hash.slice(1)) || 1) - 1);
"""

html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paytm Kaasu · Pitch</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&family=Anek+Tamil:wght@500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="bar" id="bar"></div>
<div class="stage"><div class="deck" id="deck">
{"".join(slides)}</div></div>
<div class="hud"><span>← → keys · N notes · F full screen</span><div class="dots" id="dots"></div><div style="display:flex;gap:6px"><button id="prev" type="button">Back</button><button id="next" type="button">Next</button><button id="fs" type="button">Full screen</button></div></div>
<div class="notes" id="notes" hidden></div>
<script>{JS}</script>
</body>
</html>'''
open(OUT, "w", encoding="utf-8").write(html)
print("slides:", len(slides))
