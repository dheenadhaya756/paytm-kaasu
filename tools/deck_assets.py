"""Capture transparent cut-outs of the Soundbox and phone screens for the storytelling deck."""
import os, re
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "deck", "img"); os.makedirs(OUT, exist_ok=True)
# hand-drawn shop illustration as its own file
html = open(os.path.join(ROOT, "public", "index.html"), encoding="utf-8").read()
svg = re.search(r'<svg class="hero-art".*?</svg>', html, re.S).group(0).replace('class="hero-art" ', 'xmlns="http://www.w3.org/2000/svg" ')
open(os.path.join(OUT, "shop.svg"), "w", encoding="utf-8").write(svg)

CLEAR = "document.documentElement.style.background='transparent';document.body.style.background='transparent';"
def pin(pg):
    for k in "1234": pg.click(f"#keypad button:text-is('{k}')")
    pg.wait_for_timeout(800)
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    pg = b.new_page(viewport={"width": 1100, "height": 1100}, device_scale_factor=2)
    phone = pg.locator(".phone")
    def snap(loc, name):
        pg.evaluate(CLEAR)
        if name.startswith("soundbox"):  # the 3D box spills outside its element: capture with room around it
            pg.add_style_tag(content="body *{visibility:hidden!important} .scene, .scene *{visibility:visible!important}")
            bb = loc.bounding_box(); m = 70
            pg.screenshot(path=os.path.join(OUT, name), omit_background=True, clip={"x": max(0, bb["x"] - m), "y": max(0, bb["y"] - m), "width": bb["width"] + 2 * m, "height": bb["height"] + 2 * m})
            from PIL import Image
            im = Image.open(os.path.join(OUT, name)); im.crop(im.getbbox()).save(os.path.join(OUT, name))
            pg.evaluate("document.querySelectorAll('style').forEach(s => { if (s.textContent.includes('visibility:hidden!important')) s.remove(); })")
        else:
            loc.screenshot(path=os.path.join(OUT, name), omit_background=True)
    nxt = lambda: (pg.click("#jNext"), pg.wait_for_timeout(450))
    pg.goto("http://localhost:3000", wait_until="load"); pg.wait_for_timeout(1000)
    pg.click("[data-pick=ta]"); pg.wait_for_timeout(500); pg.click("#getStarted"); pg.wait_for_timeout(3500)
    snap(pg.locator(".scene"), "soundbox.png"); snap(phone, "p-home.png")
    pg.click("[data-go=pongal]"); pg.wait_for_timeout(500); snap(phone, "p-short.png")
    nxt(); nxt(); snap(phone, "p-remind.png"); nxt(); pg.check("#consent"); pg.wait_for_timeout(200); nxt(); nxt(); pg.wait_for_timeout(500)
    snap(phone, "p-pin.png"); pin(pg); pg.wait_for_timeout(600); snap(phone, "p-done.png")
    pg.click("#doneHome"); pg.wait_for_timeout(500); snap(pg.locator(".scene"), "soundbox-on.png")
    pg.click(".tab[data-tab=Savings]"); pg.wait_for_timeout(700); snap(phone, "p-score.png")
    pg.click(".tab[data-tab=Udhaar]"); pg.wait_for_timeout(700); snap(phone, "p-udhaar.png")
    pg.click("[data-go='flow:miss']"); pg.wait_for_timeout(400); nxt(); pg.click("[data-set=fix][data-val=save]"); pg.wait_for_timeout(400); snap(phone, "p-miss.png")
    pg.click("#jClose"); pg.wait_for_timeout(400)
    pg.click(".tab[data-tab=Loans]"); pg.wait_for_timeout(500); pg.click("#rainBtn"); pg.wait_for_timeout(1200); snap(phone, "p-rain.png")
    pg.click(".tab[data-tab=Home]"); pg.wait_for_timeout(600)
    pg.click("[data-go='flow:fund']"); pg.wait_for_timeout(400); nxt(); snap(phone, "p-fund.png"); pg.click("#jClose"); pg.wait_for_timeout(400)
    pg.click("[data-go='flow:circle']"); pg.wait_for_timeout(400); nxt(); snap(phone, "p-circle.png"); pg.click("#jClose"); pg.wait_for_timeout(400)
    pg.click("[data-go='flow:bill']"); pg.wait_for_timeout(400); pg.click("#billSample"); pg.wait_for_selector("#jStep:has-text('Step 2')", timeout=60000); pg.wait_for_timeout(600); snap(phone, "p-bill.png")
    pg.click("#jClose"); pg.wait_for_timeout(400)
    pg.click("[data-go='flow:staff']"); pg.wait_for_timeout(500); nxt(); snap(phone, "p-staff.png"); pg.click("#jClose"); pg.wait_for_timeout(400)
    pg.click("[data-go='flow:galla']"); pg.wait_for_timeout(400); pg.click("[data-set=counted][data-val='3050']"); pg.wait_for_timeout(200); nxt(); snap(phone, "p-galla.png"); pg.click("#jClose"); pg.wait_for_timeout(400)
    pg.click(".tab[data-tab=Udhaar]"); pg.wait_for_timeout(500); pg.click("#paneUdhaar .bh-card"); pg.wait_for_timeout(400); snap(phone, "p-bharosa.png"); nxt(); snap(phone, "p-bharosa2.png"); pg.click("#jClose"); pg.wait_for_timeout(400)
    pg.click("#paneUdhaar .p-add"); pg.wait_for_timeout(400); nxt(); snap(phone, "p-confirm.png")
    b.close()
print("captured:", sorted(f for f in os.listdir(OUT)))
