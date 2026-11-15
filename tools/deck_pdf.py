"""Capture each deck slide (after its animations settle) and assemble Kaasu-Pitch-Deck.pdf."""
from playwright.sync_api import sync_playwright
from PIL import Image
import os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = sys.argv[1] if len(sys.argv) > 1 else "https://paytm-kaasu.vercel.app/deck/"
shots = []
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome"); pg = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    pg.goto(URL); pg.wait_for_timeout(3000)
    n = pg.evaluate("document.getElementById('deck').children.length")
    pg.add_style_tag(content="#notes,#dots,#prev,#next,#fs,#bar,.tip,.hud{display:none!important}")
    for k in range(n):
        pg.evaluate(f"document.getElementById('dots').children[{k}].click()"); pg.wait_for_timeout(2600)
        f = os.path.join(ROOT, "video", f"deck_{k+1:02d}.png"); pg.screenshot(path=f); shots.append(f)
    b.close()
ims = [Image.open(f).convert("RGB") for f in shots]
out = os.path.join(ROOT, "Kaasu-Pitch-Deck.pdf")
ims[0].save(out, save_all=True, append_images=ims[1:], resolution=144)
print(n, "slides ->", out, os.path.getsize(out) // 1024, "KB")
