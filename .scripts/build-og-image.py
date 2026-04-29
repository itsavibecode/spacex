"""
Build the SpaceX IPO Tracker Open Graph image.

Output: T:/ClaudeCodeRepo/spacex/og-image.png  (1200x630, the size every share
target expects)

Also outputs apple-touch-icon.png at 180x180 for iOS home-screen previews.

Run from T:\\ClaudeCodeRepo\\spacex with:
    python .scripts/build-og-image.py
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT_OG = REPO / "og-image.png"
OUT_APPLE = REPO / "apple-touch-icon.png"

# Palette — matches the live site (var(--bg) etc.)
BG       = (11, 13, 18)        # #0b0d12
PANEL    = (20, 24, 33)        # #141821
LINE     = (51, 58, 74)        # #333a4a
INK      = (242, 244, 248)     # #f2f4f8
INK_DIM  = (168, 176, 192)     # #a8b0c0
INK_FAINT= (107, 115, 133)     # #6b7385
ACCENT   = (255, 107, 71)      # #ff6b47
ACCENT2  = (255, 200, 87)      # #ffc857

FONTS = "C:/Windows/Fonts"
def f(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}", size)

def text_size(draw, text, font):
    """Return (w, h) for a text string."""
    l, t, r, b = draw.textbbox((0, 0), text, font=font)
    return r - l, b - t

# -----------------------------------------------------------------------------
# Open Graph image — 1200 x 630
# -----------------------------------------------------------------------------
W, H = 1200, 630
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img, "RGBA")

# Inset frame (subtle, like the panel borders on the site)
PAD = 48
d.rounded_rectangle([PAD, PAD, W - PAD, H - PAD], radius=24,
                    outline=LINE, width=2)

# --- Brand row (top-left) ---------------------------------------------------
brand_x, brand_y = PAD + 36, PAD + 36
# Pulse dot
d.ellipse([brand_x, brand_y + 10, brand_x + 12, brand_y + 22], fill=ACCENT)
# Brand text
brand_font = f("Inter-SemiBold.ttf", 22)
d.text((brand_x + 22, brand_y + 4), "SpaceX IPO", font=brand_font, fill=INK)
slash_w, _ = text_size(d, "SpaceX IPO", brand_font)
d.text((brand_x + 22 + slash_w + 10, brand_y + 4), "/  Tracker",
       font=brand_font, fill=INK_FAINT)

# Status pill (top-right)
status_text = "UNCONFIRMED · TARGET WINDOW"
status_font = f("Inter-SemiBold.ttf", 14)
sw, sh = text_size(d, status_text, status_font)
sp_x2 = W - PAD - 36
sp_y = PAD + 36
d.rounded_rectangle([sp_x2 - sw - 28, sp_y, sp_x2, sp_y + sh + 14],
                    radius=999, outline=LINE, width=1)
# small dot
d.ellipse([sp_x2 - sw - 22, sp_y + sh/2 + 1, sp_x2 - sw - 14, sp_y + sh/2 + 9],
          fill=ACCENT2)
d.text((sp_x2 - sw - 4, sp_y + 6), status_text, font=status_font, fill=ACCENT2)

# --- Big date hero ----------------------------------------------------------
date_font = f("ariblk.ttf", 140)  # Arial Black — heaviest sans on Windows
date_text = "JUNE 2026"
dw, _ = text_size(d, date_text, date_font)
ascent, descent = date_font.getmetrics()
date_visual_height = ascent + descent
date_y = 180
d.text(((W - dw) / 2, date_y), date_text, font=date_font, fill=INK)

# Subtitle under the date, with breathing room based on the font's true height
sub_font = f("Inter-Medium.ttf", 24)
sub_text = "Roadshow week of June 8  ·  Pricing window June 18–30"
sw2, _ = text_size(d, sub_text, sub_font)
d.text(((W - sw2) / 2, date_y + date_visual_height + 8),
       sub_text, font=sub_font, fill=INK_DIM)

# --- Bottom row: ticker pill + price benchmark ------------------------------
row_y = H - PAD - 36 - 110

# Ticker pill (left)
tk_x = PAD + 36
tk_w, tk_h = 280, 110
d.rounded_rectangle([tk_x, row_y, tk_x + tk_w, row_y + tk_h],
                    radius=14, fill=PANEL, outline=LINE, width=1)

lbl_font = f("Inter-SemiBold.ttf", 13)
d.text((tk_x + 22, row_y + 18), "LIKELY TICKER", font=lbl_font, fill=INK_DIM)

ticker_font = f("consolab.ttf", 44)
d.text((tk_x + 22, row_y + 40), "$SPCX", font=ticker_font, fill=ACCENT)

exch_font = f("consolab.ttf", 13)
ew, eh = text_size(d, "NASDAQ", exch_font)
d.rounded_rectangle([tk_x + tk_w - 22 - ew - 12, row_y + 18,
                     tk_x + tk_w - 22, row_y + 18 + eh + 6],
                    radius=4, fill=(255, 200, 87, 30))
d.text((tk_x + tk_w - 22 - ew - 6, row_y + 19), "NASDAQ",
       font=exch_font, fill=ACCENT2)

# Price benchmark (right)
pr_w = 540
pr_x = W - PAD - 36 - pr_w
d.rounded_rectangle([pr_x, row_y, pr_x + pr_w, row_y + tk_h],
                    radius=14, fill=PANEL, outline=LINE, width=1)
d.text((pr_x + 26, row_y + 18), "IPO PRICE BENCHMARK",
       font=lbl_font, fill=INK_DIM)
price_font = f("ariblk.ttf", 56)
d.text((pr_x + 26, row_y + 38), "~$525–$530",
       font=price_font, fill=ACCENT2)

# --- Footer URL -------------------------------------------------------------
url_font = f("Inter-Medium.ttf", 18)
url_text = "spacex.bookhockeys.com"
uw, uh = text_size(d, url_text, url_font)
d.text(((W - uw) / 2, H - PAD - 18 - uh),
       url_text, font=url_font, fill=INK_FAINT)

img.save(OUT_OG, "PNG", optimize=True)
print(f"Wrote {OUT_OG}  ({OUT_OG.stat().st_size // 1024} KB)")

# -----------------------------------------------------------------------------
# Apple touch icon — 180 x 180 (rocket silhouette on dark)
# -----------------------------------------------------------------------------
S = 180
icon = Image.new("RGB", (S, S), BG)
di = ImageDraw.Draw(icon)
# Rounded background
di.rounded_rectangle([0, 0, S - 1, S - 1], radius=34, fill=BG)
# Rocket body (matches the inline SVG favicon shape)
body = [
    (90, 28),   # tip
    (118, 78),  # top-right shoulder
    (118, 130), # right wall
    (90, 148),  # bottom point
    (62, 130),  # left wall
    (62, 78),   # top-left shoulder
]
di.polygon(body, fill=ACCENT)
# Window
di.ellipse([81, 79, 99, 97], fill=BG)
# Fins (yellow)
di.polygon([(62, 130), (44, 160), (62, 142)], fill=ACCENT2)
di.polygon([(118, 130), (136, 160), (118, 142)], fill=ACCENT2)

icon.save(OUT_APPLE, "PNG", optimize=True)
print(f"Wrote {OUT_APPLE}  ({OUT_APPLE.stat().st_size // 1024} KB)")
