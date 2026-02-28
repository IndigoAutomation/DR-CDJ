#!/usr/bin/env python3
"""Generate Dr. CDJ app icon — coral/dark theme, matches landing page palette."""
import os, sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter
except ImportError:
    os.system(f"{sys.executable} -m pip install Pillow --quiet")
    from PIL import Image, ImageDraw, ImageFilter

ROOT    = Path(__file__).parent.parent
ICONSET = ROOT / "CDJ-Check.iconset"
ASSETS  = ROOT / "assets"

# Palette (matches landing page CSS vars)
DARK_BG    = (9,   9,  14)
CORAL      = (217, 79,  79)
CORAL_HI   = (235, 112, 102)
PEACH      = (201, 100,  24)
GROOVE     = (10,   8,  15)
CENTER_LBL = (16,  12,  22)
SPINDLE_HI = (255, 200, 185)


def rounded_mask(size: int, radius_pct: float = 0.225) -> Image.Image:
    mask = Image.new("L", (size, size), 0)
    md   = ImageDraw.Draw(mask)
    r    = int(size * radius_pct)
    try:
        md.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=255)
    except AttributeError:
        # Pillow < 8.2 fallback
        md.rectangle([r, 0, size - r - 1, size - 1], fill=255)
        md.rectangle([0, r, size - 1, size - r - 1], fill=255)
        for px, py in [(r, r), (size-r-1, r), (r, size-r-1), (size-r-1, size-r-1)]:
            md.ellipse([px - r, py - r, px + r, py + r], fill=255)
    return mask


def draw_icon(size: int) -> Image.Image:
    cx = cy = size // 2

    # ── Background with subtle warm centre glow ──────────────────
    base = Image.new("RGBA", (size, size), (*DARK_BG, 255))
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gd   = ImageDraw.Draw(glow)
    gr   = int(size * 0.46)
    gd.ellipse([cx - gr, cy - gr, cx + gr, cy + gr], fill=(*CORAL, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=max(1, size // 6)))
    img  = Image.alpha_composite(base, glow)

    draw = ImageDraw.Draw(img)

    def circle(pct: float, color: tuple):
        r = int(size * pct)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color, 255))

    # ── CDJ disc — rings painted outside-in ──────────────────────
    circle(0.456, CORAL_HI)          # outer edge highlight
    circle(0.440, CORAL)             # outer ring
    circle(0.360, GROOVE)            # groove 1
    circle(0.325, PEACH)             # mid ring
    circle(0.265, GROOVE)            # groove 2
    circle(0.205, (182, 55, 55))     # inner ring (deeper coral)
    circle(0.152, GROOVE)            # groove 3
    circle(0.105, CENTER_LBL)        # centre label (dark area)

    # ── Checkmark in centre label ────────────────────────────────
    if size >= 64:
        s   = size * 0.042
        lw  = max(2, int(size * 0.012))
        p1  = (cx - s * 1.00, cy + s * 0.10)
        p2  = (cx - s * 0.20, cy + s * 0.92)
        p3  = (cx + s * 1.30, cy - s * 0.85)
        draw.line([p1, p2, p3], fill=(255, 255, 255, 215), width=lw)

    # ── Spindle (tiny, barely visible under checkmark) ───────────
    circle(0.015, (*CORAL_HI,))
    circle(0.006, SPINDLE_HI)

    # ── macOS rounded-rect mask ──────────────────────────────────
    img.putalpha(rounded_mask(size))

    return img


ICONSET_FILES = {
    "icon_16x16.png":       16,
    "icon_16x16@2x.png":    32,
    "icon_32x32.png":       32,
    "icon_32x32@2x.png":    64,
    "icon_128x128.png":    128,
    "icon_128x128@2x.png": 256,
    "icon_256x256.png":    256,
    "icon_256x256@2x.png": 512,
    "icon_512x512.png":    512,
    "icon_512x512@2x.png":1024,
}

if __name__ == "__main__":
    ICONSET.mkdir(exist_ok=True)
    ASSETS.mkdir(exist_ok=True)

    cache: dict = {}
    for fname, sz in ICONSET_FILES.items():
        if sz not in cache:
            print(f"  rendering {sz}×{sz}…", flush=True)
            cache[sz] = draw_icon(sz)
        cache[sz].save(ICONSET / fname)
        print(f"  ✓  {fname}")

    cache[1024].save(ASSETS / "logo_1024.png")
    cache[512].save(ASSETS / "logo_512.png")
    cache[256].save(ASSETS / "logo_256.png")
    print("  ✓  assets/logo_*.png")
    print("\nDone.")
