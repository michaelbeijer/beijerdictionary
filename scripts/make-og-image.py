"""Regenerate the link-preview image: what WhatsApp, LinkedIn, Slack, iMessage
and X show when a link to the site is pasted.

    python scripts/make-og-image.py

Writes public/og-image.png (1200x630), which Base.astro names in every page's
og:image and twitter:image. The path is fixed on purpose: previews already
shared keep pointing at it, so overwrite the file rather than renaming it.

Without an og:image these apps stretch the 180-pixel apple-touch-icon, which
is why previews looked blurry. Three things the apps need:

- 1200x630, the size LinkedIn, Slack and X show as a large card.
- Everything that matters inside the central 630x630 square, because WhatsApp
  and others sometimes show a square cut from the middle instead.
- Under 300 KB, or WhatsApp shows no image at all. This script refuses to
  write a bigger one.

The look is the site's light mode: its stone and ink colours, read from
src/styles/themes.css, and the Bd mark from public/favicon.ico (made by
scripts/make-icons.py; run that first if the mark changes). The site's font,
Inter, comes from Google Fonts and is not installed here, so the text is in
Arial, the font of the mark. Text is drawn at twice the size and scaled down,
so it stays crisp.

Requires Pillow and Arial - so, in practice, Windows.
"""
import io
import os
import re

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "og-image.png")
ICON = os.path.join(ROOT, "public", "favicon.ico")
THEMES = os.path.join(ROOT, "src", "styles", "themes.css")
BOLD = r"C:\Windows\Fonts\arialbd.ttf"
REGULAR = r"C:\Windows\Fonts\arial.ttf"

NAME = "Beijer Dictionary"
TAGLINE = ["Multilingual terminology", "for technical translators"]
DOMAIN = "beijerdictionary.com"

W, H = 1200, 630
SS = 2                        # drawn at twice the size, then scaled down
SAFE = 630                    # the central square a crop may keep
MAX_BYTES = 300 * 1024        # WhatsApp drops larger images


def theme():
    """The light-mode colours, from the :root block of themes.css."""
    with open(THEMES, encoding="utf-8") as f:
        css = f.read()
    root = re.search(r":root\s*\{(.*?)\}", css, re.S).group(1)
    colours = {}
    for name in ("bg", "text", "muted", "brand"):
        m = re.search(r"--%s:\s*(\d+),\s*(\d+),\s*(\d+);" % name, root)
        if not m:
            raise SystemExit("themes.css: no --%s in :root" % name)
        colours[name] = tuple(int(v) for v in m.groups())
    return colours


def mark(size):
    """The Bd mark at `size` pixels square, scaled down from the 256 icon."""
    ico = Image.open(ICON)
    ico.size = (256, 256)                 # pick the largest of the ICO's sizes
    ico.load()
    if size > 256:
        raise SystemExit("the mark would be scaled up, and blur")
    return ico.convert("RGBA").resize((size, size), Image.LANCZOS)


def main():
    c = theme()
    img = Image.new("RGB", (W * SS, H * SS), c["bg"])
    d = ImageDraw.Draw(img)

    def font(path, px):
        return ImageFont.truetype(path, px * SS)

    name_f = font(BOLD, 68)
    tag_f = font(REGULAR, 34)
    domain_f = font(BOLD, 28)

    # One centred column: the mark, then each line with the space above it
    # (final pixels, from the previous line's descenders to this line's
    # capitals). Every line of a font gets the same cap height and descender,
    # so a line without a "g" or "y" is not set closer to the next.
    mark_px = 184                         # the icon's box; the disc is 7/8 of it
    lines = [(NAME, name_f, c["text"], 30)]
    lines += [(t, tag_f, c["muted"], 30 if i == 0 else 12) for i, t in enumerate(TAGLINE)]
    lines += [(DOMAIN, domain_f, c["brand"], 34)]

    def extent(f):
        cap = -f.getbbox("H", anchor="ls")[1] / SS
        desc = f.getbbox("gjpqy", anchor="ls")[3] / SS
        return cap, desc

    height = mark_px + sum(gap + sum(extent(f)) for _, f, _, gap in lines)
    mark_top = (H - height) / 2.0 - 6     # a touch above centre looks centred
    y = mark_top + mark_px
    cx = W * SS / 2.0
    for text, f, colour, gap in lines:
        cap, desc = extent(f)
        y += gap + cap
        d.text((cx, y * SS), text, font=f, fill=colour, anchor="ms")
        y += desc
        width = d.textlength(text, font=f) / SS
        if width > SAFE - 60:
            raise SystemExit("%r is %d px wide; it must fit the central %d px square"
                             % (text, width, SAFE))

    img = img.resize((W, H), Image.LANCZOS)
    m = mark(mark_px)
    img.paste(m, (int(round((W - mark_px) / 2.0)), int(round(mark_top))), m)

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    if buf.tell() > MAX_BYTES:
        raise SystemExit("og-image.png would be %d KB; WhatsApp drops images over 300 KB"
                         % (buf.tell() // 1024))
    with open(OUT, "wb") as f:
        f.write(buf.getvalue())
    print("og-image.png (%dx%d, %d KB) in %s" % (W, H, buf.tell() // 1024, os.path.dirname(OUT)))


if __name__ == "__main__":
    main()
