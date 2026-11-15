"""Minimal hand-drawn gold coin illustration (no AI image generation). Used on the app welcome screen and the deck cover."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def coin(cx, cy, r, edge, sym, op=1):
    return f'''<g opacity="{op}">
  <ellipse cx="{cx}" cy="{cy+edge}" rx="{r}" ry="{r}" fill="url(#cEdge)"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#cFace)"/>
  <circle cx="{cx}" cy="{cy}" r="{r*.8:.1f}" fill="none" stroke="#e59a12" stroke-width="{max(1.5, r*.035):.1f}" opacity=".55"/>
  <path d="M{cx-r*.72:.1f} {cy-r*.3:.1f}A{r*.78:.1f} {r*.78:.1f} 0 0 1 {cx+r*.3:.1f} {cy-r*.72:.1f}" stroke="#fff" stroke-width="{r*.07:.1f}" stroke-linecap="round" fill="none" opacity=".55"/>
  <text x="{cx}" y="{cy + r*.36:.1f}" text-anchor="middle" font-size="{r*1.05:.0f}" font-weight="700" fill="#b86e00" font-family="Inter, Segoe UI, Arial, sans-serif">{sym}</text>
</g>'''

def spark(x, y, s, c):
    return f'<path d="M{x} {y-s}C{x+s*.15} {y-s*.15} {x+s*.15} {y-s*.15} {x+s} {y}C{x+s*.15} {y+s*.15} {x+s*.15} {y+s*.15} {x} {y+s}C{x-s*.15} {y+s*.15} {x-s*.15} {y+s*.15} {x-s} {y}C{x-s*.15} {y-s*.15} {x-s*.15} {y-s*.15} {x} {y-s}z" fill="{c}"/>'

svg = f'''<svg viewBox="0 0 400 320" xmlns="http://www.w3.org/2000/svg">
<defs>
  <radialGradient id="cFace" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#fff3b8"/><stop offset=".45" stop-color="#ffd257"/><stop offset="1" stop-color="#f0a21c"/></radialGradient>
  <linearGradient id="cEdge" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d98a10"/><stop offset="1" stop-color="#a86200"/></linearGradient>
  <radialGradient id="cGlow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#7fe0ff" stop-opacity=".45"/><stop offset="1" stop-color="#7fe0ff" stop-opacity="0"/></radialGradient>
</defs>
<circle cx="200" cy="160" r="160" fill="url(#cGlow)"/>
<ellipse cx="206" cy="292" rx="120" ry="12" fill="#011a48" opacity=".18"/>
<circle cx="200" cy="160" r="134" fill="none" stroke="#00baf2" stroke-width="1.5" stroke-dasharray="2 8" stroke-linecap="round" opacity=".7"/>
{coin(96, 92, 26, 6, "₹", .95)}
{coin(318, 236, 34, 7, "₹")}
{coin(200, 150, 100, 16, "₹")}
{spark(326, 86, 12, "#ffffff")}{spark(82, 226, 9, "#00baf2")}{spark(286, 50, 6, "#ffd257")}
</svg>'''

open(os.path.join(ROOT, "public", "deck", "img", "coin.svg"), "w", encoding="utf-8").write(svg)
p = os.path.join(ROOT, "public", "index.html"); t = open(p, encoding="utf-8").read()
inline = svg.replace('<svg viewBox="0 0 400 320" xmlns="http://www.w3.org/2000/svg">',
    '<svg class="hero-art" viewBox="0 0 400 320" role="img" aria-label="A gold rupee coin: Kaasu keeps your shop\'s money safe and planned">')
t, n = re.subn(r'<svg class="hero-art".*?</svg>', lambda m: inline, t, count=1, flags=re.S)
assert n == 1
open(p, "w", encoding="utf-8").write(t)
print("coin done")
