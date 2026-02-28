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
```

## Key Gotchas

- **FFmpeg bundling**: Run `python scripts/download-ffmpeg.py` before `python build.py` to embed FFmpeg in the .app. Without this, the app auto-downloads FFmpeg on first launch.
- **macOS error dialogs** use `osascript` (not tkinter), so they work even before Tk loads.
- **Entry point**: `dr-cdj` CLI script maps to `dr_cdj.main:main` (see `pyproject.toml`).
- **Logs** are written to `$TMPDIR/Dr-CDJ-Logs/app.log`.

## Environment

- Python 3.11+
- FFmpeg 6.x+ (for local dev; bundled in release builds)
- macOS primary target; Linux/Windows partially supported
