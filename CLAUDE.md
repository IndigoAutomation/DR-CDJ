# Dr. CDJ — CLAUDE.md

## Commands

```bash
# Run the app (dev)
python -m dr_cdj.main

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt   # dev tools

# Run tests
pytest

# Lint
ruff check src/ tests/

# Build standalone app (macOS)
python build.py          # downloads FFmpeg, runs PyInstaller
bash create-dmg.sh       # packages .app → .dmg
```

## Architecture

```
src/dr_cdj/
  main.py            # Entry point; logging setup, error dialog via osascript
  config.py          # CDJProfile / AudioFormat dataclasses + compatibility tables
  analyzer.py        # Reads audio metadata (calls ffprobe)
  compatibility.py   # Checks file against a CDJProfile
  converter.py       # Converts files via ffmpeg
  ffmpeg_downloader.py  # Auto-downloads FFmpeg at runtime if not bundled
  gui.py             # customtkinter UI (drag & drop, results table)
  splash.py          # Splash screen shown on startup

scripts/
  download-ffmpeg.py   # Downloads FFmpeg binaries for bundling
  generate_icon.py     # Generates CDJ-Check.icns from the coral/dark palette

hooks/                 # PyInstaller runtime hooks (ffmpeg, tkinter)
assets/                # Source PNGs (logo_1024/512/256.png) and icon sources
docs/
  internal/            # Release checklist, GitHub setup, landing page HTML
  assets/              # logo.svg
INSTALL.html           # Install guide bundled inside the .dmg (shown to user on mount)
```

## Key Gotchas

- **FFmpeg bundling**: Run `python scripts/download-ffmpeg.py` before `python build.py` to embed FFmpeg in the .app. Without this, the app auto-downloads FFmpeg on first launch.
- **macOS error dialogs** use `osascript` (not tkinter), so they work even before Tk loads.
- **Entry point**: `dr-cdj` CLI script maps to `dr_cdj.main:main` (see `pyproject.toml`).
- **Logs** are written to `$TMPDIR/Dr-CDJ-Logs/app.log`.
- **Icon update shortcut**: To change only the icon without a full PyInstaller rebuild, replace `CDJ-Check.icns`, copy it into `dist/Dr-CDJ.app/Contents/Resources/`, then re-run `bash create-dmg.sh`. Regenerate the icns with: `python scripts/generate_icon.py && iconutil -c icns CDJ-Check.iconset -o CDJ-Check.icns`

## Release Workflow

```bash
# 1. (Optional) rebuild the app
python scripts/download-ffmpeg.py   # embed FFmpeg
python build.py                     # PyInstaller → dist/Dr-CDJ.app

# 2. (Optional) regenerate icon only
python scripts/generate_icon.py
iconutil -c icns CDJ-Check.iconset -o CDJ-Check.icns
cp CDJ-Check.icns dist/Dr-CDJ.app/Contents/Resources/CDJ-Check.icns

# 3. Package DMG (always needed for distribution)
bash create-dmg.sh                  # produces Dr-CDJ-{VERSION}-macOS.dmg
```

## Environment

- Python 3.11+
- FFmpeg 6.x+ (for local dev; bundled in release builds)
- macOS primary target; Linux/Windows partially supported
