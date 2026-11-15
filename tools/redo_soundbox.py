"""Replace the Soundbox panel with a realistic counter device + QR standee."""
import os, random, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
random.seed(7)
N, cell = 25, 4
def finder(x, y):
    return [(x + i, y + j) for i in range(7) for j in range(7) if i in (0, 6) or j in (0, 6) or (2 <= i <= 4 and 2 <= j <= 4)]
mods = set(finder(0, 0)) | set(finder(N - 7, 0)) | set(finder(0, N - 7))
reserved = {(i, j) for i in range(8) for j in range(8)} | {(N - 8 + i, j) for i in range(8) for j in range(8)} | {(i, N - 8 + j) for i in range(8) for j in range(8)}
for i in range(N):
    for j in range(N):
        if (i, j) not in reserved and random.random() < 0.48:
            mods.add((i, j))
rects = "".join(f'<rect x="{i*cell}" y="{j*cell}" width="{cell}" height="{cell}"/>' for i, j in sorted(mods))
qr = f'<svg class="qr" viewBox="0 0 {N*cell} {N*cell}" aria-hidden="true" shape-rendering="crispEdges">{rects}</svg>'

DEVICE = f'''  <section class="soundbox-col" aria-label="Soundbox">
    <div class="col-label">On the counter</div>
    <div class="device">
      <div class="qr-stand" aria-hidden="true">
        <div class="qr-head">Scan &amp; pay</div>
        <div class="qr-box">{qr}</div>
        <div class="qr-name">Murugan Stores</div>
        <div class="qr-upi">UPI · demo QR</div>
      </div>
      <div class="device-body">
        <div class="device-top">
          <span class="led" aria-hidden="true"></span><span class="net">4G</span>
          <span class="hw-small" aria-hidden="true">−</span><span class="hw-small" aria-hidden="true">+</span><span class="hw-small power" aria-hidden="true"></span>
        </div>
        <div class="lcd"><span class="lcd-glow" id="sbTop">Rs 80 received</span></div>
        <div class="grille" aria-hidden="true"></div>
        <div class="glass">
          <div class="sb-wave" id="sbWave" aria-hidden="true"><b></b><b></b><b></b><b></b><b></b><b></b><b></b><b></b><b></b></div>
          <p class="sb-text ta" id="sbText">காலை வணக்கம் முருகன். இன்றைய பணத் திட்டம் தயார்.</p>
          <p class="sb-text-en" id="sbTextEn">Good morning Murugan. Today's cash plan is ready.</p>
        </div>
        <div class="sb-controls keys">
          <div class="seg" role="group" aria-label="Voice language">
            <button type="button" class="on" data-lang="ta" id="langTa">த</button>
            <button type="button" data-lang="en" id="langEn">EN</button>
          </div>
          <button id="playBrief" class="key" type="button" aria-label="Play morning brief"><span class="ico play" aria-hidden="true"></span><span>Brief</span></button>
          <button id="sayHaan" class="key mic" type="button" aria-label="Say haan"><span class="ico mic" aria-hidden="true"></span><span>Haan</span></button>
        </div>
        <div class="brandplate">AI Soundbox · demo</div>
      </div>
      <div class="device-shadow" aria-hidden="true"></div>
    </div>
    <p class="sb-hint" id="sbHint">Press Haan, then say "haan", "ஆம்" or "yes". Double-press to approve.</p>
    <div class="story">
      <div class="story-h">Murugan Stores · Velachery, Chennai</div>
      <p>Sells about Rs 11,000 a day on Paytm QR. Pongal stock of <b>Rs 80,000</b> is due on <b>6 January</b>. Every Sunday he takes home what's left. In January, the money isn't there.</p>
    </div>
  </section>'''

CSS = '''
/* ---------- Real-device Soundbox ---------- */
.device { position: relative; padding-top: 118px; max-width: 380px; margin: 0 auto; }
.qr-stand { position: absolute; top: 0; left: 50%; width: 220px; margin-left: -110px; height: 300px; background: linear-gradient(180deg, #ffffff, #f1f3f8); border-radius: 22px 22px 6px 6px; box-shadow: 0 0 0 1px #e1e4ec, 0 18px 30px -18px rgba(10,20,60,.35); text-align: center; padding: 12px 18px 0; }
.qr-head { font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: #0636a3; }
.qr-box { margin: 8px auto 6px; width: 104px; height: 104px; padding: 7px; background: #fff; border-radius: 10px; box-shadow: 0 0 0 1px #e6e8ef; }
.qr { width: 100%; height: 100%; display: block; fill: #0a0a0f; }
.qr-name { font-size: 13px; font-weight: 700; color: var(--ink); }
.qr-upi { font-size: 10.5px; color: var(--muted); }
.device-body { position: relative; z-index: 1; border-radius: 34px 34px 40px 40px; padding: 14px 18px 18px;
  background: linear-gradient(160deg, #2a3561 0%, #141b3d 38%, #0b1029 100%);
  box-shadow: inset 0 2px 0 rgba(255,255,255,.18), inset 0 -10px 18px rgba(0,0,0,.45), inset 6px 0 14px rgba(255,255,255,.04), 0 30px 50px -24px rgba(5,10,40,.75); color: #fff; }
.device-body::before { content: ""; position: absolute; left: 22px; right: 22px; top: 6px; height: 40%; border-radius: 30px; background: linear-gradient(180deg, rgba(255,255,255,.08), rgba(255,255,255,0)); pointer-events: none; }
.device-top { display: flex; align-items: center; gap: 8px; padding: 0 4px 10px; }
.led { width: 7px; height: 7px; border-radius: 50%; background: #3dff9a; box-shadow: 0 0 8px #3dff9a; }
.net { font-size: 10px; font-weight: 700; color: rgba(255,255,255,.6); letter-spacing: .06em; margin-right: auto; }
.hw-small { width: 30px; height: 16px; border-radius: 8px; background: linear-gradient(180deg, #2c3666, #12183a); box-shadow: inset 0 1px 0 rgba(255,255,255,.18), 0 1px 2px rgba(0,0,0,.5); color: rgba(255,255,255,.7); font-size: 12px; line-height: 15px; text-align: center; font-weight: 700; }
.hw-small.power { width: 16px; position: relative; }
.hw-small.power::after { content: ""; position: absolute; left: 5px; top: 4px; width: 6px; height: 6px; border-radius: 50%; border: 1.5px solid rgba(255,255,255,.6); box-sizing: border-box; }
.lcd { background: #050806; border-radius: 10px; padding: 8px 12px; box-shadow: inset 0 2px 6px rgba(0,0,0,.9), 0 1px 0 rgba(255,255,255,.08); text-align: center; }
.lcd-glow { font-family: "Courier New", ui-monospace, monospace; font-weight: 700; font-size: 20px; letter-spacing: .08em; color: #5dff9e; text-shadow: 0 0 6px rgba(93,255,158,.75); text-transform: uppercase; }
.grille { height: 46px; margin: 12px 6px; border-radius: 14px; background-color: #0a0f26; background-image: radial-gradient(circle, #02040d 1.6px, transparent 2.1px); background-size: 9px 9px; box-shadow: inset 0 2px 5px rgba(0,0,0,.7); }
.glass { background: linear-gradient(160deg, #0d1638 0%, #050a1f 100%); border-radius: 18px; padding: 14px 16px; height: 240px; overflow-y: auto; scrollbar-width: none; box-shadow: inset 0 0 0 1px rgba(255,255,255,.06), inset 0 8px 20px rgba(0,0,0,.6); display: flex; flex-direction: column; gap: 6px; }
.glass::-webkit-scrollbar { display: none; }
.glass .sb-text { font-size: 16px; line-height: 1.5; }
.glass .sb-text-en { font-size: 12px; }
.sb-controls.keys { display: grid; grid-template-columns: auto 1fr 1fr; gap: 10px; align-items: center; padding-top: 14px; }
.keys .seg { background: #070b20; box-shadow: inset 0 2px 4px rgba(0,0,0,.7); border-radius: 14px; padding: 4px; }
.keys .seg button { padding: 10px 11px; font-weight: 700; border-radius: 10px; font-size: 14px; }
.keys .seg button.on { background: linear-gradient(180deg, #ffffff, #d9deea); color: #0a0a0f; box-shadow: 0 2px 0 #9aa3bb; }
.key { height: 54px; border: 0; border-radius: 16px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 3px; font-size: 12px; font-weight: 600; color: #fff;
  background: linear-gradient(180deg, #2f3a6c, #161d45); box-shadow: inset 0 1px 0 rgba(255,255,255,.22), 0 4px 0 #060a1f, 0 6px 10px rgba(0,0,0,.4); transition: transform .06s, box-shadow .06s; }
.key:active { transform: translateY(3px); box-shadow: inset 0 1px 0 rgba(255,255,255,.18), 0 1px 0 #060a1f; }
.key.mic { background: linear-gradient(180deg, #ffffff, #dfe4ef); color: #0a0a0f; box-shadow: inset 0 1px 0 #fff, 0 4px 0 #8f99b3, 0 6px 10px rgba(0,0,0,.35); }
.key.mic:active { box-shadow: 0 1px 0 #8f99b3; }
.brandplate { text-align: center; font-size: 10px; letter-spacing: .14em; text-transform: uppercase; color: rgba(255,255,255,.35); margin-top: 12px; }
.device-shadow { height: 22px; margin: -6px 30px 0; border-radius: 50%; background: radial-gradient(ellipse at center, rgba(10,20,60,.35), transparent 70%); }
.soundbox-col > .sb-hint { color: var(--muted); font-size: 12.5px; text-align: center; margin: 8px 0 0; }
'''

p = os.path.join(ROOT, "public", "index.html")
s = open(p, encoding="utf-8").read()
s2 = re.sub(r'  <section class="soundbox-col" aria-label="Soundbox">.*?</section>', lambda m: DEVICE, s, count=1, flags=re.S)
assert s2 != s
open(p, "w", encoding="utf-8").write(s2)
cp = os.path.join(ROOT, "public", "styles.css")
c = open(cp, encoding="utf-8").read()
if "Real-device Soundbox" not in c:
    open(cp, "a", encoding="utf-8").write(CSS)
print("soundbox replaced")
