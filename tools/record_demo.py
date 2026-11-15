"""Record a fast, silent walkthrough of the real Kaasu app (Soundbox + phone) for the film.
Voice is muted first and /api/tts is blocked, so no paid voice credits are used."""
import os, shutil, time
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "video", "demo-raw"); shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
marks = []
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    ctx = b.new_context(viewport={"width": 1920, "height": 1080}, record_video_dir=OUT, record_video_size={"width": 1920, "height": 1080})
    t0 = time.time()
    pg = ctx.new_page()
    pg.route("**/api/tts", lambda r: r.fulfill(status=204, body=""))
    W = pg.wait_for_timeout
    nxt = lambda w=700: (pg.click("#jNext"), W(w))
    def pin():
        for k in "1234": pg.click(f"#keypad button:text-is('{k}')"); W(120)
        W(900)
    pg.goto("http://localhost:3000", wait_until="networkidle"); W(300)
    pg.click("#muteBtn"); W(200)
    marks.append(("start", time.time() - t0))
    pg.click("[data-pick=ta]"); W(900); pg.click("#getStarted"); W(2200)
    pg.click("[data-go=pongal]"); W(900); nxt(); nxt(); W(400)   # show the plan on the phone
    pg.click("#jClose"); W(700)
    pg.click("#pressBtn"); W(1400)                               # "Haan" via the Soundbox OK button
    pin(); W(1000); pg.click("#doneHome"); W(1400)
    pg.click(".tab[data-tab=Udhaar]"); W(1300)
    pg.click("#paneUdhaar .bh-card"); W(900); nxt(); nxt(); nxt(900); pin()
    pg.click("#doneHome"); W(3200)                               # payments arrive one by one
    pg.click(".tab[data-tab=Loans]"); W(600); pg.click("#rainBtn"); W(1800)
    pg.click(".tab[data-tab=Home]"); W(1500)
    marks.append(("end", time.time() - t0))
    path = pg.video.path(); ctx.close(); b.close()
os.replace(path, os.path.join(OUT, "demo.webm"))
open(os.path.join(OUT, "marks.txt"), "w").write(" ".join(f"{k}={v:.2f}" for k, v in marks))
print(marks)
