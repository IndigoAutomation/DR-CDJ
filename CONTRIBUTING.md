# 🤝 Guida per i Contributor

Grazie per il tuo interesse nel contribuire a **Dr. CDJ**! Questo documento ti guiderà attraverso il processo di contribuzione.

---

## 📋 Indice

- [Codice di Condotta](#codice-di-condotta)
- [Come posso contribuire?](#come-posso-contribuire)
- [Setup Ambiente di Sviluppo](#setup-ambiente-di-sviluppo)
- [Workflow di Sviluppo](#workflow-di-sviluppo)
- [Linee Guida per il Codice](#linee-guida-per-il-codice)
- [Commit Messages](#commit-messages)
- [Testing](#testing)
- [Pull Request](#pull-request)
- [Release Process](#release-process)
- [Domande?](#domande)

---

## 📜 Codice di Condotta

Questo progetto aderisce al [Codice di Condotta](CODE_OF_CONDUCT.md). Partecipando, ti impegni a mantenere un ambiente collaborativo e rispettoso.

---

## 💡 Come posso contribuire?

### Segnalare Bug

Prima di segnalare un bug:
1. 🔍 Cerca nelle [issues esistenti](https://github.com/IndigoAutomation/DR-CDJ/issues) per evitare duplicati
2. 📝 Raccogli informazioni: versione di Dr. CDJ, sistema operativo, log di errore
3. 🎯 Crea una issue usando il template "Bug Report"

**Informazioni utili da includere:**
- Versione di Dr. CDJ (vedi menu About)
- Versione di macOS/Windows/Linux
- Versione di FFmpeg (se installata manualmente)
- Tipo di file audio che causa il problema
- Messaggio di errore completo

### Suggerire Feature

Hai un'idea per migliorare Dr. CDJ?
1. 💭 Descrivi chiaramente la feature e il problema che risolve
2. 🎯 Spiega perché sarebbe utile per i DJ/producer
3. 📝 Apri una issue usando il template "Feature Request"

### Contribuire al Codice

1. 🍴 Forka la repository
2. 🌿 Crea un branch per la tua feature (`git checkout -b feature/nome-feature`)
3. 💾 Scrivi codice di qualità con test
4. 📤 Pusha e apri una Pull Request

---

## 🔧 Setup Ambiente di Sviluppo

### Prerequisiti

- Python 3.11+
- FFmpeg 6.x+ installato e nel PATH
- Git
- (macOS) Xcode Command Line Tools per il build

### Installazione

```bash
# 1. Clona il tuo fork
git clone https://github.com/YOUR_USERNAME/DR-CDJ.git
cd DR-CDJ

# 2. Crea virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# oppure .venv\Scripts\activate  # Windows

# 3. Installa in modalità sviluppo
pip install -e ".[dev]"

# 4. Verifica installazione
pytest --version
ruff --version
ffmpeg -version

# 5. Esegui test
pytest

# 6. Avvia l'applicazione
python -m dr_cdj.main
```

### Struttura del Progetto

```
DR-CDJ/
├── src/dr_cdj/          # Codice sorgente
│   ├── main.py          # Entry point
│   ├── config.py        # Configurazioni CDJ
│   ├── analyzer.py      # Analisi audio
│   ├── compatibility.py # Logica compatibilità
│   ├── converter.py     # Conversione FFmpeg
│   ├── gui.py           # Interfaccia utente
│   └── splash.py        # Splash screen
├── tests/               # Test suite
├── scripts/             # Script di utilità
├── hooks/               # PyInstaller hooks
├── docs/                # Documentazione
└── assets/              # Risorse (icone, logo)
```

---

## 🔄 Workflow di Sviluppo

### Branching Strategy

Usiamo il modello **GitHub Flow**:

```
main                    ← produzione, sempre stabile
├── feature/gui-dark    ← nuove feature
├── fix/ffmpeg-timeout  ← bugfix
├── docs/readme-update  ← documentazione
└── chore/deps-update   ← manutenzione
```

### Processo

1. **Crea un branch dal main aggiornato**
   ```bash
   git checkout main
   git pull upstream main
   git checkout -b feature/mia-feature
   ```

2. **Sviluppa con test**
   - Scrivi/modifica il codice
   - Aggiungi/aggiorna i test
   - Verifica che tutti i test passino

3. **Linting e formattazione**
   ```bash
   # Controllo linting
   ruff check src/
   
   # Formattazione automatica
   ruff format src/
   
   # Verifica tipi (opzionale, se installato mypy)
   mypy src/
   ```

4. **Committa con conventional commits**
   ```bash
   git add .
   git commit -m "feat(gui): add dark mode toggle"
   ```

5. **Push e Pull Request**
   ```bash
   git push origin feature/mia-feature
   ```
   Poi apri una PR su GitHub.

---

## 📝 Linee Guida per il Codice

### Stile Python

- **Line length:** 100 caratteri
- **Formatter:** Ruff
- **Type hints:** Obbligatori per funzioni pubbliche
- **Docstring:** Google style convention

### Pattern di Codice

**✅ Corretto — Usa pathlib:**
```python
from pathlib import Path
output_path = Path(input_path).parent / "CDJ_Ready" / f"{stem}.wav"
```

**❌ Sbagliato — No os.path:**
```python
import os
output_path = os.path.join(os.path.dirname(input_path), "CDJ_Ready", filename)
```

**✅ Corretto — Gestione errori specifica:**
```python
from dr_cdj.exceptions import AnalysisError

try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
except subprocess.TimeoutExpired:
    raise AnalysisError(f"Timeout analizzando {path}")
except FileNotFoundError:
    raise AnalysisError("FFmpeg non trovato")
```

**✅ Corretto — Type hints:**
```python
from pathlib import Path
from typing import Optional

def analyze_file(path: Path, timeout: Optional[int] = 30) -> AudioMetadata:
    """Analizza un file audio e restituisce i metadati.
    
    Args:
        path: Percorso del file audio
        timeout: Timeout in secondi (default: 30)
        
    Returns:
        AudioMetadata con i metadati del file
        
    Raises:
        AnalysisError: Se l'analisi fallisce
    """
    ...
```

### Moduli Core

| Modulo | Responsabilità |
|--------|----------------|
| `analyzer.py` | Solo analisi metadati via ffprobe |
| `compatibility.py` | Solo logica regole compatibilità |
| `converter.py` | Solo orchestrazione FFmpeg |
| `gui.py` | Solo interfaccia utente |
| `config.py` | Solo configurazioni e profili CDJ |

---

## 💬 Commit Messages

Usiamo [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <descrizione breve>

<body opzionale>

<footer opzionale>
```

### Tipi

| Tipo | Descrizione |
|------|-------------|
| `feat` | Nuova funzionalità |
| `fix` | Bugfix |
| `docs` | Documentazione |
| `style` | Formattazione (no logic change) |
| `refactor` | Refactoring |
| `test` | Test |
| `chore` | Config, dipendenze, build |
| `perf` | Miglioramento performance |
| `ci` | Continuous Integration |

### Scope

- `gui` — Interfaccia utente
- `analyzer` — Analisi audio
- `converter` — Conversione FFmpeg
- `compat` — Motore compatibilità
- `config` — Configurazioni
- `docs` — Documentazione
- `build` — Build system
- `deps` — Dipendenze

### Esempi

```bash
feat(gui): add drag-and-drop support for folders
fix(analyzer): handle corrupted FLAC files gracefully
docs(readme): update FFmpeg installation instructions
chore(deps): update customtkinter to 5.2.2
refactor(converter): extract ffmpeg command builder
perf(analyzer): cache ffprobe results for duplicate files
test(converter): add tests for WMA conversion
```

---

## 🧪 Testing

### Scrittura Test

```python
# tests/test_analyzer.py
import pytest
from pathlib import Path
from dr_cdj.analyzer import analyze_file

def test_analyze_mp3_valid(sample_audio_dir: Path):
    """Test analisi file MP3 valido."""
    result = analyze_file(sample_audio_dir / "test.mp3")
    assert result.codec == "mp3"
    assert result.sample_rate == 44100

def test_analyze_file_not_found():
    """Test gestione file inesistente."""
    with pytest.raises(AnalysisError):
        analyze_file(Path("/nonexistent/file.mp3"))
```

### Coverage

Manteniamo coverage > 80%:

```bash
# Coverage report in console
pytest --cov=dr_cdj --cov-report=term

# Coverage report HTML
pytest --cov=dr_cdj --cov-report=html
open htmlcov/index.html  # macOS
```

### Mocking FFmpeg

Per test veloci, mocka subprocess:

```python
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

## 🔍 Pull Request

### Requisiti PR

- [ ] Descrizione chiara delle modifiche
- [ ] Riferimento alle issue collegate (es. "Fixes #123")
- [ ] Test aggiunti/aggiornati
- [ ] Tutti i test passano (`pytest`)
- [ ] Linting passa (`ruff check src/`)
- [ ] Documentazione aggiornata (se necessario)
- [ ] CHANGELOG.md aggiornato (se necessario)

### Processo di Review

1. Tutte le PR richiedono almeno 1 review
2. I check CI devono passare
3. Risolvi i commenti dei reviewer
4. Il maintainer farà il merge una volta approvata

---

## 📦 Release Process

### Versioning

Seguiamo [Semantic Versioning](https://semver.org/):
- **MAJOR** — Cambiamenti breaking
- **MINOR** — Nuove feature (retrocompatibili)
- **PATCH** — Bugfix

### Preparare una Release

1. Aggiorna la versione in `pyproject.toml`
2. Aggiorna `CHANGELOG.md` con la nuova versione
3. Crea un commit: `chore(release): bump version to X.Y.Z`
4. Crea un tag Git: `git tag vX.Y.Z`
5. Pusha: `git push origin main --tags`
6. Crea una release su GitHub con le note di rilascio

### Build macOS App

```bash
# 1. Download FFmpeg embedded
python scripts/download-ffmpeg.py

# 2. Build con PyInstaller
python build.py

# 3. Crea DMG
bash create-dmg.sh
```

---

## 🛡️ Segnalazione Problemi di Sicurezza

Se scopri una vulnerabilità di sicurezza:

1. **NON** aprire una issue pubblica
2. Invia una email a: demos.indigo@gmail.com
3. Descrivi il problema con dettagli sufficienti per riprodurlo
4. Aspetta una risposta prima di divulgare pubblicamente

---

## 📚 Risorse

- [CLAUDE.md](CLAUDE.md) — Informazioni per AI agents
- [README.md](README.md) — Documentazione utente
- [Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)

---

## ❓ Domande?

- 💬 [Discussions](https://github.com/IndigoAutomation/DR-CDJ/discussions) — Per domande generali
- 🐛 [Issues](https://github.com/IndigoAutomation/DR-CDJ/issues) — Per bug e feature request
- 📧 Email: demos.indigo@gmail.com

---

**Grazie per contribuire a Dr. CDJ! 🎵**
