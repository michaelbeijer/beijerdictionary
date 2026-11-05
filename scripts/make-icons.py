"""Regenerate the Beijer Dictionary mark: the browser-tab icons and the logo
the header shows (which is favicon.svg itself).

    python scripts/make-icons.py

Writes public/favicon.svg, public/favicon.ico and public/apple-touch-icon.png,
and public/og-image.png, the picture a chat app or social site shows when a
link to the site is pasted.

The mark (chosen 2026-11-05, "option C" of the design review): a lower-case
b and d drawn as mirror images, two letters facing each other like a source
and a target language, in white strokes on a bottle-green rounded square
(#1E6B47, the site's accent). It is drawn from two lines and two circles
rather than a font, so it stays crisp at 16 pixels and needs no font file.
It replaced a white "Bd" in Arial Bold on a green gradient disc, which was
one of a family with Supervertaler's "Sv" and MemDesk's "Md"; this mark
leaves that family.

Requires Pillow.
"""
import os
import re

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(ROOT, "public")
GREEN = "#1E6B47"                         # the site's accent (themes.css)
SIZES = [16, 24, 32, 48, 64, 128, 256]

# The mark in its 256 box. The tile is a rounded square; the b's stem is on
# the left with its bowl to the right, the d mirrors it, and the two bowls
# touch in the middle.
TILE, TILE_RADIUS = (8, 8, 248, 248), 56
STROKE = 28
STEMS = [(56, 70, 186), (200, 70, 186)]   # x, top, bottom
BOWLS = [(92, 150), (164, 150)]           # centres
BOWL_R = 36

M = 1024                                  # master raster size


def rgb(hexcolour):
    return tuple(int(hexcolour[i:i + 2], 16) for i in (1, 3, 5))


# --------------------------------------------------------------- the raster
def draw_mark(full_bleed=False):
    """The mark at M x M. Drawn at 4x and downsampled for clean edges.
    `full_bleed` fills the whole square (iOS rounds the corners itself)."""
    n = M * 4
    k = n / 256.0
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if full_bleed:
        d.rectangle([0, 0, n, n], fill=rgb(GREEN))
    else:
        x0, y0, x1, y1 = TILE
        d.rounded_rectangle([x0 * k, y0 * k, x1 * k, y1 * k], radius=TILE_RADIUS * k, fill=rgb(GREEN))
    # Shapes rather than thick lines: Pillow's wide lines and ellipse
    # outlines leave notches where they meet a round end. A stem is a bar
    # with round ends; a bowl is a white disc with a green disc inside it.
    # The inner discs touch the stems and each other but never overlap them,
    # so painting them last can't cut into anything.
    white = (255, 255, 255, 255)
    h = STROKE * k / 2
    for x, top, bottom in STEMS:
        d.rounded_rectangle([x * k - h, top * k - h, x * k + h, bottom * k + h], radius=h, fill=white)
    for cx, cy in BOWLS:
        r = BOWL_R * k + h
        d.ellipse([cx * k - r, cy * k - r, cx * k + r, cy * k + r], fill=white)
    for cx, cy in BOWLS:
        r = BOWL_R * k - h
        d.ellipse([cx * k - r, cy * k - r, cx * k + r, cy * k + r], fill=rgb(GREEN) + (255,))
    return im.resize((M, M), Image.LANCZOS)


src = draw_mark()
src.resize((256, 256), Image.LANCZOS).save(os.path.join(PUBLIC, "favicon.ico"), format="ICO",
                                           sizes=[(s, s) for s in SIZES])
# iOS rounds the corners of a home-screen icon itself and shows any
# transparency as black, so this one fills the whole square.
draw_mark(full_bleed=True).resize((180, 180), Image.LANCZOS).convert("RGB").save(
    os.path.join(PUBLIC, "apple-touch-icon.png"))


# ------------------------------------------------------- the link preview
# What WhatsApp, LinkedIn, Slack, iMessage and X show when a link is pasted;
# Base.astro names it in every page. The mark alone, large, on the site's
# light-mode ground. WhatsApp's small preview is the middle square of the
# picture, shrunk to about 115 pixels and saved as a rough JPEG: a mark with
# the name and tagline under it came out small and soft there. The apps print
# the page title beside the picture, so the name is there anyway.
with open(os.path.join(ROOT, "src", "styles", "themes.css"), encoding="utf-8") as f:
    ground = re.search(r":root\s*\{[^}]*?--bg:\s*(\d+),\s*(\d+),\s*(\d+);", f.read())
OG_W, OG_H, OG_MARK = 1200, 630, 500      # the mark's 256 box
card = Image.new("RGB", (OG_W, OG_H), tuple(int(v) for v in ground.groups()))
big = src.resize((OG_MARK, OG_MARK), Image.LANCZOS)
card.paste(big, ((OG_W - OG_MARK) // 2, (OG_H - OG_MARK) // 2), big)
card.save(os.path.join(PUBLIC, "og-image.png"), optimize=True)


# ------------------------------------------------------------------ the SVG
x0, y0, x1, y1 = TILE
shapes = "\n    ".join(
    ['<line x1="%d" y1="%d" x2="%d" y2="%d"/>' % (x, top, x, bottom) for x, top, bottom in STEMS]
    + ['<circle cx="%d" cy="%d" r="%d"/>' % (cx, cy, BOWL_R) for cx, cy in BOWLS])
# A green tile stays visible on a dark tab strip, so no dark-mode rule.
SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
  <!-- Generated by scripts/make-icons.py - do not edit by hand.
       The browser-tab icon, and the logo in the site header. -->
  <rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="%s"/>
  <g fill="none" stroke="#ffffff" stroke-width="%d" stroke-linecap="round">
    %s
  </g>
</svg>
"""
with open(os.path.join(PUBLIC, "favicon.svg"), "w", encoding="utf-8", newline="\n") as f:
    f.write(SVG % (x0, y0, x1 - x0, y1 - y0, TILE_RADIUS, GREEN, STROKE, shapes))
print("favicon.svg, favicon.ico (%s), apple-touch-icon.png (180), og-image.png in %s" % (
    ", ".join(str(s) for s in SIZES), PUBLIC))
