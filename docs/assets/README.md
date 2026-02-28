# Assets Directory

This directory contains visual assets for CDJ-Check.

## Files

- `logo.svg` - Main project logo (SVG format)
- `logo.png` - Main project logo (PNG format, 512x512) - *To be generated*
- `screenshot-main.png` - Main GUI screenshot - *To be added*
- `screenshot-analysis.png` - Batch analysis screenshot - *To be added*
- `screenshot-conversion.png` - Conversion screen screenshot - *To be added*

## Generating PNG from SVG

```bash
# Using Inkscape
inkscape logo.svg --export-type=png --export-width=512 --export-height=512

# Using ImageMagick
convert -background none logo.svg -resize 512x512 logo.png
```
