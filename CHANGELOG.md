# Changelog

Tutte le modifiche notevoli a questo progetto saranno documentate in questo file.

Il formato è basato su [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
e questo progetto aderisce a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Supporto completo per CDJ-3000, CDJ-2000 NXS2, CDJ-2000 Nexus, XDJ-1000 MK2, XDJ-700
- Dark mode automatica in base alle preferenze di sistema
- Splash screen all'avvio
- Auto-download di FFmpeg al primo avvio (macOS app)
- Supporto per conversione batch con progresso visivo

### Changed
- Migliorata la gestione degli errori durante la conversione
- Ottimizzata l'analisi audio con caching dei risultati
- Refactoring del motore di compatibilità per supportare più profili

### Fixed
- Risolto problema con file FLAC corrotti che causavano crash
- Fixato il timeout su file molto grandi
- Corretto il path di output su Windows con spazi nei nomi

## [1.0.1] - 2025-02-28

### Fixed
- Corretto il problema con il bundle FFmpeg su macOS
- Fixato il crash quando si trascinano cartelle con permessi limitati
- Migliorata la gestione della memoria durante conversioni batch

### Changed
- Aggiornata la UI con miglior contrasto per la dark mode
- Ottimizzato il tempo di avvio dell'applicazione

## [1.0.0] - 2025-02-15

### Added
- 🎉 **Prima release stabile di Dr. CDJ**
- Supporto multi-player: CDJ-2000 Nexus, CDJ-2000 NXS2, CDJ-3000, XDJ-1000 MK2, XDJ-700
- GUI moderna con dark mode usando CustomTkinter
- Drag-and-drop nativo per file e cartelle
- Analisi audio via ffprobe con parsing JSON
- Motore di compatibilità per tutti i profili CDJ supportati
- Conversione automatica via FFmpeg con logica ottimale
- Batch processing con progress bar e annullamento
- Supporto formati: MP3, AAC, WAV, AIFF, FLAC, OGG, OPUS, WMA, ALAC
- CLI completa con output JSON per automazione
- Test suite con pytest e coverage > 80%
- Bundling con PyInstaller per macOS
- Auto-download FFmpeg al primo avvio
- Splash screen durante l'inizializzazione

### Changed
- Migliorata l'UX della GUI con feedback visivi più chiari
- Ottimizzata la logica di conversione per preservare la massima qualità

### Fixed
- Risolti memory leak durante l'analisi di grandi librerie
- Fixato il problema con file path contenenti caratteri speciali

## [0.1.0] - 2025-01-20

### Added
- 🎉 Release iniziale alpha di Dr. CDJ
- Verifica compatibilità per Pioneer CDJ-2000 Nexus
- Conversione intelligente preservando massima qualità
- GUI drag-and-drop con CustomTkinter
- CLI per scripting e automazione
- Supporto batch processing
- Dark mode default
- Cross-platform: macOS

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

---

[Unreleased]: https://github.com/IndigoAutomation/DR-CDJ/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/IndigoAutomation/DR-CDJ/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/IndigoAutomation/DR-CDJ/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/IndigoAutomation/DR-CDJ/releases/tag/v0.1.0
