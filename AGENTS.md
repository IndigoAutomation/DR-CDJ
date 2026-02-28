# 🤖 Agents.md — Guida Operativa per CDJ-Check

> Questo file è il tuo riferimento principale per lavorare sul progetto **CDJ-Check**.
> **Stack:** Python 3.11+ · CustomTkinter · FFmpeg · pytest · Ruff

---

## 1. 🎵 Panoramica Progetto

**CDJ-Check** è un tool desktop per verificare e convertire file audio per la compatibilità con il Pioneer CDJ-2000 Nexus.

### Caratteristiche principali:
- **GUI drag-and-drop** con CustomTkinter (dark mode, look moderno)
- **Analisi audio** via ffprobe (codec, sample rate, bit depth, bitrate)
- **Motore di compatibilità** per CDJ-2000 Nexus (formati supportati: MP3, AAC, WAV, AIFF)
- **Conversione automatica** via FFmpeg (FLAC → WAV, resample 96kHz → 48kHz, etc.)
- **Cross-platform:** Windows, macOS, Linux

---

## 2. 🏗️ Architettura del Progetto

### Struttura Directory

```
cdj-check/
├── src/cdj_check/           # Codice sorgente principale
│   ├── __init__.py
│   ├── main.py              # Entry point CLI/GUI
│   ├── gui.py               # Interfaccia CustomTkinter + drag-and-drop
│   ├── analyzer.py          # Analisi audio con ffprobe
│   ├── compatibility.py     # Motore di compatibilità CDJ
│   ├── converter.py         # Conversione con FFmpeg
│   ├── config.py            # Costanti e configurazioni
│   └── utils.py             # Utility varie
├── tests/                   # Test suite (pytest)
├── hooks/                   # Hook PyInstaller
├── build.py                 # Script build bundle
├── CDJ-Check.spec           # Configurazione PyInstaller
├── pyproject.toml           # Configurazione progetto
├── requirements.txt         # Dipendenze runtime
└── requirements-dev.txt     # Dipendenze sviluppo
```

### Moduli Core

| Modulo | Responsabilità | Key Functions/Classes |
|--------|----------------|----------------------|
| `analyzer.py` | Estrazione metadati audio via ffprobe | `analyze_file()`, `AudioMetadata` |
| `compatibility.py` | Logica compatibilità CDJ-2000 Nexus | `check_compatibility()`, `CompatibilityResult` |
| `converter.py` | Conversione audio via FFmpeg | `convert_file()`, `ConversionJob` |
| `gui.py` | Interfaccia grafica CustomTkinter | `CDJCheckApp`, `FileListFrame` |
| `config.py` | Costanti, formati supportati, percorsi | `SUPPORTED_FORMATS`, `CDJ_PROFILES` |

### Stack Tecnologico

| Componente | Tecnologia | Versione | Scopo |
|------------|------------|----------|-------|
| Runtime | Python | 3.11+ | Linguaggio principale |
| GUI | CustomTkinter | 5.2+ | Interfaccia moderna dark mode |
| Drag & Drop | tkinterdnd2 | 0.3+ | Supporto DnD nativo |
| Audio Analysis | ffprobe | 6.x+ | Estrazione metadati |
| Audio Conversion | FFmpeg | 6.x+ | Transcoding audio |
| Testing | pytest | 7.0+ | Unit tests |
| Linting | Ruff | 0.1.0+ | Formattazione e linting |
| Bundling | PyInstaller | latest | Eseguibile standalone |

---

## 3. 🐍 Convenzioni di Codice Python

### Stile e Formattazione

- **Line length:** 100 caratteri (configurato in pyproject.toml)
- **Formatter:** Ruff (sostituisce Black + isort + flake8)
- **Docstring:** Google style convention
- **Type hints:** Obbligatori per funzioni pubbliche

### Comandi Ruff

```bash
# Check linting
ruff check src/

# Auto-format
ruff format src/

# Fix automatico issue
ruff check src/ --fix
```

### Pattern di Codice

**Named exports (no default export tranne main):**
```python
# ✅ CORRETTO
class AudioAnalyzer:
    pass

def analyze_file(path: Path) -> AudioMetadata:
    pass

# ❌ SBAGLIATO
default_analyzer = AudioAnalyzer()  # No singleton impliciti
```

**Gestione errori con try/except specifici:**
```python
# ✅ CORRETTO
try:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_format", str(path)],
        capture_output=True,
        text=True,
        timeout=30
    )
except subprocess.TimeoutExpired:
    raise AnalysisError(f"Timeout analizzando {path}")
except FileNotFoundError:
    raise AnalysisError("FFmpeg non trovato. Installa FFmpeg.")
```

**Pathlib invece di os.path:**
```python
# ✅ CORRETTO
from pathlib import Path
output_path = Path(input_path).parent / "CDJ_Ready" / f"{stem}.wav"

# ❌ SBAGLIATO
import os
output_path = os.path.join(os.path.dirname(input_path), "CDJ_Ready", filename)
```

**Subprocess con gestione sicura:**
```python
# ✅ CORRETTO - sempre timeout, check=True, cattura stderr
result = subprocess.run(
    cmd,
    capture_output=True,
    text=True,
    timeout=300,
    check=False  # Gestiamo errori manualmente per UX migliore
)
if result.returncode != 0:
    logger.error(f"FFmpeg error: {result.stderr}")
    raise ConversionError(f"Conversione fallita: {result.stderr}")
```

---

## 4. 🎯 Workflow di Sviluppo

### Setup Ambiente

```bash
# 1. Clona repo
cd cdj-check

# 2. Crea virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# oppure .venv\Scripts\activate  # Windows

# 3. Installa dipendenze
pip install -e ".[dev]"

# 4. Verifica FFmpeg installato
ffmpeg -version
ffprobe -version
```

### Ciclo di Sviluppo

```
1. Modifica codice in src/cdj_check/
2. Esegui test: pytest
3. Linting: ruff check src/
4. Formatta: ruff format src/
5. Test manuale GUI: python -m cdj_check.main --gui
6. Commit con convenzione (vedi sezione Git)
```

### Testing

```bash
# Esegui tutti i test
pytest

# Con coverage
pytest --cov=cdj_check --cov-report=html

# Test specifico
pytest tests/test_analyzer.py -v

# Test con output dettagliato
pytest -v --tb=short
```

### Build Bundle (Eseguibile Standalone)

```bash
# Build completo con PyInstaller
python build.py

# Output in: dist/CDJ-Check.app (macOS) o dist/CDJ-Check.exe (Windows)
```

---

## 5. 🧠 Principi Specifici del Progetto

### 1. FFmpeg come motore audio

**Python è solo l'orchestratore.** Tutto il processing audio (analisi, conversione, resampling) deve essere delegato a FFmpeg via subprocess. Python non processa mai il flusso audio raw.

```python
# ✅ CORRETTO - FFmpeg fa tutto il lavoro
cmd = [
    "ffmpeg", "-y", "-i", str(input_path),
    "-ar", "48000", "-sample_fmt", "s24",
    "-acodec", "pcm_s24le",
    str(output_path)
]
subprocess.run(cmd, ...)

# ❌ SBAGLIATO - Non usare librerie Python per processing audio
import soundfile  # NO - troppo lento, non usare
```

### 2. Performance critiche

| Metrica | Target | Come raggiungerla |
|---------|--------|-------------------|
| Analisi singolo file | < 200 ms | ffprobe subprocess, parsing JSON |
| RAM idle | < 50 MB | No cache file in memoria, streaming |
| Conversione | < 1.5x durata | FFmpeg diretto, no processing Python |
| GUI responsive | 60 FPS | Thread separati per analysis/conversion |

### 3. Gestione file e path

- Usa sempre `pathlib.Path` per manipolazione path
- Crea directory output con `path.mkdir(parents=True, exist_ok=True)`
- Verifica spazio disponibile prima della conversione batch
- Gestisci nomi file duplicati con suffisso numerico

### 4. UX della GUI

- **Dark mode default** - coerente con software DJ (Rekordbox, Traktor)
- **No popup modali** - avvisi inline nella lista file
- **Feedback immediato** - highlight drop zone, progress bar, indicatori colorati
- **Drag-and-drop** come input primario, file picker come fallback

### 5. Compatibilità CDJ-2000 Nexus

**Formati supportati nativamente:**
| Formato | Sample Rate | Bit Depth |
|---------|-------------|-----------|
| MP3 | 44.1 kHz | — |
| AAC (M4A) | 44.1 / 48 kHz | — |
| WAV | 44.1 / 48 kHz | 16 / 24-bit |
| AIFF | 44.1 / 48 kHz | 16 / 24-bit |

**ATTENZIONE:** CDJ-2000 Nexus (1ª gen) **NON supporta FLAC**. Solo NXS2 e CDJ-3000 supportano FLAC.

---

## 6. 🐙 Git — Versionamento

### Branching Strategy

```
main (produzione, sempre deployabile)
 └── feature/nome-feature    ← sviluppo nuova feature
 └── fix/nome-bug            ← bugfix
 └── chore/nome-task         ← refactor, config, docs
```

### Commit Messages (Conventional Commits)

```
<type>(<scope>): <descrizione breve>

Tipi:
  feat     → nuova funzionalità
  fix      → bugfix
  docs     → documentazione
  style    → formattazione (no logic change)
  refactor → refactoring senza cambi funzionali
  test     → aggiunta o modifica test
  chore    → config, dipendenze, build

Scope comuni per CDJ-Check:
  gui      → interfaccia utente
  analyzer → analisi audio
  converter → conversione ffmpeg
  compat   → motore compatibilità
```

Esempi:
```
feat(gui): add drag-and-drop support for folders
fix(analyzer): handle corrupted FLAC files gracefully
docs(readme): update FFmpeg installation instructions
chore(deps): update customtkinter to 5.2.2
```

---

## 7. 🚀 Release e Distribuzione

### Versionamento

Segui [Semantic Versioning](https://semver.org/):
- `MAJOR` — cambiamenti breaking (nuovo formato supportato, breaking CLI)
- `MINOR` — nuove feature backward compatible (nuovi profili CDJ)
- `PATCH` — bugfix

### Checklist Pre-Release

- [ ] Tutti i test passano (`pytest`)
- [ ] Linting pulito (`ruff check src/`)
- [ ] Test manuale GUI su tutte e 3 le piattaforme
- [ ] Test conversione tutti i formati supportati
- [ ] Versione aggiornata in `pyproject.toml`
- [ ] Changelog aggiornato
- [ ] Build bundle funzionante (`python build.py`)

### Piattaforme Target

| Piattaforma | Min Version | Note |
|-------------|-------------|------|
| macOS | 12+ (Monterey) | Bundle .app firmato (se possibile) |
| Windows | 10+ | .exe standalone |
| Linux | Ubuntu 20.04+ | AppImage o tarball |

---

## 8. 🧪 Testing Guidelines

### Tipologie di Test

1. **Unit tests** — Test isolati per `analyzer`, `compatibility`, `converter`
2. **Integration tests** — Test flusso completo analisi → conversione
3. **GUI tests** — Test manuali per UX (no automatizzati per GUI Tkinter)

### Fixture Consigliate

```python
# tests/conftest.py
import pytest
from pathlib import Path

@pytest.fixture
def sample_audio_dir() -> Path:
    """Directory con file audio di test."""
    return Path(__file__).parent / "fixtures" / "audio"

@pytest.fixture
def mock_cdj_profile():
    """Profilo CDJ-2000 Nexus per test."""
    from cdj_check.config import CDJProfile
    return CDJProfile.nxs1()
```

### Mocking FFmpeg

```python
# Per test veloci, mocka subprocess.run
from unittest.mock import patch, MagicMock

def test_analyze_file_mocked():
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = '{"format": {"bit_rate": "320000"}}'
    
    with patch('subprocess.run', return_value=mock_result):
        result = analyze_file("test.mp3")
        assert result.bitrate == 320000
```

---

## 9. 📋 Checklist per Task

### Nuova Feature
- [ ] Ho letto il PRD (`CDJ-Check_PRD.md`)
- [ ] Ho identificato il modulo/i da modificare
- [ ] Ho scritto i test prima/durante lo sviluppo
- [ ] Ho gestito gli edge case (file corrotti, mancanza FFmpeg, etc.)
- [ ] Ho testato manualmente la GUI (se applicabile)
- [ ] Ho verificato `ruff check` e `ruff format`
- [ ] Ho aggiornato il README se necessario

### Bug Fix
- [ ] Ho creato un test che riproduce il bug
- [ ] Ho verificato che il fix risolve il problema
- [ ] Ho verificato che il fix non introduce regressioni
- [ ] Ho aggiunto un commento che spiega il fix se non ovvio

### Refactoring
- [ ] Tutti i test esistenti passano
- [ ] Non ho cambiato il comportamento esterno
- [ ] Ho migliorato leggibilità/mantenibilità
- [ ] Ho verificato performance non degrado

---

## 10. 🔧 Troubleshooting Comune

### Problema: FFmpeg non trovato
```
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```
**Soluzione:** Installa FFmpeg e assicurati sia nel PATH.

### Problema: GUI non si avvia su macOS
```
_tkinter.TclError: can't find package Tk
```
**Soluzione:** Installa Tkinter: `brew install python-tk@3.11`

### Problema: Drag-and-drop non funziona
**Soluzione:** Verifica `tkinterdnd2` installato e import corretto:
```python
from tkinterdnd2 import TkinterDnD, DND_FILES
```

### Problema: Build PyInstaller fallisce
**Soluzione:** 
1. Pulisci cache: `rm -rf build/ dist/`
2. Verifica spec file: `CDJ-Check.spec`
3. Riprova: `python build.py`

---

## 11. 📚 Risorse Utili

- **PRD:** `CDJ-Check_PRD.md` — Requisiti prodotto
- **README:** `README.md` — Documentazione utente
- **FFmpeg docs:** https://ffmpeg.org/documentation.html
- **CustomTkinter:** https://github.com/TomSchimansky/CustomTkinter
- **CDJ-2000 Nexus specs:** Pioneer DJ manual ufficiale

---

> **Ultimo aggiornamento:** Febbraio 2026
> **Progetto:** CDJ-Check v0.1.0
> **Maintainer:** CDJ-Check Team
