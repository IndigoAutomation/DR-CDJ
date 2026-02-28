# 🚀 Release Checklist

## Pre-Release

- [ ] Versione aggiornata in `pyproject.toml`
- [ ] Versione aggiornata in `setup.py`
- [ ] Changelog aggiornato
- [ ] Test passano: `pytest`
- [ ] Linting OK: `ruff check src/`

## Build

### macOS
```bash
# Pulizia
rm -rf build dist

# Build
pyinstaller CDJ-Check.spec

# Verifica icona
ls -la dist/CDJ-Check.app/Contents/Resources/*.icns

# Crea DMG
./create-dmg.sh
```

### Linux
```bash
# Build AppImage (richiede appimagetool)
pyinstaller --onefile src/cdj_check/gui.py
# ... converti in AppImage
```

### Windows
```bash
# Build EXE
pyinstaller --windowed --icon=assets/logo_256.ico CDJ-Check.spec
```

## GitHub Release

1. Crea tag: `git tag -a v1.0.0 -m "Release v1.0.0"`
2. Push tag: `git push origin v1.0.0`
3. Vai su GitHub → Releases → Draft new release
4. Seleziona tag `v1.0.0`
5. Aggiungi release notes
6. Upload assets:
   - CDJ-Check-1.0.0-macOS.dmg
   - CDJ-Check-1.0.0-linux.AppImage
   - CDJ-Check-1.0.0-windows.exe

## Landing Page

Aggiorna landing page con:
- [ ] Link download latest
- [ ] Screenshot app
- [ ] Features highlights
- [ ] Installazione rapida

```html
<a href="https://github.com/tuousername/cdj-check/releases/latest/download/CDJ-Check-macOS.dmg">
  Download for macOS
</a>
```
