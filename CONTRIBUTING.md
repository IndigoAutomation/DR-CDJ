# 🤝 Guida per i Contributor

Grazie per il tuo interesse nel contribuire a CDJ-Check! Questo documento ti guiderà attraverso il processo di contribuzione.

---

## 📋 Indice

- [Codice di Condotta](#codice-di-condotta)
- [Come posso contribuire?](#come-posso-contribuire)
- [Setup Ambiente di Sviluppo](#setup-ambiente-di-sviluppo)
- [Workflow di Sviluppo](#workflow-di-sviluppo)
- [Linee Guida per il Codice](#linee-guida-per-il-codice)
- [Commit Messages](#commit-messages)
- [Testing](#testing)
- [Domande?](#domande)

---

## 📜 Codice di Condotta

Questo progetto aderisce al [Codice di Condotta](CODE_OF_CONDUCT.md). Partecipando, ti impegni a mantenere un ambiente collaborativo e rispettoso.

---

## 💡 Come posso contribuire?

### Segnalare Bug

Prima di segnalare un bug:
1. 🔍 Cerca nelle [issues esistenti](https://github.com/filippoitaliano/cdj-check/issues) per evitare duplicati
2. 📝 Raccogli informazioni: versione Python, sistema operativo, log di errore
3. 🎯 Crea una issue usando il template "Bug Report"

### Suggerire Feature

Hai un'idea per migliorare CDJ-Check?
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
- FFmpeg 6.x installato e nel PATH
- Git

### Installazione

```bash
# 1. Clona il tuo fork
git clone https://github.com/YOUR_USERNAME/cdj-check.git
cd cdj-check

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
```

---

## 🔄 Workflow di Sviluppo

### Branching Strategy

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
   ruff check src/
   ruff format src/
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

**✅ Corretto — Named exports:**
```python
class AudioAnalyzer:
    pass

def analyze_file(path: Path) -> AudioMetadata:
    pass
```

**✅ Corretto — Gestione errori specifica:**
```python
try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
except subprocess.TimeoutExpired:
    raise AnalysisError(f"Timeout analizzando {path}")
except FileNotFoundError:
    raise AnalysisError("FFmpeg non trovato")
```

### Moduli Core

| Modulo | Responsabilità |
|--------|----------------|
| `analyzer.py` | Solo analisi metadati via ffprobe |
| `compatibility.py` | Solo logica regole compatibilità |
| `converter.py` | Solo orchestrazione FFmpeg |
| `gui.py` | Solo interfaccia utente |

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

### Scope

- `gui` — Interfaccia utente
- `analyzer` — Analisi audio
- `converter` — Conversione FFmpeg
- `compat` — Motore compatibilità
- `config` — Configurazioni
- `docs` — Documentazione

### Esempi

```bash
feat(gui): add drag-and-drop support for folders
fix(analyzer): handle corrupted FLAC files gracefully
docs(readme): update FFmpeg installation instructions
chore(deps): update customtkinter to 5.2.2
refactor(converter): extract ffmpeg command builder
```

---

## 🧪 Testing

### Scrittura Test

```python
# tests/test_analyzer.py
import pytest
from pathlib import Path
from cdj_check.analyzer import analyze_file

def test_analyze_mp3_valid(sample_audio_dir: Path):
    """Test analisi file MP3 valido."""
    result = analyze_file(sample_audio_dir / "test.mp3")
    assert result.codec == "mp3"
    assert result.sample_rate == 44100
```

### Coverage

Manteniamo coverage > 80%:

```bash
pytest --cov=cdj_check --cov-report=html
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

## 📚 Risorse

- [AGENTS.md](AGENTS.md) — Informazioni per AI agents
- [CDJ-Check_PRD.md](CDJ-Check_PRD.md) — Product Requirements Document
- [Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## ❓ Domande?

- 💬 [Discussions](https://github.com/filippoitaliano/cdj-check/discussions) — Per domande generali
- 🐛 [Issues](https://github.com/filippoitaliano/cdj-check/issues) — Per bug e feature request
- 📧 Email: demos.indigo@gmail.com

---

**Grazie per contribuire a CDJ-Check! 🎵**
