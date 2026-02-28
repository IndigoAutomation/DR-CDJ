# Changelog

Tutte le modifiche notevoli a questo progetto saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e questo progetto aderisce a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Supporto iniziale per profili CDJ multipli (NXS1, NXS2, CDJ-3000)
- GUI moderna con dark mode usando CustomTkinter
- Drag-and-drop nativo per file e cartelle
- Analisi audio via ffprobe con parsing JSON
- Motore di compatibilità per CDJ-2000 Nexus
- Conversione automatica via FFmpeg con logica ottimale
- Batch processing con progress bar
- Supporto formati: MP3, AAC, WAV, AIFF, FLAC, OGG, OPUS, WMA, ALAC
- CLI completa con output JSON
- Test suite completa con pytest
- Bundling con PyInstaller per Windows, macOS, Linux

## [0.1.0] - 2026-02-28

### Added
- 🎉 Release iniziale di CDJ-Check
- Verifica compatibilità per Pioneer CDJ-2000 Nexus
- Conversione intelligente preservando massima qualità
- GUI drag-and-drop con CustomTkinter
- CLI per scripting e automazione
- Supporto batch processing
- Dark mode default
- Cross-platform: Windows, macOS, Linux

### Notes
- Versione alpha — feedback benvenuto!
- Target: DJ professionisti e producer

---

## Template per Future Release

```
## [X.Y.Z] - YYYY-MM-DD

### Added
- Nuove feature

### Changed
- Modifiche a feature esistenti

### Deprecated
- Feature che verranno rimosse

### Removed
- Feature rimosse

### Fixed
- Bugfix

### Security
- Fix di sicurezza
```

[Unreleased]: https://github.com/filippoitaliano/cdj-check/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/filippoitaliano/cdj-check/releases/tag/v0.1.0
