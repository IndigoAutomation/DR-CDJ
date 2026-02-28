<div align="center">

<img src="https://raw.githubusercontent.com/filippoitaliano/cdj-check/main/docs/assets/logo.png" alt="CDJ-Check Logo" width="120">

# 🎵 CDJ-Check

**The Ultimate Audio Toolkit for Professional DJs & Producers**

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-purple.svg?style=for-the-badge)]()
[![Version](https://img.shields.io/badge/version-0.1.0-orange.svg?style=for-the-badge)]()
[![CI](https://img.shields.io/github/actions/workflow/status/filippoitaliano/cdj-check/ci.yml?label=CI&style=for-the-badge&logo=github)](https://github.com/filippoitaliano/cdj-check/actions)

<p align="center">
  <b>Stop worrying about compatibility issues. Focus on your mix.</b>
</p>

[📥 Download](#-download) • [🚀 Quick Start](#-quick-start) • [📖 Docs](#-documentation) • [🤝 Contribute](#-contribute)

</div>

---

## 🎯 Why CDJ-Check?

As a DJ or producer, you know the nightmare: **you show up at the club, plug in your USB, and the CDJ doesn't read your files.** 😱

CDJ-Check eliminates this stress by **automatically verifying and converting your audio files** to ensure perfect compatibility with Pioneer CDJ-2000 Nexus and other professional DJ equipment.

### Real Problems, Solved

| Problem | Solution |
|---------|----------|
| ❌ "Unsupported Format" errors mid-set | ✅ Pre-flight compatibility check |
| ❌ FLAC files rejected by CDJ-2000 Nexus | ✅ Auto-convert to WAV preserving quality |
| ❌ High-res files (96kHz+) not playing | ✅ Smart resampling to 48kHz |
| ❌ Manual batch conversion nightmares | ✅ Drag, drop, done |
| ❌ Corrupted files crashing decks | ✅ Pre-set integrity verification |

---

## ✨ Features

### 🎛️ For DJs
- **Instant Compatibility Check** — Drag & drop your entire library
- **Smart Conversion** — FLAC → WAV (lossless), resampling, format fixes
- **Batch Processing** — Prepare 100+ tracks in minutes
- **Visual Status** — Color-coded results: ✅ Ready | ⚠️ Convert | ❌ Error

### 🎚️ For Producers
- **Quality Preservation** — 24-bit/48kHz maximum quality output
- **Metadata Integrity** — Tags preserved during conversion
- **Live Performance Ready** — Ensure your tracks work on club systems

### 🖥️ Technical Excellence
- **Dark Mode UI** — Easy on the eyes during late-night prep sessions
- **Cross-Platform** — Windows, macOS, Linux
- **FFmpeg Powered** — Industry-standard audio engine
- **Zero Bloat** — Lightweight, fast, no unnecessary dependencies

---

## 📸 Screenshots

<div align="center">

| <img src="docs/assets/screenshot-main.png" width="300"><br>*Main Interface* | <img src="docs/assets/screenshot-analysis.png" width="300"><br>*Batch Analysis* | <img src="docs/assets/screenshot-conversion.png" width="300"><br>*Smart Conversion* |
|:---:|:---:|:---:|

</div>

---

## 📥 Download

### 🚀 Standalone Executables (Recommended)

| Platform | Download | Size |
|:---:|:---:|:---:|
| 🪟 **Windows** | [CDJ-Check-Windows.exe](https://github.com/filippoitaliano/cdj-check/releases/latest) | ~25 MB |
| 🍎 **macOS** | [CDJ-Check-macOS.dmg](https://github.com/filippoitaliano/cdj-check/releases/latest) | ~30 MB |
| 🐧 **Linux** | [CDJ-Check-Linux](https://github.com/filippoitaliano/cdj-check/releases/latest) | ~28 MB |

> 💡 **Tip:** The standalone versions include FFmpeg — no additional installation needed!

### 🐍 Install from Source

```bash
# Clone the repository
git clone https://github.com/filippoitaliano/cdj-check.git
cd cdj-check

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows

# Install
pip install -e ".[dev]"

# Verify FFmpeg is installed
ffmpeg -version
```

---

## 🚀 Quick Start

### GUI Mode (Recommended for DJs)

```bash
cdj-check
# or
cdj-check --gui
```

1. **Drag** your music folder or files into the drop zone
2. **Review** the compatibility status of each track
3. **Click** "Convert Non-Compatible" 
4. **Copy** the converted files to your USB — ready for the club! 🎉

### CLI Mode (For power users & automation)

```bash
# Check single track
cdj-check check mytrack.flac

# Check entire library
cdj-check check ~/Music/

# Check with JSON output (for scripting)
cdj-check check ~/Music/ --json

# Convert incompatible files
cdj-check convert ~/Music/ --output ~/CDJ_Ready/

# Parallel conversion (faster)
cdj-check convert ~/Music/ --workers 4
```

---

## 🎛️ CDJ Compatibility Guide

### Pioneer CDJ-2000 Nexus (1st Gen)

| Format | Native Support | With CDJ-Check |
|--------|----------------|----------------|
| **MP3** | ✅ 32-320 kbps | ✅ Ready to play |
| **AAC (M4A)** | ✅ 44.1/48 kHz | ✅ Ready to play |
| **WAV** | ✅ 16/24-bit, 44.1/48 kHz | ✅ Ready to play |
| **AIFF** | ✅ 16/24-bit, 44.1/48 kHz | ✅ Ready to play |
| **FLAC** | ❌ Not supported | ✅ Auto-convert to WAV |
| **ALAC** | ❌ Not supported | ✅ Auto-convert to WAV |
| **High-Res WAV** | ⚠️ 96/192 kHz not supported | ✅ Resample to 48 kHz |
| **OGG/OPUS** | ❌ Not supported | ✅ Convert to WAV |

> ⚠️ **Important:** The original CDJ-2000 Nexus does **NOT** support FLAC. This support was added in the NXS2. CDJ-Check automatically converts FLAC to WAV with zero quality loss.

---

## 🏗️ Architecture

```
cdj_check/
├── 🎵 analyzer.py        # Fast audio analysis via ffprobe
├── 🔍 compatibility.py   # CDJ compatibility rules engine
├── 🔄 converter.py       # FFmpeg orchestration & batch processing
├── 🖼️ gui.py            # Modern dark-mode interface (CustomTkinter)
├── ⚙️ config.py         # Profiles & constants
├── 🛠️ utils.py          # Helper utilities
└── 🚀 main.py           # CLI/GUI entry point
```

### Built With

| Component | Technology | Purpose |
|-----------|------------|---------|
| Runtime | Python 3.11+ | Fast, modern Python |
| GUI Framework | CustomTkinter 5.2+ | Native-looking dark UI |
| Audio Engine | FFmpeg 6.x | Industry-standard processing |
| Drag & Drop | tkinterdnd2 | Native file dropping |
| Testing | pytest 7.0+ | Comprehensive test coverage |
| Linting | Ruff | Fast, modern Python linting |
| Bundling | PyInstaller | Standalone executables |

---

## 📖 Documentation

| Guide | Description |
|-------|-------------|
| [📘 User Guide](docs/USER_GUIDE.md) | Complete tutorial for DJs and producers |
| [🔧 Developer Guide](docs/DEVELOPER_GUIDE.md) | Setup for contributors |
| [⚡ Performance](docs/PERFORMANCE.md) | Benchmarks & optimizations |
| [🐛 Troubleshooting](docs/TROUBLESHOOTING.md) | Common issues & solutions |
| [📋 Changelog](CHANGELOG.md) | Version history |

---

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage report
pytest --cov=cdj_check --cov-report=html

# Test specific module
pytest tests/test_analyzer.py -v

# Linting
ruff check src/
ruff format src/
```

---

## 🤝 Contribute

We welcome contributions from the DJ and developer community!

### How to Contribute

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🔁 Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Roadmap

- [ ] CDJ-2000 NXS2 support (adds native FLAC)
- [ ] CDJ-3000 support
- [ ] Rekordbox XML integration
- [ ] LUFS loudness analysis
- [ ] Clipping detection
- [ ] Watch folder (auto-convert on file add)
- [ ] Cloud sync for profiles

---

## 📊 Performance Benchmarks

| Operation | Target | Tested On |
|-----------|--------|-----------|
| Single file analysis | < 200ms | MacBook Pro M1 |
| WAV 24-bit conversion | < 1.5x duration | SSD NVMe |
| Batch 50 files | < 30s | Ryzen 7 5800X |
| Idle RAM usage | < 50 MB | — |

---

## 💬 Community

- 💡 [Discussions](https://github.com/filippoitaliano/cdj-check/discussions) — Ask questions, share tips
- 🐛 [Issues](https://github.com/filippoitaliano/cdj-check/issues) — Report bugs, request features
- 📧 Email: demos.indigo@gmail.com

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Credits

Made with ❤️ by and for DJs, producers, and audio professionals.

**Maintainer:**
- [@filippoitaliano](https://github.com/filippoitaliano) — Creator & maintainer

**Special Thanks:**
- The FFmpeg team for the incredible audio toolkit
- The CustomTkinter community for the modern UI framework
- All contributors and beta testers

---

<div align="center">

⚠️ **Disclaimer:** Pioneer, CDJ, CDJ-2000, Nexus, NXS2, and CDJ-3000 are trademarks of Pioneer Corporation. This tool is not affiliated with, associated with, authorized by, or officially connected to Pioneer Corporation.

**[⬆ Back to Top](#-cdj-check)**

</div>
