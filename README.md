# 🎵 Dr. CDJ

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)]()

**Dr. CDJ - Audio Compatibility Checker & Converter per Pioneer CDJ**

Verifica istantaneamente se i tuoi file audio sono compatibili con i Pioneer CDJ (2000 Nexus, NXS2, 3000, XDJ) e convertili automaticamente nel formato di massima qualità supportato.
---

## ✨ Caratteristiche

- 🎯 **Supporto Multi-Player**: CDJ-2000 Nexus, CDJ-2000 NXS2, CDJ-3000, XDJ-1000MK2, XDJ-700
- 🎨 **Interfaccia Moderna**: Dark mode con design professionale
- 📁 **Drag & Drop**: Trascina file o cartelle
- ⚙️ **Conversione Personalizzata**: Formato, sample rate e bit depth configurabili
- 🚀 **Massima Qualità**: Impostazioni automatiche per il player target
- 📊 **Analisi Istantanea**: Verifica compatibilità in millisecondi

---

## 🚀 Installazione Rapida

### Metodo 1: Script Automatico (Consigliato)

```bash
git clone https://github.com/IndigoAutomation/DR-CDJ.git
cd DR-CDJ
python3 install.py
```

### Metodo 2: Manuale

**Requisiti:**
- Python 3.11+
- FFmpeg 6.x+

```bash
# 1. Clona il repository
git clone https://github.com/IndigoAutomation/DR-CDJ.git
cd dr-cdj

# 2. Installa dipendenze
pip install -r requirements.txt

# 3. Installa Dr. CDJ
pip install -e .

# 4. Avvia
dr-cdj
```

### Metodo 3: App Bundle (macOS)

Scarica l'ultima release:
```bash
curl -L -o Dr-CDJ.dmg https://github.com/IndigoAutomation/DR-CDJ/releases/latest/download/Dr-CDJ-1.0.1-macOS.dmg
```

---

## 🎮 Utilizzo

### GUI (Interfaccia Grafica)

```bash
dr-cdj
# oppure
python3 -m dr_cdj.gui
```

1. Seleziona il tuo **Player Target** (CDJ-2000 Nexus, CDJ-3000, etc.)
2. Trascina i file audio nella drop zone
3. Verifica la compatibilità
4. Clicca **Converti** per i file non compatibili

### CLI (Linea di Comando)

```bash
# Verifica singolo file
dr-cdj check track.flac

# Verifica cartella
dr-cdj check /path/to/music/

# Converti file
dr-cdj convert track.flac --output ./converted/

# Output JSON
dr-cdj check track.flac --json
```

---

## 📋 Formati Supportati

### Input
| Formato | Stato |
|---------|-------|
| MP3 | ✅ Nativo |
| AAC/M4A | ✅ Nativo |
| WAV | ✅ Nativo |
| AIFF | ✅ Nativo |
| FLAC | ⚠️ Convertibile |
| OGG | ⚠️ Convertibile |
| OPUS | ⚠️ Convertibile |
| WMA | ⚠️ Convertibile |

### Output Conversione
| Formato | Qualità Max |
|---------|-------------|
| WAV | 24-bit / 96 kHz |
| AIFF | 24-bit / 96 kHz |

---

## 🏗️ Architettura

```
dr_cdj/
├── analyzer.py        # Analisi audio con ffprobe
├── compatibility.py   # Motore compatibilità multi-profilo
├── converter.py       # Conversione con ffmpeg
├── gui.py             # Interfaccia CustomTkinter
├── config.py          # Profili CDJ e costanti
└── main.py            # Entry point
```

---

## 🤝 Contribuire

Contributi benvenuti! Leggi [CONTRIBUTING.md](CONTRIBUTING.md) per iniziare.

### Sviluppo Locale

```bash
# Setup ambiente
git clone https://github.com/IndigoAutomation/DR-CDJ.git
cd dr-cdj
pip install -e ".[dev]"

# Esegui test
pytest

# Linting
ruff check src/
ruff format src/

# Build app
python3 build.py
```

---

## 📦 Release

| Versione | Download | Stato |
|----------|----------|-------|
| Latest | [Dr-CDJ.dmg](https://github.com/IndigoAutomation/DR-CDJ/releases/latest) | ✅ Stabile |
| macOS | `Dr-CDJ.dmg` | ✅ Supportato |
| Windows | `Dr-CDJ.exe` | 🚧 In sviluppo |
| Linux | `dr-cdj` | 🚧 In sviluppo |

---

## 📄 Licenza

MIT License - vedi [LICENSE](LICENSE)

---

## 🙏 Credits

Creato per DJ che usano Pioneer CDJ in club e festival.

> ⚠️ **Disclaimer**: Pioneer e CDJ sono marchi registrati di Pioneer Corporation. Questo tool non è affiliato con Pioneer.

---

<div align="center">

**[⬇️ Scarica Ora](https://github.com/tuousername/dr-cdj/releases)** • 
**[📖 Documentazione](docs/)** • 
**[🐛 Segnala Bug](../../issues)**

</div>
