"""Render the Kaasu film deterministically: seek every CSS animation to each frame time and screenshot."""
import json, os, subprocess, sys, urllib.parse
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DUR = {"s01": 11, "s02": 15, "s03": 15, "s04": 9, "s05": 18, "s06": 14, "s07": 10, "s08": 15, "s09": 15}
T, t = {}, 0.0
for k, v in DUR.items(): T[k] = [round(t, 2), round(t + v, 2)]; t += v
LENGTH = t
url = "http://localhost:3000/" + os.environ.get("FILM", "film") + "/?t=" + urllib.parse.quote(json.dumps(T))
mode = sys.argv[1] if len(sys.argv) > 1 else "preview"
FPS = 25
SPEED = float(os.environ.get("SPEED", "1"))
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome"); pg = b.new_page(viewport={"width": 1920, "height": 1080})
    pg.goto(url, wait_until="networkidle"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(800)
    if mode == "preview":
        out = sys.argv[2]
        for i, s in enumerate([float(x) for x in sys.argv[3].split(",")]):
            pg.evaluate(f"seek({s})"); pg.wait_for_timeout(60); pg.screenshot(path=os.path.join(out, f"f{i:02d}.jpg"), type="jpeg", quality=80)
    else:
        out = os.path.join(ROOT, "video", os.environ.get("FILM", "film") + ("-fast" if SPEED != 1 else "") + "-silent.mp4")
        ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "image2pipe", "-framerate", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        n = int(LENGTH / SPEED * FPS)
        for i in range(n):
            pg.evaluate(f"seek({i / FPS * SPEED})")
            ff.stdin.write(pg.screenshot(type="jpeg", quality=92))
            if i % 250 == 0: print("frame", i, "/", n, flush=True)
        ff.stdin.close(); ff.wait(); print("wrote", out, LENGTH, "s")
    b.close()
print(json.dumps(T))
