"""Rebuild the deck in a bento layout (rounded tile grids, light titles, big numbers, numbered lists, timeline)
in Paytm colours, with the full research A to Z. Keeps the existing HUD and interactive script."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(ROOT, "public", "deck", "index.html")
old = open(os.path.join(ROOT, "backup", "deck-v1.html"), encoding="utf-8").read()
tail = old[old.index('<div class="hud">'):]   # HUD, notes, lightbox, script (unchanged ids)
JS_HELPERS = r'''
// ---- motion helpers ----
const STAG = ".c, .mx tbody tr, .num-list > div, .stack > div, .tag, .leg > div";
slides.forEach((s) => {
  let k = 0; s.querySelectorAll(STAG).forEach((el) => { if (el.closest(".lb")) return; el.classList.add("st"); el.style.setProperty("--i", k++); });
  s.querySelectorAll(".bar").forEach((el, j) => el.style.setProperty("--i", j));
  s.querySelectorAll(".tl-node").forEach((el, j) => el.style.setProperty("--i", j));
  s.querySelectorAll(".logo-c").forEach((el, j) => el.style.setProperty("--i", j));
  s.querySelectorAll(".big:not([data-count])").forEach((el) => { const n = el.firstChild; if (n && n.nodeType === 3) el.dataset.orig = n.nodeValue; });
});
function countUp(s) {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  s.querySelectorAll(".big[data-orig]").forEach((el) => {
    const m = el.dataset.orig.match(/^([^\d]*)([\d][\d,]*\.?\d*)(.*)$/); if (!m) return;
    const [, pre, num, post] = m, dec = (num.split(".")[1] || "").length, comma = num.includes(","), to = parseFloat(num.replace(/,/g, ""));
    const node = el.firstChild, t0 = performance.now(), dur = 1100;
    const fmt = (v) => comma ? Math.round(v).toLocaleString("en-IN") : v.toFixed(dec);
    const st = (t) => { const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3); node.nodeValue = pre + fmt(to * e) + post; if (k < 1) requestAnimationFrame(st); else node.nodeValue = el.dataset.orig; };
    requestAnimationFrame(st);
  });
}
'''
tail = tail.replace("function show(n) {", JS_HELPERS + chr(10) + "function show(n) {", 1)
tail = tail.replace('$("reloadDemo").onclick', 'if ($("reloadDemo")) $("reloadDemo").onclick', 1)
tail = tail.replace("// the pot fills, from the same cash engine as the app", "try { // the pot fills, from the same cash engine as the app", 1)
tail = tail.replace("show((parseInt(", "} catch (e) {}" + chr(10) + "show((parseInt(", 1).replace("  const s = slides[i];", "  const s = slides[i]; countUp(s);", 1)

CSS = r"""
:root {
  --navy: #012b72; --navy-2: #0c3b8f; --navy-3: #1a4ea6; --sky: #00baf2; --sky-2: #59d2f7; --pale: #d6f1fc; --mist: #f1f8fc; --line: #dfe8f1;
  --ink: #0b1630; --ink-2: #44506a; --muted: #7d889e; --green: #0f9d6e; --red: #e0345c; --gold: #f0a21c;
  --font: "Inter", -apple-system, "Segoe UI", Arial, sans-serif; --tamil: "Anek Tamil", sans-serif; --ease: cubic-bezier(.22, 1, .36, 1); color-scheme: light;
}
* { box-sizing: border-box; }
[hidden] { display: none !important; }
html, body { margin: 0; height: 100%; overflow: hidden; background: #d9ebf6; font-family: var(--font); color: var(--ink); -webkit-font-smoothing: antialiased; letter-spacing: -.01em; }
button { font: inherit; cursor: pointer; transition: transform .18s var(--ease), background-color .2s, box-shadow .25s, opacity .2s; }
button:not(:disabled):active { transform: scale(.96); }
button:focus-visible { outline: 2px solid var(--sky); outline-offset: 3px; }
.ta { font-family: var(--tamil); letter-spacing: 0; }
.stage { position: fixed; inset: 0; display: grid; place-items: center; }
.deck { position: relative; width: 1280px; height: 720px; transform-origin: center; counter-reset: sl; }
.s { position: absolute; inset: 0; border-radius: 8px; overflow: hidden; background: var(--mist); box-shadow: 0 30px 80px -30px rgba(1,43,114,.45); opacity: 0; visibility: hidden; transform: scale(1.015); transition: opacity .6s var(--ease), transform .8s var(--ease), visibility 0s .6s; counter-increment: sl; }
.s::after { content: counter(sl, decimal-leading-zero); position: absolute; right: 26px; bottom: 16px; font-size: 11px; font-weight: 600; color: var(--muted); letter-spacing: .08em; }
.s.dark { background: var(--navy); color: #fff; } .s.dark::after { color: rgba(255,255,255,.45); }
.s.on { opacity: 1; visibility: visible; transform: none; transition: opacity .6s var(--ease), transform .8s var(--ease), visibility 0s; }
.s.past { transform: scale(.99); }
.in { position: absolute; inset: 0; padding: 46px 56px; }
.s .a { opacity: 0; transform: translateY(18px); }
.s.on .a { animation: up .85s var(--ease) both; }
.s.on .d1 { animation-delay: .1s; } .s.on .d2 { animation-delay: .2s; } .s.on .d3 { animation-delay: .3s; } .s.on .d4 { animation-delay: .4s; } .s.on .d5 { animation-delay: .5s; } .s.on .d6 { animation-delay: .6s; }
@keyframes up { to { opacity: 1; transform: none; } }
.s.on .float { animation: up .85s var(--ease) both, float 6s 1s ease-in-out infinite; }
@keyframes float { 0%, 100% { translate: 0 0; } 50% { translate: 0 -8px; } }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation-duration: .01ms !important; animation-delay: 0s !important; transition-duration: .01ms !important; } .s .a { opacity: 1; transform: none; } }

/* type */
.t { font-size: 44px; line-height: 1.08; font-weight: 400; letter-spacing: -.03em; color: var(--navy); margin: 0; text-wrap: balance; }
.dark .t, .c-navy .t, .c-mid .t { color: #fff; }
.t.xl { font-size: 78px; letter-spacing: -.045em; line-height: 1; }
.t.sm { font-size: 34px; }
.eb { font-size: 12px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--sky); margin-bottom: 10px; }
.dark .eb { color: var(--sky-2); }
.p { font-size: 14.5px; line-height: 1.55; color: var(--ink-2); margin: 0; }
.dark .p, .c-navy .p, .c-mid .p { color: rgba(255,255,255,.72); }
.c-sky .p { color: rgba(255,255,255,.9); }
.mini { font-size: 12px; line-height: 1.4; color: var(--muted); }
.dark .mini, .c-navy .mini, .c-mid .mini { color: rgba(255,255,255,.55); } .c-sky .mini { color: rgba(255,255,255,.85); }
.big { font-size: 46px; font-weight: 400; letter-spacing: -.04em; line-height: 1; font-variant-numeric: tabular-nums; }
.big small { font-size: 20px; letter-spacing: -.02em; margin-left: 3px; }
.lbl { font-size: 13.5px; font-weight: 600; margin-top: 8px; line-height: 1.3; }
hr.rule { border: 0; border-top: 1px solid rgba(255,255,255,.18); margin: 18px 0; }
.lt hr.rule, hr.rule.lt { border-top-color: var(--line); }

/* cards */
.c { border-radius: 18px; padding: 22px; position: relative; overflow: hidden; }
.c-navy { background: var(--navy); color: #fff; }
.c-mid { background: var(--navy-2); color: #fff; }
.c-sky { background: var(--sky); color: #fff; }
.c-pale { background: var(--pale); color: var(--navy); }
.c-white { background: #fff; color: var(--ink); box-shadow: 0 0 0 1px var(--line); }
.c-glass { background: rgba(255,255,255,.08); color: #fff; box-shadow: inset 0 0 0 1px rgba(255,255,255,.12); }
.c-img { background: linear-gradient(160deg, #e6f6fd, #bfe9fb); padding: 0; }
.dark .c-img { background: linear-gradient(160deg, #1a4ea6, #0c3b8f); }
.c-img img { display: block; }
.crop { overflow: hidden; border-radius: 14px; }
.crop img { width: 100%; display: block; }
.grid { display: grid; gap: 14px; }
.ab { position: absolute; }
.tag { display: inline-flex; align-items: center; gap: 6px; font-size: 11.5px; font-weight: 700; padding: 5px 10px; border-radius: 99px; background: var(--pale); color: var(--navy); }
.dark .tag, .c-navy .tag { background: rgba(255,255,255,.12); color: #fff; }
.tag.sky { background: var(--sky); color: #fff; } .tag.green { background: #dff5ec; color: var(--green); } .tag.amber { background: #fff1d6; color: #9a5b00; } .tag.red { background: #fde6ec; color: var(--red); }
.num-list { display: grid; grid-template-columns: 1fr 1fr; }
.num-list > div { display: grid; grid-template-columns: 74px 1fr; gap: 14px; padding: 22px 26px 22px 0; border-top: 1px solid rgba(255,255,255,.16); }
.num-list > div:nth-child(odd) { border-right: 1px solid rgba(255,255,255,.16); }
.num-list > div:nth-child(even) { padding-left: 30px; }
.num-list .n { font-size: 48px; font-weight: 300; letter-spacing: -.04em; line-height: .95; color: var(--sky-2); }
.num-list b { font-size: 17px; font-weight: 600; display: block; margin-bottom: 6px; }
.bar { height: 54px; border-radius: 12px; display: flex; align-items: center; justify-content: space-between; padding: 0 18px; color: #fff; font-size: 13.5px; font-weight: 600; }
.bar b { font-size: 22px; font-weight: 500; letter-spacing: -.02em; }
.stack > div { border-radius: 14px; padding: 14px 18px; display: flex; justify-content: space-between; align-items: center; gap: 14px; }
.stack b { font-size: 15.5px; } .stack .mini { margin-top: 2px; }
.stack .v { font-size: 24px; font-weight: 500; letter-spacing: -.02em; white-space: nowrap; }
.logo-w { display: flex; align-items: center; gap: 12px; height: 26px; color: #fff; font-weight: 700; font-size: 20px; letter-spacing: -.02em; }
.logo-w img { height: 100%; } .logo-w i { width: 1px; height: 20px; background: rgba(255,255,255,.4); }
.logo-w.navy { color: var(--navy); } .logo-w.navy i { background: rgba(1,43,114,.3); }
.phone { filter: drop-shadow(0 22px 30px rgba(1,43,114,.28)); }
.zoom { cursor: zoom-in; transition: transform .35s var(--ease); }
.zoom:hover { transform: translateY(-4px) scale(1.02); }
.bubble { background: #fff; color: var(--ink); border-radius: 18px; padding: 14px 18px; box-shadow: 0 18px 40px -18px rgba(1,43,114,.45); font-size: 17px; line-height: 1.4; font-weight: 600; }
.bubble small { display: block; font-size: 13px; color: var(--muted); font-weight: 500; margin-top: 6px; font-family: var(--font); }
.chip { border: 0; border-radius: 99px; padding: 9px 16px; font-size: 14.5px; font-weight: 700; background: rgba(255,255,255,.12); color: #fff; }
.chip.on { background: var(--sky); color: #fff; }
.btn { border: 0; border-radius: 14px; background: var(--sky); color: #fff; font-weight: 700; font-size: 15.5px; padding: 13px 20px; box-shadow: 0 14px 30px -14px rgba(0,186,242,.8); }
.btn:disabled { background: var(--green); box-shadow: none; }
.btn.navy { background: var(--navy); box-shadow: none; }
.leg { display: grid; gap: 12px; }
.leg div { display: grid; grid-template-columns: 16px 1fr auto; gap: 12px; align-items: center; font-size: 15px; font-weight: 500; }
.leg i { width: 16px; height: 16px; border-radius: 5px; } .leg b { font-variant-numeric: tabular-nums; font-size: 17px; font-weight: 600; }
#jarFill rect { transition: y .9s var(--ease), height .9s var(--ease); }
.rain { position: absolute; inset: 0; pointer-events: none; opacity: 0; transition: opacity .8s; z-index: 0; }
.rain.on { opacity: 1; }
.rain i { position: absolute; top: -20px; width: 2px; height: 18px; border-radius: 2px; background: linear-gradient(#9fdcff, rgba(159,220,255,0)); animation: drop .9s linear infinite; }
@keyframes drop { to { transform: translateY(760px); } }
#rainSteps > div { transition: opacity .5s, background-color .5s; }
.flow { stroke-dasharray: 2 10; animation: dash 1.1s linear infinite; }
@keyframes dash { to { stroke-dashoffset: -24; } }
.lb { position: fixed; inset: 0; background: rgba(5,20,50,.8); backdrop-filter: blur(6px); display: grid; place-items: center; z-index: 20; cursor: zoom-out; }
.lb img { height: 86vh; filter: drop-shadow(0 30px 60px rgba(0,0,0,.5)); animation: up .5s var(--ease) both; }
.frame { position: absolute; left: 56px; right: 56px; top: 132px; bottom: 40px; border-radius: 18px; overflow: hidden; background: #f2f3f6; box-shadow: 0 0 0 1px var(--line); }
.frame iframe { position: absolute; left: 0; top: 0; width: 1520px; height: 840px; border: 0; transform: scale(.769); transform-origin: 0 0; }
.hud { position: fixed; left: 0; right: 0; bottom: 0; display: flex; align-items: center; justify-content: space-between; padding: 10px 18px; color: #4a5a78; font-size: 12.5px; z-index: 10; }
.hud .bar { position: fixed; left: 0; top: 0; height: 3px; padding: 0; border-radius: 0; background: var(--sky); transition: width .5s var(--ease); }
.hud button { border: 0; background: rgba(1,43,114,.1); color: var(--navy); border-radius: 10px; padding: 7px 12px; font-size: 13px; font-weight: 600; }
.dots { display: flex; gap: 5px; } .dots i { width: 6px; height: 6px; border-radius: 50%; background: rgba(1,43,114,.2); cursor: pointer; transition: width .3s var(--ease), background .3s; }
.dots i.on { width: 20px; border-radius: 4px; background: var(--sky); }
.notes { position: fixed; right: 16px; top: 16px; width: 340px; background: rgba(1,27,72,.95); color: #e6ecff; border-radius: 16px; padding: 14px 16px; font-size: 14px; line-height: 1.5; z-index: 11; }
.logo-tile { height: 58px; border-radius: 12px; background: rgba(255,255,255,.07); display: grid; place-items: center; padding: 0 12px; box-shadow: inset 0 0 0 1px rgba(255,255,255,.1); }
.logo-tile img { max-height: 24px; max-width: 100%; object-fit: contain; }
.mx { width: 100%; border-collapse: separate; border-spacing: 0; font-size: 14px; background: #fff; border-radius: 18px; box-shadow: 0 0 0 1px var(--line); overflow: hidden; }
.mx th { font-size: 11px; text-transform: uppercase; letter-spacing: .08em; color: var(--muted); font-weight: 700; text-align: center; padding: 12px 8px; background: #f6f9fc; }
.mx th:first-child, .mx td:first-child { text-align: left; padding-left: 20px; }
.mx td { padding: 9px 8px; border-top: 1px solid #eef2f7; text-align: center; font-weight: 600; color: var(--ink); }
.mx td small { display: block; font-size: 11.5px; color: var(--muted); font-weight: 500; }
.mx tr.us td { background: var(--navy); color: #fff; } .mx tr.us td small { color: rgba(255,255,255,.65); }
.mx.score td { font-variant-numeric: tabular-nums; }
.dot { display: inline-block; width: 15px; height: 15px; border-radius: 50%; vertical-align: -3px; }
.dot.y { background: var(--green); } .dot.p { background: linear-gradient(90deg, var(--gold) 50%, #e3e9f1 50%); } .dot.n { box-shadow: inset 0 0 0 2px #cfd8e4; }
.mx tr.us .dot.y { background: var(--sky); box-shadow: 0 0 0 3px rgba(0,186,242,.3); }
.tl-line { position: absolute; left: 56px; right: 56px; height: 0; border-top: 2px dashed #9fc6e3; }
.tl-node { position: absolute; width: 38px; height: 38px; border-radius: 50%; background: #fff; box-shadow: 0 0 0 2px var(--navy); display: grid; place-items: center; color: var(--navy); font-size: 13px; font-weight: 800; transform: translate(-50%, -50%); }
.tl-node.on { background: var(--sky); color: #fff; box-shadow: 0 0 0 6px rgba(0,186,242,.2); }
.src-list { columns: 2; column-gap: 36px; font-size: 12.5px; line-height: 1.45; color: var(--ink-2); }
.src-list div { break-inside: avoid; margin-bottom: 8px; } .src-list b { color: var(--navy); }
.dark .c-pale .t, .dark .c-white .t { color: var(--navy); }
.dark .c-pale .p, .dark .c-white .p { color: var(--ink-2); }
.dark .c-pale .mini, .dark .c-white .mini { color: var(--muted); }
.dark .c-pale .eb, .dark .c-white .eb { color: #0089c2; }

/* ---- motion: smooth, staggered, Apple-like ---- */
.s { transform: translateX(28px) scale(.985); transition: opacity .75s var(--ease), transform 1s var(--ease), visibility 0s .75s; }
.s.on { transform: none; }
.s.past { transform: translateX(-28px) scale(.985); }
.s .a { transform: translateY(16px); filter: blur(4px); }
.s.on .a { animation: up .9s var(--ease) both; }
@keyframes up { from { opacity: 0; transform: translateY(16px); filter: blur(4px); } to { opacity: 1; transform: none; filter: none; } }
.s .st { opacity: 0; }
.s.on .st { animation: rise .8s var(--ease) both; animation-delay: calc(.18s + var(--i, 0) * 60ms); }
@keyframes rise { from { opacity: 0; transform: translateY(14px) scale(.98); filter: blur(3px); } to { opacity: 1; transform: none; filter: none; } }
.s.on .st.a { filter: none; }
.s.on .bar { animation: grow 1.1s var(--ease) both; animation-delay: calc(.3s + var(--i, 0) * 90ms); transform-origin: left center; }
@keyframes grow { from { transform: scaleX(0); opacity: .3; } to { transform: none; opacity: 1; } }
.s.on .tl-line { animation: draw 1.4s var(--ease) both .2s; transform-origin: left center; }
@keyframes draw { from { transform: scaleX(0); } to { transform: none; } }
.s.on .tl-node { animation: pop .6s cubic-bezier(.34,1.56,.64,1) both; animation-delay: calc(.4s + var(--i, 0) * 250ms); }
@keyframes pop { from { opacity: 0; transform: translate(-50%, -50%) scale(.3); } to { opacity: 1; transform: translate(-50%, -50%); } }
.c { transition: transform .45s var(--ease), box-shadow .45s var(--ease); }
.c:hover { transform: translateY(-3px); box-shadow: 0 18px 40px -22px rgba(1,43,114,.45); }
.c-white:hover { box-shadow: 0 0 0 1px var(--line), 0 18px 40px -22px rgba(1,43,114,.35); }
.mx tbody tr { transition: background-color .3s; }
.mx tbody tr:not(.us):hover td { background: #f3f9fd; }
@media (prefers-reduced-motion: reduce) { .s, .s.past { transform: none; } .s .a, .s .st { filter: none; opacity: 1; transform: none; } }
.logo-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; margin-top: 4px; }
.logo-c { height: 74px; border-radius: 14px; background: var(--mist); display: grid; place-items: center; padding: 0 14px; transition: transform .45s var(--ease), background-color .3s, box-shadow .45s var(--ease); }
.logo-c.wide { grid-column: span 2; } .logo-c.wide img { max-height: 26px; }
.logo-c img[alt=JWIL] { max-height: 46px; }
.logo-c img { max-height: 32px; max-width: 100%; object-fit: contain; transition: transform .45s var(--ease); }
.logo-c:hover { background: #fff; box-shadow: 0 0 0 1px var(--line), 0 14px 30px -18px rgba(1,43,114,.4); transform: translateY(-3px); }
.logo-c:hover img { transform: scale(1.06); }
.s.on .logo-c { animation: logoIn .7s var(--ease) both; animation-delay: calc(.35s + var(--i, 0) * 55ms); }
@keyframes logoIn { from { opacity: 0; transform: translateY(12px) scale(.92); filter: blur(3px); } to { opacity: 1; transform: none; filter: none; } }
.ic { width: 40px; height: 40px; border-radius: 12px; display: grid; place-items: center; }
.ic svg { width: 21px; height: 21px; }
"""

# small icon set (line icons, 24px grid)
def ic(paths, bg="var(--pale)", fg="var(--navy)"):
    return f'<span class="ic" style="background:{bg};color:{fg}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{paths}</svg></span>'
I = {
 "cal": '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4"/>',
 "home": '<path d="m3 10 9-7 9 7v10a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
 "book": '<path d="M4 19.5V5a2 2 0 0 1 2-2h14v16H6.5A2.5 2.5 0 0 0 4 21.5z"/><path d="M8 7h8M8 11h6"/>',
 "bank": '<path d="M3 10 12 4l9 6M5 10v8M9 10v8M15 10v8M19 10v8M3 20h18"/>',
 "mic": '<rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10v1a7 7 0 0 0 14 0v-1M12 18v4"/>',
 "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
 "cloud": '<path d="M7 18a4 4 0 0 1-.5-8A6 6 0 0 1 18 9a4.5 4.5 0 0 1-1 9z"/>',
 "check": '<path d="m5 12 5 5L20 7"/>',
 "spark": '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
 "shield": '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/>',
 "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-3.5 3-6 7-6s7 2.5 7 6M16 4a3.5 3.5 0 0 1 0 7M18 14c2.5.7 4 2.8 4 6"/>',
 "phone": '<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/>',
 "rupee": '<path d="M7 4h10M7 9h10M7 4c6 0 6 10 0 10l8 6"/>',
 "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
}

def S(cls, notes, body):
    return f'<section class="s {cls}" data-notes="{notes}"><div class="in">{body}</div></section>\n'

def stat(cls, big, unit, lbl, src, extra=""):
    u = f"<small>{unit}</small>" if unit else ""
    return f'<div class="c {cls}" {extra}><div class="big">{big}{u}</div><div class="lbl">{lbl}</div><div class="mini" style="margin-top:4px">{src}</div></div>'

LOGOS = [("bajajfinance.svg", "Bajaj Finance"), ("nuvama.png", "Nuvama"), ("maxiom.svg", "Maxiom Wealth"), ("turtlemint.png", "Turtlemint"), ("finfinity.svg", "Finfinity"),
         ("mstock.svg", "mStock"), ("ltimindtree.svg", "LTIMindtree"), ("medanta.svg", "Medanta"), ("yamaha.png", "Yamaha"), ("royalenfield.png", "Royal Enfield"),
         ("acquire.svg", "Acquire"), ("tracebale.png", "TraceBale"), ("jwil.png", "JWIL")]

Y, PA, N = '<i class="dot y" title="Yes"></i>', '<i class="dot p" title="Partly"></i>', '<i class="dot n" title="Not found"></i>'
def mrow(name, sub, cells, us=False):
    return f'<tr{" class=us" if us else ""}><td>{name}<small>{sub}</small></td>' + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"

sl = []
# ---------------------------------------------------------------- 1 COVER
sl.append(S("dark", "Hi, I'm Dheena. This is Kaasu: every shop's cash, planned.", f'''
<div class="logo-w a"><img src="/brand/paytm-logo-white.svg" alt="Paytm"><i></i>Kaasu</div>
<div class="ab a" style="right:56px;top:42px;font-size:28px;font-weight:300;letter-spacing:-.02em">2026</div>
<div class="ab" style="left:56px;top:250px;width:600px">
  <div class="eb a d1">Paytm Buildathon · Chennai · Track 1</div>
  <h1 class="t xl a d2">Every shop's cash, planned.</h1>
  <div class="a d3" style="margin-top:20px;font-size:16px;color:rgba(255,255,255,.75)">Savings · Udhaar · Smart loans · On the Soundbox</div>
</div>
<div class="c c-img ab a d2" style="right:56px;top:96px;width:520px;height:470px;background:radial-gradient(circle at 50% 42%,#1f62c2,#0c3b8f 70%)">
  <img class="float" src="img/coin.svg" alt="Gold rupee coin" style="position:absolute;left:30px;top:20px;width:460px">
  <div class="c c-sky ab" style="left:20px;bottom:20px;right:20px;padding:16px 20px;display:flex;justify-content:space-between;align-items:center"><span style="font-weight:600;font-size:15px">Kaasu means money</span><span class="ta" style="font-size:17px;font-weight:600">காசு</span></div>
</div>
<div class="ab a d4" style="left:56px;bottom:46px;display:flex;gap:40px;font-size:13px;color:rgba(255,255,255,.7)">
  <div>Presenter<br><b style="color:#fff;font-size:14.5px">Dheena Dhayalan R</b></div>
  <div>Forward Deployed Designer<br><img src="/brand/rps-logo-white.svg" alt="Rock Paper Scissors" style="height:15px;margin-top:5px"></div>
</div>'''))

# ---------------------------------------------------------------- 2 ME
WIDE = {"bajajfinance.svg", "royalenfield.png"}
logos = "".join(f'<div class="logo-c{" wide" if f in WIDE else ""}"><img src="logos/c/{f}" alt="{a}"></div>' for f, a in LOGOS)
proj = [("nuvama.png", "Wealth platform", "Web app + design system"), ("maxiom.svg", "AI wealth app", "50% fewer steps"), ("turtlemint.png", "Insurance app", "Buy, renew, claim"), ("finfinity.svg", "Lending fintech", "Brand + web app")]
sl.append(S("", "Ten seconds. Engineer by training, 8 patents, designer at a fintech design agency.", f'''
<div class="grid" style="grid-template-columns:400px 1fr;gap:16px;height:100%">
  <div class="grid" style="grid-template-rows:auto 1fr;gap:14px">
    <div class="c c-pale a" style="padding:28px">
      <div class="eb">Hi, I'm</div>
      <h2 class="t" style="font-size:42px">Dheena Dhayalan R</h2>
      <p class="p" style="margin-top:12px;font-size:15px">Engineering graduate. Forward Deployed Designer at Rock Paper Scissors, a fintech design agency.</p>
      <img src="/brand/rps-logo-black.svg" alt="Rock Paper Scissors" style="height:17px;margin-top:18px">
    </div>
    <div class="grid" style="grid-template-columns:1fr 1fr;gap:14px">
      <div class="c c-navy"><div class="big">8</div><div class="lbl">Patents in engineering</div></div>
      <div class="c c-sky"><div class="big">₹25<small>L+</small></div><div class="lbl">Won for IEEE projects</div></div>
      <div class="c c-white"><div class="big" style="font-size:30px;color:var(--navy)">Elsevier</div><div class="lbl">Research book chapter</div><div class="mini">MIT Square</div></div>
      <div class="c c-white"><div class="big" style="font-size:30px;color:var(--navy)">Hackathons</div><div class="lbl">Winner, several times</div></div>
    </div>
  </div>
  <div class="c c-white a d1" style="padding:26px;display:flex;flex-direction:column">
    <div class="eb">Fintech and brand teams we design for</div>
    <div class="logo-grid">{logos}</div>
    <hr class="rule lt">
    <div class="grid" style="grid-template-columns:repeat(4,1fr);gap:10px;margin-top:auto">
      {"".join(f'<div class="c c-pale" style="padding:14px"><img src="logos/c/{f}" alt="" style="height:18px;max-width:100%;object-fit:contain;object-position:left"><div class="lbl">{a}</div><div class="mini">{b}</div></div>' for f, a, b in proj)}
    </div>
  </div>
</div>'''))

# ---------------------------------------------------------------- 3 MEET MURUGAN (exec-summary style)
sl.append(S("dark", "Read the Tamil line slowly. Then the English.", f'''
<div class="c c-img ab a" style="left:56px;top:46px;right:56px;bottom:150px;background:linear-gradient(120deg,#0c3b8f,#1f62c2 60%,#00baf2)">
  <img class="float" src="img/soundbox.png" alt="Paytm Soundbox on Murugan's counter" style="position:absolute;right:90px;top:30px;height:380px">
  <div class="bubble ab" style="right:330px;top:50px;max-width:360px"><span class="ta">"வியாபாரம் நல்லா இருக்கு. ஆனா தேவைப்படும் நாள்ல பணம் இல்ல."</span><small>"Business is good. The money isn't there on the day I need it."</small></div>
</div>
<div class="c c-pale ab a d1" style="left:84px;top:84px;width:380px;padding:28px">
  <div class="eb">Meet our user</div>
  <h2 class="t" style="font-size:40px">Murugan, Murugan Stores</h2>
  <p class="p" style="margin-top:14px">Velachery, Chennai. Paytm QR and Soundbox on the counter. Regulars buy on udhaar. He sells well, yet runs out of cash on the days that matter.</p>
</div>
<div class="ab a d2" style="left:56px;right:56px;bottom:40px;display:grid;grid-template-columns:repeat(4,1fr);gap:24px">
  <div><div class="big" style="font-size:40px">₹11,240</div><div class="mini">Sales a day</div></div>
  <div><div class="big" style="font-size:40px">₹80,000</div><div class="mini" style="color:rgba(255,255,255,.8)">Pongal stock due 6 Jan</div></div>
  <div><div class="big" style="font-size:40px;color:#ff8aa6">−₹32,520</div><div class="mini">Short at today's pace</div></div>
  <div><div class="big" style="font-size:40px">53 days</div><div class="mini">To fix it</div></div>
</div>'''))

# ---------------------------------------------------------------- 4 COUNTDOWN
pots = open(os.path.join(ROOT, "backup", "deck-v1.html"), encoding="utf-8").read()
pot_svg = re.search(r'<svg class="a d2" viewBox="0 0 1140 400".*?</svg>', pots, re.S).group(0)
pot_svg = pot_svg.replace('class="a d2" viewBox="0 0 1140 400" style="position:absolute;left:70px;top:220px;width:1140px"', 'viewBox="0 0 1140 400" style="width:100%"')
sl.append(S("", "Point at the two pots. The gap is the whole problem.", f'''
<div class="grid" style="grid-template-columns:330px 1fr;gap:16px;height:100%">
  <div class="c c-navy a" style="padding:30px;display:flex;flex-direction:column">
    <div class="eb">The problem</div>
    <h2 class="t">On 6 January, the pot won't be full.</h2>
    <p class="p" style="margin-top:16px">Pongal stock is paid upfront. At today's pace Murugan has ₹47,480 of the ₹80,000 he needs.</p>
    <div style="margin-top:auto"><div class="big" style="color:#ff8aa6">−₹32,520</div><div class="mini" style="margin-top:6px">Shortfall in 53 days</div></div>
  </div>
  <div class="c c-white a d1" style="display:grid;place-items:center">{pot_svg}</div>
</div>'''))

# ---------------------------------------------------------------- 5 KEY CHALLENGES
sl.append(S("dark", "Four reasons, all about timing, not sales.", f'''
<div class="eb a">Why it happens</div>
<h2 class="t a d1" style="max-width:700px">Key challenges: not low sales, bad timing.</h2>
<hr class="rule a d1" style="margin:30px 0 0">
<div class="num-list a d2">
  <div><span class="n">01</span><div><b>Festivals come early</b><p class="p">Pongal and Diwali stock is paid weeks before the sales arrive.</p></div></div>
  <div><span class="n">02</span><div><b>Profit goes home</b><p class="p">Every Sunday the family takes the week's profit, before the big bill comes.</p></div></div>
  <div><span class="n">03</span><div><b>Udhaar stays unpaid</b><p class="p">He won't chase regulars. Customers "might get offended and move to another store".</p></div></div>
  <div><span class="n">04</span><div><b>Credit comes late and costly</b><p class="p">Only 14% of MSMEs reach formal credit, so the gap is filled in a panic.</p></div></div>
</div>'''))

# ---------------------------------------------------------------- 6 RESEARCH: MARKET (industry overview bento)
sl.append(S("", "Research 1. The market is huge and already digital. Paytm already owns the counter.", f'''
<div class="grid" style="grid-template-columns:1.1fr 1fr 1fr 1.2fr;grid-template-rows:1fr 1fr 1fr;gap:14px;height:100%">
  <div class="c c-navy a" style="grid-column:1/3;padding:24px 26px"><div class="eb">Research 01 · Market</div><h2 class="t" style="font-size:38px">The counter is already Paytm's.</h2></div>
  {stat("c-sky a d1", "1.64", " Cr", "Soundboxes on counters", "Paytm Q2 FY27 · +27 lakh in a year")}
  <div class="c c-img a d2" style="grid-column:4;grid-row:1/3;display:grid;place-items:center"><img src="img/soundbox.png" alt="Paytm Soundbox" style="height:300px"></div>
  {stat("c-white a d2", "4.9", " Cr", "Registered Paytm merchants", "Paytm Q4 FY26")}
  {stat("c-pale a d2", "₹7.1", " lakh cr", "Merchant payments in a quarter", "Paytm GMV Q2 FY27 · +26%")}
  {stat("c-navy a d3", "91%", "", "Of grocery still sold by kiranas", "Redseer estimate, 2025")}
  {stat("c-white a d3", "20.7", " bn", "UPI payments in one month", "NPCI via Inc42, Oct 2025")}
  {stat("c-pale a d4", "85%", "", "Of merchant loans went to device owners", "Reported, Q2 FY26")}
  {stat("c-white a d4", "50%+", "", "Merchant loans to repeat borrowers", "Paytm, Q2 FY26")}
  <div class="c c-sky a d5"><div class="lbl" style="margin-top:0;font-size:15px">The device is the relationship.</div><div class="mini" style="margin-top:6px">So the money brain should live on the device.</div></div>
</div>'''))

# ---------------------------------------------------------------- 7 RESEARCH: PAIN (bars)
bars = [("82%", "Buyers moved ¼ of kirana shopping to quick commerce", "Datum Intelligence", "#1F5FD1", 82),
        ("52%", "Kiranas saw food and FMCG sales fall", "PwC × Kirana Club, 508 retailers", "#1F5FD1", 52),
        ("28%", "Fall in Tier 1 footfall", "Same survey", "#1F5FD1", 28),
        ("22%", "Kiranas plan any tech spend", "CPM India, 4,593 retailers", "#1F5FD1", 22),
        ("14%", "MSMEs reach formal credit", "2026 industry report", "#1F5FD1", 14)]
bar_html = "".join(f'<div class="a d{k+1}" data-tip="{l}: {v}" style="display:flex;align-items:center;gap:16px"><div class="bar" style="width:{w*0.55:.0f}%;min-width:76px;background:{c};justify-content:flex-end"><b>{v}</b></div><div><div style="font-size:14.5px;font-weight:600;color:var(--ink)">{l}</div><div class="mini">{s}</div></div></div>' for k, (v, l, s, c, w) in enumerate(bars))
sl.append(S("", "Research 2. Payments are solved. Money is not. These are surveys, not guesses.", f'''
<div class="grid" style="grid-template-columns:400px 1fr;gap:16px;height:100%">
  <div class="c c-navy a" style="padding:30px;display:flex;flex-direction:column">
    <div class="eb">Why it matters</div>
    <h2 class="t">Payments are solved. Money isn't.</h2>
    <p class="p" style="margin-top:16px">Quick commerce is taking regulars. Udhaar is cash they can't ask for. Stock and cash are managed by memory. Typing in Indian languages is hard; voice is natural.</p>
    <div class="grid" style="grid-template-columns:1fr 1fr;gap:12px;margin-top:auto">
      <div class="c c-mid" style="padding:16px"><div class="big" style="font-size:30px">₹25–30<small>L cr</small></div><div class="mini" style="margin-top:6px">MSME credit gap</div></div>
      <div class="c c-mid" style="padding:16px"><div class="big" style="font-size:30px">~2<small>lakh</small></div><div class="mini" style="margin-top:6px">Kiranas closed (AICPDF claim)</div></div>
    </div>
  </div>
  <div class="c c-white" style="padding:28px 30px;display:grid;gap:12px;align-content:center">
    <div class="eb a">Kirana surveys 2024–2026 · share of stores or buyers</div>{bar_html}
  </div>
</div>'''))

# ---------------------------------------------------------------- 8 RESEARCH: WHAT PAYTM ALREADY HAS
pt = [("AI Soundbox", "Oct 2025 · GFF", "Answers sales and collection questions in 11 languages.", "Don't build a Q&A bot. Build the action layer."),
      ("Merchant AI agents", "Roadmap", "CEO: agents as a small shop's COO, CFO, CMO. Subscription + inference fees.", "Kaasu is the CFO they announced."),
      ("Paytm Intelligence (Pi)", "Enterprise AI", "~4B parameter model tuned for Indian languages.", "Cheap Indian-language AI is a priority."),
      ("Internal AI agents", "Live", "Agents power merchant sales, service and loan collection.", "Paytm trusts agents for collections."),
      ("Payment Gateway + ChatGPT", "Sep 2026", "Online merchants track payments and insights in chat.", "Insights-in-chat is done. Action isn't."),
      ("Paytm Postpaid", "Relaunched Sep 2025", "Buy now, pay later with a lending partner.", "Bharosa routes trusted udhaar here.")]
cards = "".join(f'<div class="c {"c-navy" if k in (0,3) else "c-white" if k in (1,5) else "c-pale"} a d{k%5+1}" style="padding:20px"><div style="display:flex;justify-content:space-between;align-items:center"><b style="font-size:16.5px">{a}</b><span class="tag{" sky" if k in (0,3) else ""}">{b}</span></div><p class="p" style="margin-top:10px">{c}</p><hr class="rule{" lt" if k not in (0,3) else ""}" style="margin:12px 0"><div style="font-size:13.5px;font-weight:600;color:{"var(--sky-2)" if k in (0,3) else "var(--navy)"}">→ {d}</div></div>' for k, (a, b, c, d) in enumerate(pt))
sl.append(S("", "Research 3. What Paytm already ships, and what that means for us.", f'''
<div class="eb a">Research 03 · Paytm today</div>
<h2 class="t a d1">What Paytm already built for merchants.</h2>
<div class="grid" style="grid-template-columns:repeat(3,1fr);gap:14px;margin-top:26px">{cards}</div>'''))

# ---------------------------------------------------------------- 9 RESEARCH: COMPETITORS
matrix = "".join([
    mrow("Paytm AI Soundbox", "Sales and collections, 11 languages", [Y, N, N, N]),
    mrow("BharatPe assistant", "Gemini agent in the business app", [Y, PA, N, N]),
    mrow("PhonePe Business", "Payments, loans ₹50k–7L", [N, N, N, N]),
    mrow("OkCredit / Khatabook", "Udhaar ledgers, auto reminders", [N, PA, PA, N]),
    mrow("Reelo / LoyalStack", "Loyalty and win-back", [N, PA, Y, N]),
    mrow("Square · Shopify · Toast", "Managerbot, Sidekick, Toast IQ", [Y, Y, PA, N]),
    mrow("Pine Labs agents", "With Google Gemini, on POS", [Y, Y, PA, N]),
    mrow("KiranaPro Vani", "Pricing, inventory, demand", [Y, PA, N, N]),
    mrow("Paytm Kaasu", "On the Soundbox already on the counter", [Y, Y, Y, Y], us=True)])
sl.append(S("", "Research 4. Everyone answers. Few act. Nobody plans the shop's cash ahead on the counter.", f'''
<div class="grid" style="grid-template-columns:300px 1fr;gap:16px;height:100%">
  <div class="c c-sky a" style="padding:28px;display:flex;flex-direction:column">
    <div class="eb" style="color:#fff;opacity:.85">Research 04 · Competitors</div>
    <h2 class="t" style="color:#fff">Others answer. Kaasu plans ahead.</h2>
    <p class="p" style="margin-top:14px">The world moved from assistants that answer to agents that act. India's merchant apps are at step one.</p>
    <div class="mini" style="margin-top:auto;line-height:2">{Y} Yes &nbsp; {PA} Partly &nbsp; {N} Not found<br>Public sources, Nov 2026</div>
  </div>
  <div class="a d1" style="align-self:center"><table class="mx"><thead><tr><th>Player</th><th>Answers</th><th>Acts</th><th>Brings money in</th><th>Plans cash ahead, by voice</th></tr></thead><tbody>{matrix}</tbody></table></div>
</div>'''))

# ---------------------------------------------------------------- 10 RESEARCH: HACKATHON + PRIOR ART CHECK
newf = ["Pongal Fund", "Buy together", "Check a bill", "Save Score", "Rain Shield", "Payday udhaar"]
partly = [("Bharosa", "PhonePe Khata shows udhaar to customers; Paytm Postpaid pays shops", "New: per-entry confirm + udhaar takeover"),
          ("Staff advance", "Square, GajiGesa abroad", "New: voice request on Soundbox, from own savings"),
          ("Galla check", "POS cash-drawer tools", "New: spoken count, patterns not blame"),
          ("Gap-only planning", "Money SOS, Mumbai 2026 winner", "New: festival pot + udhaar + voice")]
sl.append(S("dark", "Research 5. We checked earlier Paytm hackathon entries and products before building. Be honest about prior art.", f'''
<div class="grid" style="grid-template-columns:1fr 1.25fr;gap:16px;height:100%">
  <div class="grid" style="grid-template-rows:auto 1fr;gap:14px">
    <div class="a"><div class="eb">Research 05 · Is it new?</div><h2 class="t">We checked before we built.</h2></div>
    <div class="grid" style="grid-template-columns:1fr 1fr;gap:14px">
      <div class="c c-sky a d1"><div class="big">12</div><div class="lbl">Earlier Paytm Build for India entries</div></div>
      <div class="c c-glass a d1"><div class="big">~45</div><div class="lbl">Product searches</div></div>
      <div class="c c-pale a d2" style="grid-column:1/3"><div class="eb">Not found anywhere · 15 Nov 2026</div><div style="display:flex;flex-wrap:wrap;gap:8px">{"".join(f'<span class="tag sky">{x}</span>' for x in newf)}</div></div>
    </div>
  </div>
  <div class="c c-glass a d2" style="padding:24px">
    <div class="eb">Partly exists · what we add</div>
    {"".join(f'<div style="display:grid;grid-template-columns:130px 1fr;gap:14px;padding:13px 0;border-top:1px solid rgba(255,255,255,.12)"><b style="font-size:15.5px">{a}</b><div><div class="p" style="font-size:13.5px">Exists: {b}</div><div style="font-size:13.5px;font-weight:600;color:var(--sky-2);margin-top:3px">{c}</div></div></div>' for a, b, c in partly)}
  </div>
</div>'''))

# ---------------------------------------------------------------- 11 RESEARCH: IDEAS SCORED
ideas = [("Cash-flow planning + gap-only loan → Kaasu", 5, 5, 5, 4), ("Proactive growth agent (win-back + udhaar)", 4, 5, 5, 4), ("Regulars win-back alone", 4, 5, 5, 4),
         ("Udhaar recovery alone", 4, 4, 4, 5), ("Voice-note orders to cart", 4, 4, 4, 3), ("Festival demand + restock", 3, 4, 3, 4),
         ("Shelf photo → ONDC catalogue", 3, 3, 3, 3), ("GST + bookkeeping", 2, 3, 3, 4), ("Sales Q&A chatbot on Soundbox", 1, 3, 4, 5)]
rows = "".join(f'<tr{" class=us" if k == 0 else ""}><td>{n}</td><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td><b>{a+b+c+d}</b></td></tr>' for k, (n, a, b, c, d) in enumerate(ideas))
sl.append(S("", "Research 6. Ten ideas scored honestly. A chatbot scores lowest because Paytm already has one.", f'''
<div class="grid" style="grid-template-columns:1fr 330px;gap:16px;height:100%">
  <div class="a d1" style="align-self:center"><table class="mx score"><thead><tr><th>Idea</th><th>Unique</th><th>Impact</th><th>Paytm fit</th><th>Feasible</th><th>/20</th></tr></thead><tbody>{rows}</tbody></table></div>
  <div class="c c-navy a" style="padding:28px;display:flex;flex-direction:column">
    <div class="eb">Research 06 · Opportunity map</div>
    <h2 class="t">Ten ideas, scored honestly.</h2>
    <p class="p" style="margin-top:14px">Each scored 1 to 5 on what judges value. Earlier we explored Munshi, a win-back agent. Deeper checks showed win-back and reminders already exist, so we moved to cash planning.</p>
    <div style="margin-top:auto"><div class="big">19<small>/20</small></div><div class="mini" style="margin-top:6px">Kaasu: unique, high impact, on Paytm's roadmap</div></div>
  </div>
</div>'''))

# ---------------------------------------------------------------- 12 RESEARCH: FEASIBILITY + RULES
feas = [("cloud", "Soundbox has its own 4G SIM", "Both box and app talk to Paytm servers on the same merchant account. Updates over the air."),
        ("mic", "Voice or button", "AI Soundbox listens. Older boxes have no mic, so the OK button says yes."),
        ("rupee", "Voice AI is affordable", "Indian-language voice agents start at about ₹1 a minute. Plain maths plans; AI only explains."),
        ("lock", "Money moves only with PIN", "Voice never moves money. Every loan shows a Key Fact Statement and asks consent."),
        ("users", "Reminders in Paytm's name", "Customers see Paytm, not the shop, so regulars aren't offended."),
        ("shield", "Within the rules", "Wage advance deductions within the Code on Wages 50% cap. Udhaar trail is alternate data with consent, not a bureau report.")]
sl.append(S("", "Research 7. Can it really ship? Yes, on what Paytm already runs.", f'''
<div class="eb a">Research 07 · Feasibility and compliance</div>
<h2 class="t a d1">Ships on what Paytm already runs.</h2>
<div class="grid" style="grid-template-columns:repeat(3,1fr);gap:14px;margin-top:26px">
{"".join(f'<div class="c {"c-white" if k%2==0 else "c-pale"} a d{k%5+1}" style="padding:22px">{ic(I[i], "var(--navy)" if k%2==0 else "#fff", "#fff" if k%2==0 else "var(--navy)")}<b style="display:block;font-size:16.5px;margin-top:16px;color:var(--navy)">{a}</b><p class="p" style="margin-top:6px">{b}</p></div>' for k, (i, a, b) in enumerate(feas))}
</div>'''))

# ---------------------------------------------------------------- 13 RESEARCH: SIZE + BUSINESS MODEL
sl.append(S("dark", "Research 8. Say the assumptions out loud. Judges respect that.", f'''
<div class="grid" style="grid-template-columns:1fr 1fr;gap:16px;height:100%">
  <div class="c c-mid a" style="padding:28px">
    <div class="eb">Research 08 · Size and money</div>
    <h2 class="t">Start with the Soundbox.</h2>
    <svg viewBox="0 0 420 300" style="width:100%;margin-top:18px" role="img" aria-label="4.9 crore merchants, 1.64 crore with a Soundbox, 10 lakh year-one goal">
      <circle cx="210" cy="160" r="138" fill="rgba(255,255,255,.08)" stroke="rgba(255,255,255,.2)"/>
      <circle cx="210" cy="196" r="100" fill="rgba(0,186,242,.25)" stroke="rgba(0,186,242,.6)"/>
      <circle cx="210" cy="240" r="54" fill="#00baf2"/>
      <text x="210" y="56" text-anchor="middle" fill="#fff" font-size="26" font-family="Inter" font-weight="400">4.9 Cr</text><text x="210" y="76" text-anchor="middle" fill="rgba(255,255,255,.6)" font-size="12" font-family="Inter">Paytm merchants</text>
      <text x="210" y="134" text-anchor="middle" fill="#fff" font-size="26" font-family="Inter">1.64 Cr</text><text x="210" y="154" text-anchor="middle" fill="rgba(255,255,255,.7)" font-size="12" font-family="Inter">with a Soundbox</text>
      <text x="210" y="242" text-anchor="middle" fill="#fff" font-size="22" font-family="Inter" font-weight="600">10 lakh</text><text x="210" y="260" text-anchor="middle" fill="#fff" font-size="11" font-family="Inter">year-one goal</text>
    </svg>
  </div>
  <div style="display:flex;flex-direction:column;gap:12px" class="stack">
    <div class="a d1" style="background:var(--sky)"><div><b>Kaasu plan</b><div class="mini" style="color:rgba(255,255,255,.85)">₹49 a month × 10 lakh shops</div></div><span class="v">₹59 Cr/yr</span></div>
    <div class="a d2" style="background:#fff;color:var(--navy)"><div><b>Better loans</b><div class="mini">Smaller, festival-timed, priced by Save Score</div></div><span class="v">Lower risk</span></div>
    <div class="a d3" style="background:var(--pale);color:var(--navy)"><div><b>Postpaid customers</b><div class="mini">Bharosa brings trusted udhaar customers</div></div><span class="v">New users</span></div>
    <div class="a d4" style="background:rgba(255,255,255,.1)"><div><b>Deposits</b><div class="mini">Daily savings pots for partner banks</div></div><span class="v">Float</span></div>
    <div class="a d5" style="background:rgba(255,255,255,.06)"><div><b>Paytm's own plan</b><div class="mini">Subscription + inference fees for merchant AI (Q2 FY27 call)</div></div><span class="v">Fits</span></div>
    <div class="mini a d5" style="margin-top:auto">₹49 price and 10 lakh goal (about 6% of Soundbox merchants) are our assumptions.</div>
  </div>
</div>'''))

# ---------------------------------------------------------------- 13b BUSINESS MODEL FOR PAYTM
eng = [("Payments", "Paytm earns on devices and payments", "Daily saving, Pongal Fund and udhaar links all run through the Paytm QR, so Soundboxes stay active and GMV stays on Paytm.", "Keeps 1.64 Cr devices sticky", "c-white"),
       ("Financial services", "Paytm distributes loans, Postpaid and insurance", "Kaasu sends smaller, festival-timed loans with better repayment, new Postpaid users via Bharosa, and Rain Shield cover.", "Lower risk, more distribution", "c-pale"),
       ("Merchant AI", "Paytm plans subscription + inference fees", "Kaasu is the paid AI CFO tier on the Soundbox, priced like a recharge.", "₹49 a month", "c-navy")]
ue = [("Kaasu AI plan", "₹49 × 12", "₹588"), ("Loan distribution", "30% take a ₹11k loan · ~3% take", "₹99"), ("Bharosa partner fee", "~₹2,600 udhaar moved a month · 2%", "₹624"), ("AI + voice cost", "Cached briefs, ~₹1/min voice", "−₹180")]
sl.append(S("", "Paytm's three engines: payments, financial services distribution, and merchant AI subscriptions. Kaasu feeds all three. Numbers per shop are illustrative.", f'''
<div class="grid" style="grid-template-columns:1fr 1fr 1fr 380px;grid-template-rows:auto 1fr auto;gap:14px;height:100%">
  <div class="c c-navy a" style="grid-column:1/3;padding:24px 26px"><div class="eb">Business model for Paytm</div><h2 class="t" style="font-size:38px">How Paytm earns from Kaasu.</h2></div>
  <div class="c c-sky a d1" style="padding:22px"><div class="big" style="font-size:40px">₹131<small>Cr/yr</small></div><div class="lbl">Revenue at 10 lakh shops</div><div class="mini">₹113 Cr after AI cost</div></div>
  <div class="c c-white a d2" style="grid-row:1/4;grid-column:4;padding:24px;display:flex;flex-direction:column">
    <div class="eb">Unit economics · per shop, per year</div>
    {"".join(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:13px 0;border-top:1px solid var(--line)"><div><b style="font-size:15px;color:var(--navy)">{a}</b><div class="mini">{b}</div></div><span style="font-size:22px;font-weight:500;color:{"var(--red)" if c.startswith("−") else "var(--navy)"}">{c}</span></div>' for a, b, c in ue)}
    <div style="display:flex;justify-content:space-between;align-items:center;padding:16px 18px;margin-top:8px;border-radius:14px;background:var(--navy);color:#fff"><b>Net per shop</b><span style="font-size:28px;font-weight:500">₹1,131</span></div>
    <div class="mini" style="margin-top:auto">Illustrative. Prices, take rates and adoption are our assumptions, to be tested in the Chennai pilot.</div>
  </div>
  {"".join(f'<div class="c {cls} a d{k+2}" style="padding:22px;display:flex;flex-direction:column"><span class="tag{" sky" if cls=="c-navy" else ""}">{k+1} · {a}</span><b style="display:block;font-size:15px;margin-top:14px">{b}</b><p class="p" style="margin-top:8px">{c}</p><div style="margin-top:auto;padding-top:14px;font-size:17px;font-weight:600;color:{"var(--sky-2)" if cls=="c-navy" else "var(--navy)"}">→ {d}</div></div>' for k, (a, b, c, d, cls) in enumerate(eng))}
  <div class="c c-pale a d5" style="grid-column:1/4;padding:16px 22px;display:flex;align-items:center;justify-content:space-between;gap:10px;font-size:14px;font-weight:600">
    <span>The flywheel</span><span>Save daily</span><span style="color:var(--sky)">→</span><span>Save Score rises</span><span style="color:var(--sky)">→</span><span>Cheaper, safer loans</span><span style="color:var(--sky)">→</span><span>More payments on Paytm</span><span style="color:var(--sky)">→</span><span>More saved</span><span style="color:var(--sky)">↺</span>
  </div>
</div>'''))

# ---------------------------------------------------------------- 14 MEET KAASU
sl.append(S("dark", "No new device. No new app. A brain on Paytm's servers.", f'''
<div class="grid" style="grid-template-columns:1fr 520px;gap:30px;height:100%">
  <div style="display:flex;flex-direction:column">
    <div class="eb a">The solution</div>
    <h2 class="t a d1">Meet Kaasu, money that plans ahead.</h2>
    <p class="p a d2" style="margin-top:14px;max-width:440px">On the Soundbox he already has, in the Paytm business app he already uses.</p>
    <div class="num-list a d3" style="margin-top:auto">
      <div style="grid-template-columns:1fr"><div><b>Plans</b><p class="p">Sees the festival gap 53 days early</p></div></div>
      <div style="grid-template-columns:1fr"><div><b>Saves</b><p class="p">₹600 a day, auto-saved at 9 pm</p></div></div>
      <div style="grid-template-columns:1fr"><div><b>Collects</b><p class="p">Paytm reminds udhaar on payday</p></div></div>
      <div style="grid-template-columns:1fr"><div><b>Lends only the gap</b><p class="p">₹11,000, not ₹35,000 in a panic</p></div></div>
    </div>
  </div>
  <div class="grid" style="grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:14px">
    <div class="c c-sky a d1"><div class="big">₹0</div><div class="lbl">New hardware</div></div>
    <div class="c c-img a d2" style="grid-row:1/3;display:grid;place-items:center"><img class="phone zoom" src="img/p-home.png" alt="Kaasu home" style="width:210px"></div>
    <div class="c c-img a d3" style="display:grid;place-items:center"><img src="img/soundbox.png" alt="Soundbox" style="height:220px"></div>
  </div>
</div>'''))

# ---------------------------------------------------------------- 15 ONE MORNING (value-chain timeline)
steps = [("7:00", "Soundbox speaks", '<span class="ta">"₹32,520 குறையும். தினமும் ₹600 ஒதுக்கலாமா?"</span>', '<img src="img/soundbox-on.png" alt="" style="height:96px">', 170, "up"),
         ("7:01", "He says Haan", 'Or presses OK on older boxes', '<div style="width:86px;height:86px;border-radius:50%;background:var(--sky);color:#fff;display:grid;place-items:center;font-size:26px;font-weight:700" class="ta">ஆம்</div>', 470, "down"),
         ("7:02", "PIN on the phone", 'Money never moves on voice alone', '<img class="zoom" src="img/p-pin.png" alt="PIN" style="height:110px">', 790, "up"),
         ("9 pm", "Pongal covered", '₹600 auto-saved every night', '<img class="zoom" src="img/p-done.png" alt="Plan active" style="height:110px">', 1100, "down")]
tl = ""
for k, (tm, h, sub, art, x, pos) in enumerate(steps):
    top = 170 if pos == "up" else 410
    tl += f'<div class="tl-node a d{k+2} {"on" if k==3 else ""}" style="left:{x}px;top:380px">{k+1}</div>'
    tl += f'<div class="c {"c-navy" if k%2 else "c-white"} ab a d{k+2}" style="left:{x-140}px;top:{top}px;width:280px;padding:16px;display:grid;grid-template-columns:auto 1fr;gap:14px;align-items:center">{art}<div><span class="tag{" sky" if k%2 else ""}">{tm}</span><b style="display:block;font-size:16px;margin-top:8px">{h}</b><div class="mini" style="margin-top:4px">{sub}</div></div></div>'
sl.append(S("", "Walk through the four steps like a comic strip.", f'''
<div class="eb a">One morning at Murugan Stores</div>
<h2 class="t a d1">Four steps. Pongal is safe.</h2>
<div class="tl-line a d1" style="top:380px"></div>{tl}'''))

# ---------------------------------------------------------------- 16 POT FILLS (interactive)
jar = re.search(r'<svg class="a d2" viewBox="0 0 340 380".*?</svg>', pots, re.S).group(0)
jar = jar.replace('class="a d2" viewBox="0 0 340 380" style="position:absolute;right:120px;top:130px;width:430px"', 'viewBox="0 0 340 380" style="height:520px"')
sl.append(S("", "Let the judge tap. Watch the loan shrink.", f'''
<div class="grid" style="grid-template-columns:520px 1fr;gap:16px;height:100%">
  <div class="c c-navy a" style="padding:30px">
    <div class="eb">Tap to try · same engine as the app</div>
    <h2 class="t">Own money first. Borrow only the gap.</h2>
    <div style="display:flex;gap:8px;align-items:center;margin-top:22px;flex-wrap:wrap"><span class="mini" style="margin-right:4px">Saves a day</span><span id="saveChips" style="display:flex;gap:6px"></span></div>
    <button class="chip" id="fundOn" aria-pressed="false" style="margin-top:12px">+ Customers' Pongal Fund</button>
    <div class="leg" id="legend" style="margin-top:26px"></div>
  </div>
  <div class="c c-white a d1" style="display:grid;place-items:center">{jar}</div>
</div>'''))

# ---------------------------------------------------------------- 17 BUILT ONLY HERE
six = [("p-fund", "Pongal Fund", "Customers fund the stock"), ("p-circle", "Buy together", "Neighbours get bulk price"), ("p-bill", "Check a bill", "AI finds missed discounts"),
       ("p-score", "Save Score", "Savers borrow cheaper"), ("p-rain", "Rain Shield", "Floods pause the loan"), ("p-udhaar", "Payday udhaar", "Paytm reminds on payday")]
tiles = "".join(f'<div class="c {"c-pale" if k%3==1 else "c-white"} a d{k%5+1}" style="padding:12px 12px 14px"><div class="crop" style="height:300px;background:#eaf6fd"><img class="zoom" src="img/{f}.png" alt="{n}"></div><b style="display:block;margin-top:12px;font-size:15px;color:var(--navy)">{n}</b><div class="mini">{s}</div></div>' for k, (f, n, s) in enumerate(six))
sl.append(S("", "Tap any screen to zoom. We checked 12 earlier Paytm hackathon entries.", f'''
<div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb a">Built only here · tap a screen</div><h2 class="t a d1">Six things no other team built.</h2></div><span class="tag sky a d2">Verified 15 Nov 2026</span></div>
<div class="grid" style="grid-template-columns:repeat(6,1fr);gap:12px;margin-top:24px">{tiles}</div>'''))

# ---------------------------------------------------------------- 18 RAIN (interactive)
sl.append(S("dark", "Press the button. Let it rain.", f'''
<div class="rain" id="rain"></div>
<div class="grid" style="grid-template-columns:1fr 1fr;gap:16px;height:100%;position:relative;z-index:1">
  <div style="display:flex;flex-direction:column">
    <div class="eb a">When life happens</div>
    <h2 class="t a d1">Chennai floods. Kaasu steps in, no claim form.</h2>
    <div class="grid a d2" style="gap:10px;margin-top:24px" id="rainSteps">
      <div class="c c-glass" style="padding:14px 18px;font-weight:600">IMD red alert · pin code 600042</div>
      <div class="c c-glass" style="padding:14px 18px;font-weight:600">His sales −70% · neighbours −64%</div>
      <div class="c c-glass" style="padding:14px 18px;font-weight:600">Loan repayments paused 3 days</div>
      <div class="c c-glass" style="padding:14px 18px;font-weight:600">₹3,000 protection payout</div>
    </div>
    <button class="btn a d3" id="rainGo" style="margin-top:auto;align-self:flex-start">Simulate Chennai red alert</button>
  </div>
  <div class="c c-img a d2" style="position:relative">
    <img src="img/soundbox-on.png" alt="" style="position:absolute;left:20px;bottom:20px;height:250px">
    <img class="phone zoom" src="img/p-rain.png" alt="Rain Shield active" style="position:absolute;right:30px;top:24px;width:240px">
  </div>
</div>'''))

# ---------------------------------------------------------------- 19 GROW (interactive bill)
sl.append(S("", "Press the button: the real AI reads a real bill.", f'''
<div class="grid" style="grid-template-columns:1.2fr 1fr;gap:16px;height:100%">
  <div class="c c-img a" style="position:relative">
    <img class="phone zoom" src="img/p-fund.png" alt="Pongal Fund" style="position:absolute;left:30px;top:70px;width:200px;rotate:-5deg">
    <img class="phone zoom" src="img/p-circle.png" alt="Buy together" style="position:absolute;left:210px;top:30px;width:210px;z-index:2">
    <img class="phone zoom" src="img/p-bill.png" alt="Bill check" style="position:absolute;left:400px;top:70px;width:200px;rotate:5deg">
  </div>
  <div class="c c-pale a d1" style="padding:30px;display:flex;flex-direction:column">
    <div class="eb">Grow with Kaasu</div>
    <h2 class="t">Customers, neighbours and bills become cash.</h2>
    <p class="p" style="margin-top:12px">Regulars pre-pay a Pongal Fund. Four shops buy together at bulk price. AI reads distributor bills and finds missed discounts.</p>
    <button class="btn navy" id="billGo" style="margin-top:20px;align-self:flex-start">Let the AI read a real bill</button>
    <div id="billOut" class="c c-white" style="margin-top:14px;display:none;padding:16px"></div>
  </div>
</div>'''))

# ---------------------------------------------------------------- 20 NEW: BHAROSA, STAFF, GALLA
three = [("p-bharosa2", "Bharosa", "Customer confirms udhaar in Paytm. Trusted udhaar is paid to the shop today.", "₹2,577 paid"),
         ("p-staff", "Staff advance", "Helper asks the Soundbox. Paid from savings, no interest.", "Up to 50% earned"),
         ("p-galla", "Galla check", "Say the cash count. Patterns, never blame.", "₹210 short, 6–9 pm")]
sl.append(S("dark", "Three more problems every kirana has. Tap a screen.", f'''
<div class="grid" style="grid-template-columns:330px 1fr;gap:20px;height:100%">
  <div style="display:flex;flex-direction:column">
    <div class="eb a">New · beyond payments</div>
    <h2 class="t a d1">Udhaar, helpers and the galla.</h2>
    <p class="p a d2" style="margin-top:14px">Automation for the three daily headaches of a kirana, on the same Soundbox and app.</p>
    <div class="a d3" style="margin-top:auto"><hr class="rule"><div style="display:flex;justify-content:space-between;align-items:baseline"><span class="mini">Udhaar confirmed by customers</span><b style="font-size:24px;font-weight:500">5 of 7</b></div><hr class="rule"><div style="display:flex;justify-content:space-between;align-items:baseline"><span class="mini">Advance interest</span><b style="font-size:24px;font-weight:500">₹0</b></div></div>
  </div>
  <div class="grid" style="grid-template-columns:repeat(3,1fr);gap:14px">
  {"".join(f'<div class="c c-glass a d{k+2}" style="padding:14px"><span class="tag sky">{t}</span><div class="crop" style="height:330px;margin-top:12px;background:#eaf6fd"><img class="zoom" src="img/{f}.png" alt="{n}"></div><b style="display:block;font-size:16px;margin-top:12px">{n}</b><div class="mini" style="margin-top:4px">{s}</div></div>' for k, (f, n, s, t) in enumerate(three))}
  </div>
</div>'''))

# ---------------------------------------------------------------- 21 HOW IT CONNECTS (value chain)
sl.append(S("", "The Soundbox has its own 4G SIM. Both talk to Paytm's servers.", f'''
<div class="eb a">How it connects</div>
<h2 class="t a d1">No new device. No new app.</h2>
<svg class="ab a d2" viewBox="0 0 1168 60" style="left:56px;top:330px;width:1168px" aria-hidden="true"><path class="flow" d="M300 30H430M738 30H868" stroke="#00baf2" stroke-width="4" stroke-linecap="round" fill="none"/></svg>
<div class="c c-white ab a d2" style="left:56px;top:200px;width:330px;height:330px;display:grid;place-items:center;text-align:center"><img src="img/soundbox.png" alt="Soundbox" style="height:210px"><div><b style="color:var(--navy)">Paytm Soundbox</b><div class="mini">Own 4G SIM · voice or OK button</div></div></div>
<div class="c c-navy ab a d3" style="left:475px;top:200px;width:330px;height:330px;display:flex;flex-direction:column;justify-content:center;text-align:center"><span style="margin:0 auto;width:72px;height:72px;border-radius:22px;background:var(--sky);color:#fff;display:grid;place-items:center"><svg viewBox="0 0 24 24" width="36" height="36" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{I["cloud"]}</svg></span><b style="font-size:22px;font-weight:500;margin-top:18px">Paytm servers</b><div class="mini" style="margin-top:6px">Kaasu's engine + AI · same merchant account</div></div>
<div class="c c-pale ab a d4" style="right:56px;top:200px;width:330px;height:330px;display:grid;place-items:center;text-align:center"><img class="phone" src="img/p-home.png" alt="Business app" style="height:220px"><div><b>Paytm for Business app</b><div class="mini">PIN moves the money</div></div></div>
<div class="ab a d5" style="left:56px;right:56px;bottom:44px;display:grid;grid-template-columns:repeat(3,1fr);gap:14px">
  <div class="c c-white" style="padding:14px 18px;font-weight:600;font-size:14px">1 · Voice or button says yes</div>
  <div class="c c-white" style="padding:14px 18px;font-weight:600;font-size:14px">2 · Plain maths plans, AI explains in Tamil</div>
  <div class="c c-sky" style="padding:14px 18px;font-weight:600;font-size:14px">3 · PIN moves the money</div>
</div>'''))

# ---------------------------------------------------------------- 22 LIVE
sl.append(S("", "The real app. Restart to begin from the language screen.", '''
<div style="display:flex;justify-content:space-between;align-items:flex-end" class="a"><div><div class="eb">Live</div><h2 class="t">Try it. It's the real product.</h2></div><button class="btn" id="reloadDemo" style="white-space:nowrap">Restart demo</button></div>
<div class="frame a d1"><iframe id="demoFrame" title="Kaasu live demo" data-src="/"></iframe></div>'''))

# ---------------------------------------------------------------- 23 ASK
sl.append(S("dark", "Close on the ask. Stop talking.", f'''
<div class="logo-w a"><img src="/brand/paytm-logo-white.svg" alt="Paytm"><i></i>Kaasu</div>
<h2 class="t xl a d1" style="margin-top:80px;max-width:820px">Let's pilot it in Chennai this Pongal.</h2>
<div class="grid a d2" style="grid-template-columns:repeat(4,1fr);gap:14px;position:absolute;left:56px;right:56px;bottom:100px">
  <div class="c c-sky"><div class="big" data-count="164" data-suffix="L">0</div><div class="lbl">Soundbox counters ready</div></div>
  <div class="c c-glass"><div class="big">₹0</div><div class="lbl">New hardware</div></div>
  <div class="c c-glass"><div class="big">1,000</div><div class="lbl">Chennai shops to pilot</div></div>
  <div class="c c-pale"><div class="big">3×</div><div class="lbl">Revenue: AI plan, safer loans, Postpaid</div></div>
</div>
<div class="ab a d3" style="left:56px;bottom:44px;display:flex;align-items:center;gap:14px;font-size:14px;color:rgba(255,255,255,.75)"><img src="/brand/rps-logo-white.svg" alt="Rock Paper Scissors" style="height:16px">Dheena Dhayalan R · Thank you</div>
<img class="ab a d2 float" src="img/coin.svg" alt="" style="right:40px;top:30px;width:330px">'''))

# ---------------------------------------------------------------- 24 SOURCES
src = [("Paytm", "Q2 FY27 results and call: Soundbox base, merchant GMV, merchant AI subscription plans"), ("Paytm", "Q4 FY26 results: registered merchants; Q2 FY26 lending mix"),
       ("YourStory", "Inside Paytm's Q2, AI Soundbox (Nov 2025)"), ("Analytics India Magazine", "Paytm AI Soundbox in 11 languages"),
       ("Redseer", "Kirana share of grocery, 2025"), ("Inc42", "UPI hits 20.7 billion transactions, Oct 2025"),
       ("Upstox", "PwC × Kirana Club survey, 508 retailers"), ("Datum Intelligence", "Buyers shifting kirana purchases"),
       ("Business Standard", "AICPDF on 2 lakh kirana closures (Oct 2024)"), ("Mediabrief", "CPM India Kirana 2025, 4,593 retailers"),
       ("The Hans India", "Grant Thornton Bharat kirana survey, 1,000+ stores"), ("Outlook Business · NewKerala", "MSME credit gap; 14% formal credit"),
       ("Business Today", "How kirana owners get dues paid back"), ("Sarvam AI", "Voice agents from about ₹1 a minute"),
       ("Competitors", "BharatPe, PhonePe Business, OkCredit, Khatabook, Reelo, LoyalStack, Square, Shopify, Toast, Pine Labs, KiranaPro"),
       ("Prior art", "PhonePe Khata, Paytm Postpaid (Suryoday, Sep 2025), GajiGesa, Square payroll advance"),
       ("Hackathon check", "12 earlier Paytm Build for India entries incl. Money SOS (Mumbai 2026)"), ("Rules", "RBI Digital Lending Directions 2025; Payment Aggregator Master Direction Sep 2025; RBI FAQ on Paytm Payments Bank 2024; DPDP Act 2023; Code on Wages 2019")]
sl.append(S("", "Only if asked. Every number in the deck comes from here.", f'''
<div class="grid" style="grid-template-columns:300px 1fr;gap:16px;height:100%">
  <div class="c c-navy a" style="padding:28px"><div class="eb">Research sources</div><h2 class="t">Where every number comes from</h2><p class="p" style="margin-top:14px">Research done 14–15 Nov 2026. Vendor and industry-body claims are marked as claims.</p></div>
  <div class="c c-white a d1" style="padding:28px"><div class="src-list">{"".join(f"<div><b>{a}</b> · {b}</div>" for a, b in src)}</div></div>
</div>'''))

# ---------------------------------------------------------------- TECH STACK
layers = [("Where Murugan uses it", [("Paytm Soundbox", "Voice in Tamil, OK button, 4G"), ("Paytm for Business app", "Kaasu tabs, PIN, journeys")], "c-white"),
          ("Kaasu service", [("Node.js 24 API", "/brief · /ask · /tts · /bill"), ("Cash engine (rules)", "Every rupee computed in code"), ("Guardrail", "AI text checked against facts")], "c-pale"),
          ("AI layer", [("Google Gemini Flash", "Daily brief and answers"), ("Gemini Vision", "Reads distributor bills to JSON"), ("Sarvam AI", "Indian-language chat + Bulbul voice")], "c-navy"),
          ("Paytm rails", [("UPI + Soundbox", "Payments, savings, reminders"), ("Lending partners · Postpaid", "Loans with KFS, Bharosa"), ("IMD alerts · insurance", "Rain Shield trigger and payout")], "c-sky")]
rows_html = ""
for k, (h, items, cls) in enumerate(layers):
    rows_html += f'<div class="c {cls} a d{k+1}" style="display:grid;grid-template-columns:190px repeat(3,1fr);gap:12px;align-items:center;padding:16px 18px"><b style="font-size:15px">{h}</b>' + "".join(
        f'<div style="background:{"rgba(255,255,255,.1)" if cls in ("c-navy","c-sky") else "#fff" if cls=="c-pale" else "var(--mist)"};border-radius:12px;padding:10px 14px"><div style="font-weight:600;font-size:14px">{a}</div><div class="mini">{b}</div></div>' for a, b in items) + "</div>"
sl.append(S("", "Plain maths decides every number. AI only explains it in Tamil. Gemini first, Sarvam as fallback, cached so demo credits aren't burned.", f'''
<div class="grid" style="grid-template-columns:1fr 300px;gap:16px;height:100%">
  <div style="display:flex;flex-direction:column;gap:12px">
    <div class="a"><div class="eb">Technology · tech stack</div><h2 class="t">Built on what Paytm already runs.</h2></div>
    {rows_html}
  </div>
  <div class="c c-navy a d2" style="padding:24px;display:flex;flex-direction:column;gap:14px">
    <div class="eb">Design choices</div>
    <div><b>Maths decides, AI explains</b><p class="p" style="margin-top:4px">The LLM never invents a number. Any figure not in the facts is rejected.</p></div>
    <div><b>Two AI providers</b><p class="p" style="margin-top:4px">If Gemini fails or hits a limit, Sarvam answers. Voice is cached.</p></div>
    <div><b>PIN moves money</b><p class="p" style="margin-top:4px">Voice and buttons only say yes. Every loan shows a Key Fact Statement.</p></div>
    <div><b>Tested end to end</b><p class="p" style="margin-top:4px">Playwright walks every journey in Chrome.</p></div>
    <div class="mini" style="margin-top:auto">Prototype: HTML, CSS, JavaScript, Node 24. Production: Soundbox OTA + Paytm app module, Paytm Pi model for cost.</div>
  </div>
</div>'''))

# ---------------------------------------------------------------- USP
usp = [("Plans ahead, doesn't just answer", "Sees the Pongal gap 53 days early and fixes it day by day."),
       ("Own money first, loan only the gap", "₹11,000 planned loan instead of ₹35,000 in a panic."),
       ("On the device already on the counter", "1.64 crore Soundboxes. Tamil voice, OK button on older boxes."),
       ("Paytm asks, not the shop", "Udhaar reminders come from Paytm, so regulars aren't offended."),
       ("Safe AI", "Maths decides, AI explains, PIN moves money."),
       ("Six features no other team built", "Pongal Fund, Buy together, Check a bill, Save Score, Rain Shield, Payday udhaar.")]
sl.append(S("dark", "Six reasons Kaasu is different. Then the proof on the next slides.", f'''
<div class="eb a">USP · unique selling proposition</div>
<h2 class="t a d1" style="max-width:760px">Others answer questions. Kaasu plans the shop's cash.</h2>
<hr class="rule a d1" style="margin:26px 0 0">
<div class="num-list a d2" style="grid-template-columns:1fr 1fr 1fr">
{"".join(f'<div style="grid-template-columns:62px 1fr;border-right:{"1px solid rgba(255,255,255,.16)" if k%3!=2 else "0"};padding-left:{"0" if k%3==0 else "24px"}"><span class="n" style="font-size:40px">0{k+1}</span><div><b>{a}</b><p class="p">{b}</p></div></div>' for k, (a, b) in enumerate(usp))}
</div>'''))

# ---------------------------------------------------------------- IMPACT & BENEFITS
sl.append(S("", "Impact for every person in the shop's life, and for Paytm.", f'''
<div class="grid" style="grid-template-columns:repeat(4,1fr);grid-template-rows:auto 1fr 1fr;gap:14px;height:100%">
  <div class="c c-navy a" style="grid-column:1/3;padding:24px 26px"><div class="eb">Impact and benefits</div><h2 class="t" style="font-size:38px">Pongal stock covered, with a smaller loan.</h2></div>
  {stat("c-sky a d1", "−69%", "", "Smaller loan", "₹11,000 planned vs ₹35,000 in a panic")}
  {stat("c-white a d1", "₹31,200", "", "Saved by the shop itself", "₹600 a day for 52 days")}
  <div class="c c-white a d2"><span class="tag">Merchant</span><div class="big" style="margin-top:14px">₹3,370</div><div class="lbl">Udhaar expected back via payday reminders</div><div class="mini" style="margin-top:6px">+ ₹446 found in one bill · ₹2,577 paid via Bharosa</div></div>
  <div class="c c-pale a d2"><span class="tag">Customers</span><div class="lbl" style="font-size:16px;margin-top:14px">No awkward asks. Confirmed udhaar builds their own credit trail. Pongal Fund gives them a festival discount.</div></div>
  <div class="c c-white a d3"><span class="tag">Helpers</span><div class="big" style="margin-top:14px">₹0</div><div class="lbl">Interest on wage advances</div><div class="mini" style="margin-top:6px">Instead of a moneylender</div></div>
  <div class="c c-navy a d3"><span class="tag sky">Paytm</span><div class="lbl" style="font-size:16px;margin-top:14px">Stickier Soundboxes, lower-risk loans, new Postpaid users, a paid AI tier.</div></div>
  <div class="c c-img a d4" style="grid-column:1/3;display:flex;align-items:center;gap:20px;padding:20px 24px"><img src="img/coin.svg" alt="" style="height:150px"><div><span class="tag sky">India</span><div class="lbl" style="font-size:17px;color:var(--navy);margin-top:10px">Savings-first credit history for shops outside formal credit (only 14% of MSMEs today).</div></div></div>
  {stat("c-sky a d4", "1.64", " Cr", "Shops it can reach on day one", "No new hardware")}
  {stat("c-white a d5", "53", " days", "Early warning before the festival", "Not a panic at the last minute")}
</div>'''))

# ---------------------------------------------------------------- RBI & REGULATORY FEASIBILITY
rbi = [("Planned loan", "RBI Digital Lending Directions 2025", "Paytm is the lending service provider for a regulated lender. KFS with APR before signing, cooling-off period, money paid straight to the shop's bank, repaid straight to the lender. No pool account."),
       ("Savings pots", "Deposits only with a bank", "Pots are the shop's own RD or sweep at Paytm's partner bank. Paytm never holds the money. Auto-save by UPI AutoPay, set up with UPI PIN."),
       ("Pongal pre-booking", "Payment Aggregator Directions 2025", "Customer payments settle to the shop T+1. No escrow holding. An advance for goods, never a deposit with returns. Refund if not delivered."),
       ("Bharosa", "Digital lending + credit reporting", "The customer's own Postpaid loan from a regulated lender, with KFS and consent. Paid to the shop as the end-beneficiary. The lender reports to credit bureaus. The shop vouches, never guarantees."),
       ("Reminders and confirmations", "DPDP Act 2023 · TRAI DLT", "Customer opt-in, sent in Paytm's name, each customer sees only their own amount. Not debt collection, no recovery agents."),
       ("Rain Shield", "IRDAI + lender product terms", "Parametric cover from a licensed insurer through Paytm's insurance broking arm. The repayment pause is written into the loan's KFS."),
       ("Staff advance", "Code on Wages 2019", "The shop's own money, not a loan business. Within the 50% deduction limit, with the helper's consent recorded."),
       ("Every payment", "RBI additional factor of authentication", "Money moves only with UPI PIN. Voice and the OK button only say yes. Loan pricing stays with the lender's credit policy.")]
sl.append(S("", "We designed every feature against RBI rules. Paytm is the distributor and technology layer; regulated partners hold money and lend.", f'''
<div style="display:flex;justify-content:space-between;align-items:flex-end;gap:20px">
  <div><div class="eb a">Feasibility · RBI and regulation</div><h2 class="t a d1">Built to RBI rules from day one.</h2></div>
  <div class="c c-navy a d1" style="padding:14px 18px;max-width:430px;font-size:13.5px;line-height:1.45">Paytm is the distributor and technology layer. <b style="color:var(--sky-2)">Regulated banks, NBFCs and insurers</b> hold money, lend and insure.</div>
</div>
<div class="grid" style="grid-template-columns:repeat(4,1fr);gap:12px;margin-top:22px">
{"".join(f'<div class="c {"c-white" if k%2==0 else "c-pale"} a d{k%5+1}" style="padding:16px 18px"><div style="display:flex;justify-content:space-between;align-items:center;gap:8px"><b style="font-size:15px;color:var(--navy)">{a}</b><span class="tag green">✓</span></div><div style="font-size:11.5px;font-weight:700;color:#0089c2;margin-top:6px;letter-spacing:.02em">{b}</div><p class="p" style="margin-top:6px;font-size:12.5px;line-height:1.45">{c}</p></div>' for k, (a, b, c) in enumerate(rbi))}
</div>
<div class="mini a d5" style="margin-top:12px">Based on RBI Digital Lending Directions (May 2025), Payment Aggregator Master Direction (Sep 2025), RBI action on Paytm Payments Bank (2024), DPDP Act 2023. To be confirmed with Paytm's legal and compliance team.</div>'''))

# ================================================================ charts (validated palette: #1F5FD1 series, #0A9BD0 second, grey = context)
C1, C2, CTX = "#1F5FD1", "#0A9BD0", "#C9D3E1"
def colchart(title, sub, rows, unit, fmt, note):
    mx = max(v for _, v, _ in rows) * 1.15
    cols = "".join(f'<div class="cc-col" data-tip="{lab}: {fmt(v)}{unit}"><span class="cc-v">{fmt(v)}{unit}</span><i style="height:{v/mx*100:.1f}%;background:{c}"></i><span class="cc-l">{lab}</span></div>' for lab, v, c in rows)
    return f'<div class="c c-white chart"><b class="ch-t">{title}</b><div class="mini">{sub}</div><div class="cc">{cols}</div><div class="mini">{note}</div></div>'
def hbars(rows, mx, fmt, unit=""):
    return "".join(f'<div class="hb" data-tip="{lab}: {fmt(v)}{unit}"><span class="hb-l">{lab}</span><span class="hb-track"><i class="bar" style="width:{v/mx*100:.1f}%;background:{c}"></i></span><span class="hb-v">{fmt(v)}{unit}</span></div>' for lab, v, c in rows)
CSS += """
.chart { padding: 20px 22px; display: flex; flex-direction: column; }
.ch-t { font-size: 15px; color: var(--ink); }
.cc { flex: 1; display: flex; align-items: flex-end; gap: 22px; padding: 14px 6px 0; border-bottom: 1px solid var(--line); min-height: 150px; margin-bottom: 26px; }
.cc-col { flex: 1; height: 100%; display: flex; flex-direction: column; justify-content: flex-end; align-items: center; position: relative; cursor: default; }
.cc-col i { width: 24px; border-radius: 4px 4px 0 0; display: block; transform-origin: bottom; }
.s.on .cc-col i { animation: colGrow 1.1s var(--ease) both .35s; }
@keyframes colGrow { from { transform: scaleY(0); } to { transform: none; } }
.cc-v { font-size: 14px; font-weight: 600; color: var(--ink); margin-bottom: 6px; font-variant-numeric: tabular-nums; }
.cc-l { position: absolute; bottom: -22px; font-size: 11.5px; color: var(--muted); white-space: nowrap; }
.hb { display: grid; grid-template-columns: 170px 1fr 54px; gap: 12px; align-items: center; padding: 5px 0; cursor: default; }
.hb-l { font-size: 13px; font-weight: 600; color: var(--ink); } .hb-l small { display: block; font-weight: 500; color: var(--muted); font-size: 11px; }
.hb-track { height: 16px; border-left: 1px solid var(--line); display: flex; align-items: center; }
.hb-track .bar { height: 14px; border-radius: 0 4px 4px 0; padding: 0; display: block; }
.hb-v { font-size: 13.5px; font-weight: 600; text-align: right; font-variant-numeric: tabular-nums; color: var(--ink); }
.hb:hover .hb-l, [data-tip]:hover .cc-v { color: #1F5FD1; }
.split { display: flex; height: 26px; gap: 2px; margin-top: 14px; }
.split i { display: block; height: 100%; } .split i:first-child { border-radius: 4px 0 0 4px; } .split i:last-child { border-radius: 0 4px 4px 0; }
.legend { display: flex; gap: 16px; margin-top: 10px; font-size: 12.5px; color: var(--ink-2); } .legend span { display: inline-flex; align-items: center; gap: 6px; } .legend i { width: 10px; height: 10px; border-radius: 3px; display: inline-block; }
.tip { position: fixed; z-index: 30; pointer-events: none; background: var(--ink); color: #fff; font-size: 12.5px; font-weight: 600; padding: 7px 10px; border-radius: 8px; opacity: 0; transform: translateY(4px); transition: opacity .15s, transform .15s; white-space: nowrap; }
.tip.on { opacity: 1; transform: none; }
.bmc { display: grid; grid-template-columns: repeat(10, 1fr); grid-template-rows: 1fr 1fr auto; gap: 10px; height: 100%; }
.bmc > div { border-radius: 16px; padding: 14px 16px; overflow: hidden; }
.bmc h4 { margin: 0 0 8px; font-size: 11.5px; letter-spacing: .1em; text-transform: uppercase; display: flex; align-items: center; gap: 8px; }
.bmc ul { margin: 0; padding: 0; list-style: none; display: grid; gap: 5px; }
.bmc li { font-size: 12.5px; line-height: 1.35; padding-left: 12px; position: relative; }
.bmc li::before { content: ""; position: absolute; left: 0; top: 7px; width: 5px; height: 5px; border-radius: 50%; background: currentColor; opacity: .45; }
.arch { display: grid; grid-template-columns: 1fr 34px 1fr 34px 1.25fr 34px 1fr; align-items: stretch; gap: 0; }
.arch .col { display: flex; flex-direction: column; gap: 12px; } .arch .node { flex: 1; display: flex; flex-direction: column; justify-content: center; }
.arch .col > b { font-size: 11.5px; letter-spacing: .12em; text-transform: uppercase; color: #0089c2; }
.arch .node { border-radius: 14px; padding: 12px 16px; font-size: 15px; font-weight: 600; }
.arch .node small { display: block; font-size: 11.5px; font-weight: 500; opacity: .72; margin-top: 2px; }
.arch .arr { display: grid; place-items: center; }
"""
JS_HELPERS += r'''
// hover tooltips for chart marks
const tip = document.createElement("div"); tip.className = "tip"; document.body.appendChild(tip);
document.addEventListener("mouseover", (e) => { const t = e.target.closest("[data-tip]"); if (!t) { tip.classList.remove("on"); return; } tip.textContent = t.dataset.tip; tip.classList.add("on"); });
document.addEventListener("mousemove", (e) => { tip.style.left = (e.clientX + 14) + "px"; tip.style.top = (e.clientY + 14) + "px"; });
'''
if "hover tooltips for chart marks" not in tail:
    tail = tail.replace("function show(n) {", JS_HELPERS.split("// hover tooltips for chart marks")[0][:0] + "// hover tooltips for chart marks" + JS_HELPERS.split("// hover tooltips for chart marks")[1] + "\nfunction show(n) {", 1)

# ---------------------------------------------------------------- 29 ARCHITECTURE
arrow = '<div class="arr"><svg viewBox="0 0 34 20" width="30" aria-hidden="true"><path class="flow" d="M2 10H28M22 4l7 6-7 6" stroke="#0A9BD0" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
def nodes(items, cls):
    return "".join(f'<div class="node {cls} st">{a}<small>{b}</small></div>' for a, b in items)
sl.append(S("", "Left to right: the shop and its customers, Paytm's existing platform, the Kaasu service, and the regulated partners who hold money and lend.", f'''
<div class="eb a">How it works · architecture</div>
<h2 class="t a d1">Kaasu sits on top of what Paytm already runs.</h2>
<div class="arch a d2" style="margin-top:26px;height:430px">
  <div class="col"><b>Users</b>{nodes([("Paytm Soundbox", "Tamil voice · OK button"), ("Paytm for Business app", "Journeys · UPI PIN"), ("Customer's Paytm app", "Confirm udhaar · pre-book"), ("Helper", "Asks the Soundbox")], "c-white")}</div>
  {arrow}
  <div class="col"><b>Paytm platform</b>{nodes([("Soundbox fleet", "Own 4G SIM · OTA updates"), ("Merchant account", "Payments history · KYC"), ("UPI + Payment Aggregator", "Settles T+1"), ("Notifications", "In Paytm's name")], "c-pale")}</div>
  {arrow}
  <div class="col"><b>Kaasu service</b>{nodes([("Cash engine", "Rules compute every rupee"), ("Planner", "Festival goals · daily save · gap-only loan"), ("AI layer", "Gemini Flash + Vision · Sarvam fallback"), ("Guardrail + consent", "Numbers checked · DPDP consent log")], "c-navy")}</div>
  {arrow}
  <div class="col"><b>Regulated partners</b>{nodes([("Partner bank", "Savings pots (RD / sweep)"), ("NBFC / bank lenders", "Loans with KFS"), ("Postpaid lender", "Bharosa"), ("Insurer · IMD alerts", "Rain Shield")], "c-white")}</div>
</div>
<div class="grid a d4" style="grid-template-columns:repeat(4,1fr);gap:10px;margin-top:16px">
  <div class="c c-sky" style="padding:12px 16px;font-size:13.5px;font-weight:600">1 · Payment data in</div>
  <div class="c c-white" style="padding:12px 16px;font-size:13.5px;font-weight:600">2 · Engine plans, AI explains in Tamil</div>
  <div class="c c-white" style="padding:12px 16px;font-size:13.5px;font-weight:600">3 · Merchant says yes, PIN confirms</div>
  <div class="c c-navy" style="padding:12px 16px;font-size:13.5px;font-weight:600">4 · Partners move the money</div>
</div>'''))

# ---------------------------------------------------------------- 30 BUSINESS MODEL CANVAS
def blk(title, items, cls, style=""):
    return f'<div class="{cls} st" style="{style}"><h4>{title}</h4><ul>{"".join(f"<li>{x}</li>" for x in items)}</ul></div>'
sl.append(S("", "The business model canvas. Revenue figures are our assumptions for a 10 lakh shop rollout.", f'''
<div style="display:grid;grid-template-rows:auto 1fr;gap:14px;height:100%">
<div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb a">Business model canvas</div><h2 class="t a d1" style="font-size:36px">How Kaasu creates and captures value.</h2></div><span class="tag sky a d1">≈ ₹131 Cr a year at 10 lakh shops</span></div>
<div class="bmc a d2">
  {blk("Key partners", ["Partner banks for savings pots", "NBFC and bank lenders", "Postpaid lender for Bharosa", "IRDAI-licensed insurers", "Gemini, Sarvam AI", "Distributors"], "c-white", "grid-column:1/3;grid-row:1/3")}
  {blk("Key activities", ["Cash-flow planning engine", "Tamil voice briefs", "Udhaar reminders in Paytm's name", "Loan and insurance distribution"], "c-pale", "grid-column:3/5;grid-row:1")}
  {blk("Key resources", ["1.64 Cr Soundboxes", "4.9 Cr merchants' payment data", "Paytm app + Pi model", "Lending and insurance partners"], "c-pale", "grid-column:3/5;grid-row:2")}
  {blk("Value proposition", ["Sees the festival gap 53 days early", "Own money first, loan only the gap", "Udhaar back without awkward asks", "Tamil voice on a device he already has", "Safe: PIN, KFS, consent"], "c-navy", "grid-column:5/7;grid-row:1/3")}
  {blk("Customer relationships", ["Daily voice brief", "Consent-first automation", "Save Score that grows"], "c-pale", "grid-column:7/9;grid-row:1")}
  {blk("Channels", ["Paytm Soundbox", "Paytm for Business app", "Customers' Paytm app", "Paytm field sales"], "c-pale", "grid-column:7/9;grid-row:2")}
  {blk("Customer segments", ["Kiranas and small shops with a Soundbox", "Their regular customers", "Shop helpers", "Lenders and insurers (B2B)"], "c-white", "grid-column:9/11;grid-row:1/3")}
  {blk("Cost structure", ["AI + voice ≈ ₹15 per shop a month (cached)", "Engineering and partner integration", "Compliance, support, field training"], "c-white", "grid-column:1/6;grid-row:3")}
  {blk("Revenue streams", ["₹49 a month Kaasu plan → ₹588 a shop a year", "Loan distribution fee ≈ 3% → ₹99", "Bharosa partner fee ≈ 2% → ₹624", "Insurance commission · deposit referral · more UPI on Paytm"], "c-sky", "grid-column:6/11;grid-row:3")}
</div></div>'''))

# ---------------------------------------------------------------- 31 RESEARCH DATA · MARKET (charts)
sl.append(S("", "Research data. Paytm already owns the counter, and kiranas still own grocery. Hover any bar for the value.", f'''
<div style="display:grid;grid-template-rows:auto 1fr auto;gap:14px;height:100%">
<div><div class="eb a">Research data · the market</div><h2 class="t a d1" style="font-size:38px">Paytm owns the counter. Kiranas own grocery.</h2></div>
<div class="grid a d2" style="grid-template-columns:1fr 1fr 1.25fr;gap:14px">
  {colchart("Soundboxes on counters", "Crore devices", [("Q2 FY26", 1.37, C1), ("Q2 FY27", 1.64, C1)], " Cr", lambda v: f"{v:.2f}", "Up 27 lakh in a year · Paytm Q2 FY27")}
  {colchart("Merchant payments a quarter", "₹ lakh crore (GMV)", [("Q2 FY26", 5.6, C1), ("Q2 FY27", 7.1, C1)], "", lambda v: f"₹{v:.1f}", "Up 26% · Q2 FY26 derived from growth")}
  <div class="c c-white chart"><b class="ch-t">India's grocery market by seller</b><div class="mini">Share of sales, 2025</div>
    <div class="big" style="font-size:54px;margin-top:18px;color:var(--ink)">91%</div><div class="lbl" style="margin-top:2px">still sold by kiranas</div>
    <div class="split"><i style="width:91%;background:{C1}" data-tip="Kiranas: 91%"></i><i style="width:9%;background:{CTX}" data-tip="Modern trade + online: 9%"></i></div>
    <div class="legend"><span><i style="background:{C1}"></i>Kiranas</span><span><i style="background:{CTX}"></i>Modern trade + online</span></div>
    <div class="mini" style="margin-top:auto">Redseer estimate</div></div>
</div>
<div class="grid a d3" style="grid-template-columns:repeat(3,1fr);gap:14px">
  {stat("c-navy", "4.9", " Cr", "Registered Paytm merchants", "Paytm Q4 FY26")}
  {stat("c-pale", "20.7", " bn", "UPI payments in one month", "NPCI via Inc42, Oct 2025")}
  {stat("c-sky", "85%", "", "Of Paytm merchant loans went to device owners", "Reported, Q2 FY26")}
</div></div>'''))

# ---------------------------------------------------------------- 32 RESEARCH DATA · COMPETITION + CHOICE (charts)
cap = [("Paytm Kaasu", 4, C1), ("Square · Shopify (US)", 2.5, CTX), ("Pine Labs agents", 2.5, CTX), ("BharatPe assistant", 1.5, CTX), ("Reelo / LoyalStack", 1.5, CTX), ("KiranaPro Vani", 1.5, CTX), ("OkCredit / Khatabook", 1, CTX), ("Paytm AI Soundbox", 1, CTX), ("PhonePe Business", 0, CTX)]
idea = [("Cash planning → Kaasu", 19, C1), ("Proactive growth agent", 18, CTX), ("Regulars win-back", 18, CTX), ("Udhaar recovery", 17, CTX), ("Voice-note orders", 15, CTX), ("Festival restock", 14, CTX), ("Sales Q&A chatbot", 13, CTX)]
sl.append(S("", "Research data. Left: how many of the four capabilities each player covers. Right: how we chose this idea over nine others.", f'''
<div style="display:grid;grid-template-rows:auto 1fr auto;gap:14px;height:100%">
<div><div class="eb a">Research data · competition and choice</div><h2 class="t a d1" style="font-size:38px">Nobody else covers all four. So we built it.</h2></div>
<div class="grid a d2" style="grid-template-columns:1.15fr 1fr;gap:14px">
  <div class="c c-white chart"><b class="ch-t">Capabilities covered, out of 4</b><div class="mini" style="margin-bottom:8px">Answers · acts · brings money in · plans cash ahead by voice. Partly = 0.5</div>{hbars(cap, 4, lambda v: f"{v:g}")}</div>
  <div class="c c-white chart"><b class="ch-t">Idea score, out of 20</b><div class="mini" style="margin-bottom:8px">Unique + impact + Paytm fit + feasible, 5 each</div>{hbars(idea, 20, lambda v: f"{v}")}<div class="mini" style="margin-top:auto">12 earlier Paytm Build for India entries and ~45 product searches checked, 15 Nov 2026</div></div>
</div>
<div class="legend a d3" style="margin:0"><span><i style="background:{C1}"></i>Paytm Kaasu</span><span><i style="background:{CTX}"></i>Others</span><span style="color:var(--muted)">Public sources, Nov 2026 · hover a bar for its value</span></div>
</div>'''))

# ================================================================ 10-SLIDE DECK: every detail once, nothing repeated
# 33 · PROBLEM STATEMENT (persona + gap + root causes)
sl.append(S("", "One man, one date, one number. Murugan is ₹32,520 short for Pongal, and four timing problems explain why.", f'''
<div class="grid" style="grid-template-columns:1.05fr 1fr;gap:16px;height:100%">
  <div class="c c-img a" style="background:linear-gradient(140deg,#0c3b8f,#1f62c2 60%,#00baf2);position:relative;padding:30px">
    <div class="eb" style="color:#bfeeff">Problem statement</div>
    <h2 class="t" style="color:#fff;font-size:40px">Murugan sells ₹11,240 a day and still runs out of money.</h2>
    <div class="bubble" style="margin-top:20px;max-width:380px;position:relative"><span class="ta">"வியாபாரம் நல்லா இருக்கு. ஆனா தேவைப்படும் நாள்ல பணம் இல்ல."</span><small>"Business is good. The money isn't there on the day I need it." · Murugan Stores, Velachery, Chennai</small></div>
    <img src="img/soundbox.png" alt="Paytm Soundbox" style="position:absolute;right:24px;bottom:20px;height:250px">
    <div class="grid" style="grid-template-columns:repeat(2,176px);gap:10px;position:absolute;left:30px;bottom:30px">
      <div class="c c-glass" style="padding:12px 14px"><div class="big" style="font-size:28px">₹80,000</div><div class="mini">Pongal stock due 6 Jan</div></div>
      <div class="c c-glass" style="padding:12px 14px"><div class="big" style="font-size:28px">₹47,480</div><div class="mini" style="color:rgba(255,255,255,.8)">He'll have at today's pace</div></div>
      <div class="c c-glass" style="padding:12px 14px"><div class="big" style="font-size:28px;color:#ffb3c4;white-space:nowrap">−₹32,520</div><div class="mini" style="color:rgba(255,255,255,.8)">Short at today's pace</div></div>
      <div class="c c-glass" style="padding:12px 14px"><div class="big" style="font-size:28px">53 days</div><div class="mini" style="color:rgba(255,255,255,.8)">Left to fix it</div></div>
    </div>
  </div>
  <div class="c c-navy a d1" style="padding:28px">
    <div class="eb">Root causes · timing, not sales</div>
    <div class="num-list" style="grid-template-columns:1fr;margin-top:10px">
      <div style="grid-template-columns:60px 1fr;border-right:0;padding-right:0"><span class="n" style="font-size:38px">01</span><div><b>Festivals come early</b><p class="p">Stock is paid weeks before festival sales arrive.</p></div></div>
      <div style="grid-template-columns:60px 1fr;border-right:0;padding:18px 0"><span class="n" style="font-size:38px">02</span><div><b>Profit goes home</b><p class="p">The family takes each Sunday's profit before the big bill comes.</p></div></div>
      <div style="grid-template-columns:60px 1fr;border-right:0;padding-right:0"><span class="n" style="font-size:38px">03</span><div><b>Udhaar stays unpaid</b><p class="p">Asking regulars to pay "might offend them and they move to another store".</p></div></div>
      <div style="grid-template-columns:60px 1fr;border-right:0;padding:18px 0"><span class="n" style="font-size:38px">04</span><div><b>Credit comes late and costly</b><p class="p">The gap is filled in a panic: a ₹35,000 loan at the worst price.</p></div></div>
    </div>
  </div>
</div>'''))

# 34 · WHY IT MATTERS (research data, charts)
pain = [("Buyers moved ¼ of kirana shopping online", 82), ("Kiranas saw food and FMCG sales fall", 52), ("Fall in Tier 1 footfall", 28), ("Kiranas planning any tech spend", 22), ("Small businesses reaching formal credit", 14)]
sl.append(S("", "The research. Paytm owns the counter, kiranas still own grocery, yet their money management is broken.", f'''
<div style="display:grid;grid-template-rows:auto 1fr;gap:14px;height:100%">
<div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb a">Why it matters · research data</div><h2 class="t a d1" style="font-size:38px">Payments are solved. Money isn't.</h2></div><span class="mini a d1" style="max-width:420px;text-align:right">Sources: Paytm Q2 FY27 &amp; Q4 FY26 results, Redseer, NPCI, PwC × Kirana Club (508 stores), Datum, CPM India (4,593 stores), AICPDF, Outlook Business</span></div>
<div class="grid a d2" style="grid-template-columns:1fr 1fr 1.3fr;gap:14px">
  {colchart("Soundboxes on counters", "Crore devices", [("Q2 FY26", 1.37, C1), ("Q2 FY27", 1.64, C1)], " Cr", lambda v: f"{v:.2f}", "+27 lakh in a year")}
  <div class="grid" style="grid-template-rows:1fr 1fr 1fr;gap:10px">
    {stat("c-navy", "4.9", " Cr", "Paytm merchants", "₹7.1 lakh cr payments a quarter, +26%")}
    {stat("c-pale", "91%", "", "Grocery still sold by kiranas", "20.7 bn UPI payments a month")}
    {stat("c-sky", "85%", "", "Merchant loans to Paytm device owners", "₹25–30 lakh cr MSME credit gap")}
  </div>
  <div class="c c-white chart"><b class="ch-t">Kiranas under pressure</b><div class="mini" style="margin-bottom:12px">Share of stores or buyers, surveys 2024–2026 · about 2 lakh kiranas closed (AICPDF claim)</div>
    {"".join(f'<div class="hb" data-tip="{l}: {v}%" style="grid-template-columns:1fr;gap:4px;padding:6px 0"><span class="hb-l" style="font-weight:500">{l}</span><span style="display:flex;align-items:center;gap:10px"><span class="hb-track" style="flex:1"><i class="bar" style="width:{v}%;background:{C1}"></i></span><span class="hb-v">{v}%</span></span></div>' for l, v in pain)}
  </div>
</div></div>'''))

# 35 · SOLUTION (Kaasu + how it works + the money)
sl.append(S("dark", "Kaasu, Tamil for money. Own money first, loan only the gap. The Soundbox says it, the merchant says yes, the PIN moves money.", f'''
<div class="grid" style="grid-template-columns:1fr 300px 330px;gap:16px;height:100%">
  <div style="display:flex;flex-direction:column">
    <div class="eb a">How we solve it · Paytm Kaasu</div>
    <h2 class="t a d1">Kaasu plans the shop's cash, 53 days ahead.</h2>
    <p class="p a d2" style="margin-top:10px">காசு, Tamil for money. Runs on the Soundbox and the Paytm for Business app he already uses. No new hardware.</p>
    <div class="grid a d3" style="grid-template-columns:repeat(4,1fr);gap:8px;margin-top:20px">
      <div class="c c-glass" style="padding:12px"><span class="tag sky">1</span><div class="lbl">Soundbox speaks in Tamil at 7 am</div></div>
      <div class="c c-glass" style="padding:12px"><span class="tag sky">2</span><div class="lbl">He says "aam", or presses OK on older boxes</div></div>
      <div class="c c-glass" style="padding:12px"><span class="tag sky">3</span><div class="lbl">UPI PIN on the phone moves the money</div></div>
      <div class="c c-glass" style="padding:12px"><span class="tag sky">4</span><div class="lbl">Auto-saves every night at 9 pm</div></div>
    </div>
    <div class="c c-white a d4" style="margin-top:auto;padding:18px 20px">
      <div class="eb">The money plan · ₹32,520 gap</div>
      <div class="stack" style="display:grid;gap:6px">
        <div style="background:var(--mist);padding:9px 14px"><b>His own savings</b><span class="v" style="font-size:20px;color:var(--navy)">₹600 × 52 days = ₹31,200</span></div>
        <div style="background:var(--mist);padding:9px 14px"><b>Udhaar collected on payday</b><span class="v" style="font-size:20px;color:var(--navy)">₹3,370 expected</span></div>
        <div style="background:var(--navy);color:#fff;padding:9px 14px"><b>Planned loan, gap only</b><span class="v" style="font-size:20px">₹11,000 · ₹190/day from 17 Jan</span></div>
      </div>
      <div class="mini" style="margin-top:8px">Instead of ₹35,000 in a panic. Customers' Pongal pre-bookings can take it to zero.</div>
    </div>
  </div>
  <div class="c c-img a d2" style="display:grid;place-items:center"><img src="img/soundbox-on.png" alt="Soundbox speaking" style="height:330px"></div>
  <div class="c c-img a d3" style="display:grid;place-items:center"><img class="phone zoom" src="img/p-short.png" alt="Pongal plan screen" style="height:560px"></div>
</div>'''))

# 36 · FEATURES (all nine, one line each, honest prior art)
feats = [("p-fund", "Pongal pre-booking", "Regulars pre-pay festival hampers; settles to the shop T+1."), ("p-circle", "Buy together", "4 neighbouring shops pool orders for a 6% bulk price."), ("p-bill", "Check a bill", "Gemini Vision reads distributor bills: ₹446 of missed discounts found."),
         ("p-score", "Save Score", "Regular savers get cheaper loans: score 730, 1.2% a month."), ("p-rain", "Rain Shield", "IMD red alert pauses repayments 3 days and pays ₹3,000 cover."), ("p-udhaar", "Payday udhaar", "Paytm, not the shop, reminds each customer on their payday."),
         ("p-bharosa2", "Bharosa", "Customers confirm udhaar; trusted udhaar paid to the shop today (₹2,577)."), ("p-staff", "Staff advance", "Helper asks the Soundbox; up to 50% of earned wage, no interest."), ("p-galla", "Galla check", "Spoken cash count vs expected: ₹210 short, 6–9 pm pattern, no blame.")]
sl.append(S("", "Nine features. The first six were not found in any earlier Paytm hackathon entry or product. The last three extend things that partly exist.", f'''
<div style="display:flex;justify-content:space-between;align-items:flex-end"><div><div class="eb a">How we solve it · features</div><h2 class="t a d1" style="font-size:36px">Nine ways Kaasu brings money in. Tap a screen.</h2></div><span class="tag sky a d1">Top 6 new · checked 15 Nov 2026</span></div>
<div class="grid" style="grid-template-columns:repeat(9,1fr);gap:10px;margin-top:18px">
{"".join(f'<div class="c {"c-white" if k<6 else "c-pale"} a d{k%5+1}" style="padding:10px 10px 12px"><div class="crop" style="height:300px;background:#eaf6fd"><img class="zoom" src="img/{f}.png" alt="{n}"></div><b style="display:block;margin-top:10px;font-size:14px;color:var(--navy)">{n}</b><div class="mini" style="margin-top:3px;line-height:1.35">{s}</div></div>' for k, (f, n, s) in enumerate(feats))}
</div>
<div class="mini a d5" style="margin-top:12px">Partly exists elsewhere: customer-visible khata (PhonePe), Paytm Postpaid, wage advances (Square, GajiGesa abroad), POS cash-drawer tools. Kaasu adds per-entry confirmation, udhaar takeover, voice requests on the Soundbox and patterns instead of blame.</div>'''))

# 37 · COMPETITION + USP
usp6 = ["Plans ahead, doesn't just answer", "Own money first, loan only the gap", "On 1.64 Cr devices already on counters", "Paytm asks for udhaar, not the shop", "Maths decides, AI explains, PIN moves money", "Tamil voice, OK button on older boxes"]
sl.append(S("dark", "Everyone answers. Few act. Nobody else plans the shop's cash ahead, by voice, on the counter. That is our USP.", f'''
<div class="grid" style="grid-template-columns:1.2fr 1fr;gap:16px;height:100%">
  <div class="c c-white a" style="padding:24px">
    <div class="eb">Competition · capabilities covered out of 4</div>
    <div class="mini" style="margin-bottom:10px">Answers · acts · brings money in · plans cash ahead by voice (partly = 0.5). Public sources, Nov 2026.</div>
    {hbars(cap, 4, lambda v: f"{v:g}")}
    <div class="mini" style="margin-top:12px">Also checked: 12 earlier Paytm Build for India entries. Mumbai 2026 winner "Money SOS" plans a cash gap; Kaasu adds the festival pot, udhaar and Soundbox voice. Of 10 ideas scored on uniqueness, impact, Paytm fit and feasibility, this scored 19/20; a sales chatbot scored 13.</div>
  </div>
  <div style="display:flex;flex-direction:column">
    <div class="eb a">USP</div>
    <h2 class="t a d1" style="font-size:38px">Others answer questions. Kaasu plans the cash.</h2>
    <div class="grid a d2" style="grid-template-columns:1fr 1fr;gap:10px;margin-top:20px">
      {"".join(f'<div class="c c-glass" style="padding:14px 16px"><span class="n" style="font-size:24px;color:var(--sky-2);font-weight:300">0{k+1}</span><div class="lbl" style="margin-top:4px">{u}</div></div>' for k, u in enumerate(usp6))}
    </div>
  </div>
</div>'''))

# 38 · ASK + IMPACT + SOURCES (close)
sl.append(S("dark", "Close on the ask, then stop. Sources are on screen if a judge asks.", f'''
<div class="grid" style="grid-template-columns:1.25fr 1fr;gap:18px;height:100%">
  <div style="display:flex;flex-direction:column">
    <div class="logo-w a"><img src="/brand/paytm-logo-white.svg" alt="Paytm"><i></i>Kaasu</div>
    <h2 class="t xl a d1" style="margin-top:46px;font-size:68px">Let's pilot it in Chennai this Pongal.</h2>
    <div class="grid a d2" style="grid-template-columns:repeat(3,1fr);gap:10px;margin-top:28px">
      <div class="c c-sky"><div class="big" style="font-size:36px">1,000</div><div class="lbl">Chennai shops in the pilot</div></div>
      <div class="c c-glass"><div class="big" style="font-size:36px">−69%</div><div class="lbl">Smaller festival loan</div></div>
      <div class="c c-glass"><div class="big" style="font-size:36px">₹0</div><div class="lbl">New hardware or interest on advances</div></div>
    </div>
    <p class="p a d3" style="margin-top:16px">Impact: shops plan instead of panic; customers keep their dignity and build a credit trail; helpers skip the moneylender; Paytm gets stickier Soundboxes, safer loans and new Postpaid users.</p>
    <div class="a d4" style="margin-top:auto;display:flex;align-items:center;gap:14px;font-size:14px;color:rgba(255,255,255,.75)"><img src="/brand/rps-logo-white.svg" alt="Rock Paper Scissors" style="height:16px">Dheena Dhayalan R · Thank you</div>
  </div>
  <div class="c c-glass a d2" style="padding:22px">
    <div class="eb">Sources · research 14–15 Nov 2026</div>
    <div class="src-list" style="columns:1;font-size:11.5px;color:rgba(255,255,255,.75)">{"".join(f"<div><b style='color:#fff'>{a}</b> · {b}</div>" for a, b in src)}</div>
  </div>
</div>'''))

# architecture slide: replace the step strip with the RBI compliance strip so slide 7 carries both
sl[29] = sl[29].replace('''<div class="grid a d4" style="grid-template-columns:repeat(4,1fr);gap:10px;margin-top:16px">
  <div class="c c-sky" style="padding:12px 16px;font-size:13.5px;font-weight:600">1 · Payment data in</div>
  <div class="c c-white" style="padding:12px 16px;font-size:13.5px;font-weight:600">2 · Engine plans, AI explains in Tamil</div>
  <div class="c c-white" style="padding:12px 16px;font-size:13.5px;font-weight:600">3 · Merchant says yes, PIN confirms</div>
  <div class="c c-navy" style="padding:12px 16px;font-size:13.5px;font-weight:600">4 · Partners move the money</div>
</div>''', f'''<div class="grid a d4" style="grid-template-columns:repeat(4,1fr);gap:10px;margin-top:14px">
  {"".join(f'<div class="c {"c-navy" if k==0 else "c-white"}" style="padding:10px 14px"><b style="font-size:13px">{a}</b><div class="mini" style="margin-top:2px">{b}</div></div>' for k, (a, b) in enumerate([("RBI-ready by design", "Paytm is the distributor; regulated partners hold money and lend"), ("Digital Lending Directions 2025", "KFS + APR, cooling-off, paid and repaid directly, no pool account"), ("Payment Aggregator rules 2025", "Pre-bookings settle to the shop T+1, never held in escrow"), ("DPDP Act · Code on Wages", "Consent for reminders; wage deductions within the 50% limit")]))}
</div>''')
sl[29] = sl[29].replace('<div class="arch a d2" style="margin-top:26px;height:430px">', '<div class="arch a d2" style="margin-top:20px;height:400px">')
sl[29] = sl[29].replace("Kaasu sits on top of what Paytm already runs.", "Architecture and tech stack: Kaasu runs on what Paytm already has.")

CSS += """
.amb { position: absolute; inset: 0; pointer-events: none; z-index: 0; overflow: hidden; }
.amb i { position: absolute; border-radius: 50%; filter: blur(50px); opacity: .5; animation: ambd 16s ease-in-out infinite alternate; animation-play-state: paused; }
.amb i:nth-child(1) { width: 520px; height: 520px; right: -140px; top: -160px; background: radial-gradient(circle, rgba(0,186,242,.55), transparent 70%); }
.amb i:nth-child(2) { width: 460px; height: 460px; left: -160px; bottom: -180px; background: radial-gradient(circle, rgba(36,72,255,.35), transparent 70%); animation-duration: 20s; animation-direction: alternate-reverse; }
.amb i:nth-child(3) { width: 14px; height: 14px; filter: none; opacity: .7; left: 62%; top: 18%; background: var(--sky); box-shadow: 0 0 18px var(--sky); animation: ambdot 9s ease-in-out infinite alternate; animation-play-state: paused; }
.s.on .amb i { animation-play-state: running; }
@keyframes ambd { 0% { transform: translate(0,0) scale(1); } 50% { transform: translate(-60px,40px) scale(1.12); } 100% { transform: translate(40px,80px) scale(.94); } }
@keyframes ambdot { 0% { transform: translate(0,0); } 100% { transform: translate(-220px,120px); } }
.s .in { z-index: 1; }
.s.on .c-img img:not(.zoom), .s.on img[src*="soundbox"], .s.on img[src*="coin"] { animation: up .85s var(--ease) both, float 6s 1s ease-in-out infinite; }
.s.on .crop img { animation: peek 9s ease-in-out infinite alternate; }
@keyframes peek { 0%, 20% { transform: translateY(0); } 100% { transform: translateY(-14%); } }
.s.on .big { text-shadow: 0 0 0 transparent; }
@media (prefers-reduced-motion: reduce) { .amb i, .s.on .crop img { animation: none !important; } }
"""
JS_AMB = "document.querySelectorAll('section.s').forEach(s => { const a = document.createElement('div'); a.className = 'amb'; a.innerHTML = '<i></i><i></i><i></i>'; s.prepend(a); });"
tail = tail.replace("const deck = $(\"deck\")", JS_AMB + chr(10) + "const deck = $(\"deck\")", 1)
SEC = {}
order = []
def put(sec, *idx):
    for i in idx: order.append(i); SEC[i] = sec
put("Title", 0)
put("Introduction", 1)
put("Problem statement", 33)
put("Why it matters", 34)
put("How we solve it", 35, 36)
put("Architecture and RBI", 29)
put("Competition and USP", 37)
put("Business model canvas", 30)
put("Thank you", 38)
sl = [s for s in sl]  # every other slide is dropped: nothing repeats
sl = [sl[i].replace('<section class="s ', f'<section data-sec="{SEC[i]}" class="s ', 1) for i in order]
CSS += """
.s[data-sec]::before { content: attr(data-sec); position: absolute; left: 56px; bottom: 15px; font-size: 11px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); z-index: 2; }
.s.dark[data-sec]::before { color: rgba(255,255,255,.45); }
.s[data-sec="Title"]::before, .s[data-sec="Thank you"]::before { content: none; }
"""

html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Paytm Kaasu · Story</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Anek+Tamil:wght@500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="stage"><div class="deck" id="deck">
{"".join(sl)}
</div></div>

{tail}'''
open(P, "w", encoding="utf-8").write(html)
print("slides:", len(sl))
