# Dr. CDJ - User Manual

**Audio Compatibility Checker & Converter for Pioneer CDJ Players**

---

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Using the App](#using-the-app)
5. [Supported Formats](#supported-formats)
6. [CDJ Compatibility](#cdj-compatibility)
7. [Command Line Interface (CLI)](#command-line-interface-cli)
8. [Troubleshooting](#troubleshooting)
9. [FAQ](#faq)

---

## Introduction

Dr. CDJ is a macOS application that helps DJs and producers ensure their audio files are compatible with Pioneer CDJ players. It analyzes your audio files and automatically converts incompatible formats to ensure they'll play correctly on your target CDJ model.

### Key Features

- **Drag & Drop Interface**: Simply drop files or folders to analyze
- **Multi-Player Support**: Works with CDJ-2000, CDJ-3000, XDJ series, and more
- **Batch Processing**: Convert hundreds of files at once
- **Smart Conversion**: Automatically picks the best format for your player
- **Studio Quality**: Maintains up to 24-bit / 96kHz quality

---

## Installation

### Requirements

- **macOS**: Version 12 (Monterey) or later
- **Architecture**: Intel or Apple Silicon (M1/M2/M3)
- **Storage**: ~200 MB free space
- **Internet**: Required for first launch (FFmpeg download)

### Installation Steps

1. **Download** the latest version from:
   https://indigoautomation.github.io/DR-CDJ/

2. **Open** the DMG file:
   ```
   Dr-CDJ-1.0.1-macOS.dmg
   ```

3. **Drag** Dr. CDJ to your Applications folder

4. **Launch** the app from Applications

5. **First Launch**: The app will download FFmpeg automatically (one-time, ~30 MB)

> **Note**: If you see a security warning, go to System Settings > Privacy & Security and click "Open Anyway"

---

## Quick Start

### Basic Workflow

1. **Select your CDJ model** from the dropdown (top-right)
2. **Drag and drop** audio files or folders into the drop zone
3. **Review** the analysis results:
   - ✅ Green: File is compatible
   - ⚠️ Yellow: File needs conversion
   - ❌ Red: File cannot be converted
4. **Click "Convert"** to convert incompatible files
5. **Find** converted files in the `CDJ_Ready/` folder next to your originals

---

## Using the App

### Main Interface

```
┌─────────────────────────────────────────────┐
│  Dr. CDJ                    [CDJ-3000 ▼]   │  ← Player selector
├─────────────────────────────────────────────┤
│                                             │
│           [  DROP FILES HERE  ]             │  ← Drop zone
│                                             │
├─────────────────────────────────────────────┤
│  File Analysis                              │
│  ┌─────────────────────────────────────┐   │
│  │ ✅ Track_01.wav    Compatible      │   │
│  │ ⚠️ Track_02.flac   Needs conversion│   │
│  │ ✅ Track_03.mp3    Compatible      │   │
│  └─────────────────────────────────────┘   │
├─────────────────────────────────────────────┤
│  [     Convert Selected Files     ]        │  ← Convert button
└─────────────────────────────────────────────┘
```

### Selecting Your CDJ Model

Click the dropdown in the top-right corner to select your target player:

- **CDJ-2000 Nexus**: 24-bit / 48 kHz max, MP3/AAC/WAV/AIFF
- **CDJ-2000 NXS2**: 24-bit / 96 kHz max, adds FLAC support
- **CDJ-3000**: 24-bit / 96 kHz max, full format support including FLAC
- **XDJ-1000 MK2**: 24-bit / 96 kHz max
- **XDJ-700**: 24-bit / 48 kHz max

### Drag and Drop

You can drop:
- Individual audio files
- Folders containing audio files
- Multiple files/folders at once

**Supported file types for analysis:**
- MP3, AAC, M4A
- WAV, AIFF
- FLAC, ALAC
- OGG, Opus
- WMA

### Understanding Results

| Icon | Status | Meaning |
|------|--------|---------|
| ✅ | Compatible | File will play on your CDJ |
| ⚠️ | Convertible | File needs conversion (will be converted to WAV) |
| ❌ | Incompatible | File cannot be converted (rare) |

### Converting Files

1. After analysis, click **"Convert"**
2. The app will convert all ⚠️ files to CDJ-compatible WAV format
3. Progress will be shown with a progress bar
4. Cancel anytime by clicking "Cancel"

**Output Location:**
- Original: `/Music/my-track.flac`
- Converted: `/Music/CDJ_Ready/my-track.wav`

---

## Supported Formats

### Native Playback (No Conversion Needed)

| Format | CDJ-2000 NXS | CDJ-2000 NXS2 | CDJ-3000 | XDJ Series |
|--------|--------------|---------------|----------|------------|
| MP3 | ✅ | ✅ | ✅ | ✅ |
| AAC/M4A | ✅ | ✅ | ✅ | ✅ |
| WAV | ✅ | ✅ | ✅ | ✅ |
| AIFF | ✅ | ✅ | ✅ | ✅ |
| FLAC | ❌ | ✅ | ✅ | ✅ |
| ALAC | ❌ | ❌ | ✅ | ✅ |

### Formats Requiring Conversion

These formats will be automatically converted to WAV:

- FLAC (on CDJ-2000 Nexus)
- OGG / Opus
- WMA
- ALAC (on older players)

### Quality Settings

Converted files maintain maximum quality:
- **Bit Depth**: 24-bit (or 16-bit if source is 16-bit)
- **Sample Rate**: Up to 96 kHz (depending on player)
- **Codec**: Uncompressed PCM (WAV) or lossless AIFF

---

## CDJ Compatibility

### Maximum Quality by Player

| Player | Max Bit Depth | Max Sample Rate | Best Output Format |
|--------|---------------|-----------------|-------------------|
| CDJ-2000 Nexus | 24-bit | 48 kHz | WAV or AIFF |
| CDJ-2000 NXS2 | 24-bit | 96 kHz | WAV or AIFF |
| CDJ-3000 | 24-bit | 96 kHz | FLAC or WAV |
| XDJ-1000 MK2 | 24-bit | 96 kHz | WAV or AIFF |
| XDJ-700 | 24-bit | 48 kHz | WAV or AIFF |

### USB Drive Preparation

For best results when preparing USB drives for CDJs:

1. **Format**: Use FAT32 or HFS+ (Mac OS Extended)
2. **Structure**: Organize files in folders by genre/energy
3. **Rekordbox**: Use Pioneer Rekordbox to create playlists and hot cues
4. **Test**: Always test your USB on the actual CDJ before your gig

---

## Command Line Interface (CLI)

Dr. CDJ includes a command-line interface for automation and scripting.

### Installation (CLI Only)

```bash
pip install dr-cdj
```

### Basic Commands

#### Analyze a file

```bash
dr-cdj analyze /path/to/file.mp3 --player cdj-3000
```

**Output:**
```json
{
  "file": "/path/to/file.mp3",
  "codec": "mp3",
  "sample_rate": 44100,
  "bit_depth": null,
  "compatible": true
}
```

#### Batch analyze a folder

```bash
dr-cdj analyze /path/to/music/folder --player cdj-2000-nxs --output report.json
```

#### Convert files

```bash
dr-cdj convert /path/to/file.flac --player cdj-2000-nxs --output /path/to/output/
```

#### Batch convert

```bash
dr-cdj convert /path/to/music/folder --player cdj-3000
```

### CLI Options

```
Options:
  --player, -p     Target CDJ model (default: cdj-2000-nxs)
  --output, -o     Output directory or file
  --format, -f     Output format: wav, aiff, flac
  --recursive, -r  Process subdirectories
  --json, -j       Output JSON format
```

### Examples

**Check all files in a folder:**
```bash
dr-cdj analyze ~/Music/Gig-2024 --player cdj-3000 --recursive
```

**Convert incompatible files only:**
```bash
dr-cdj convert ~/Music/Gig-2024 --player cdj-2000-nxs --output ~/Music/Gig-2024-CDJ-Ready
```

**Generate a compatibility report:**
```bash
dr-cdj analyze ~/Music --player cdj-3000 --json > compatibility-report.json
```

---

## Troubleshooting

### Common Issues

#### "FFmpeg not found" error

**Solution:** Dr. CDJ will download FFmpeg automatically on first launch. Ensure you have an internet connection. If the download fails:

1. Check your internet connection
2. Restart the app
3. If the problem persists, install FFmpeg manually:
   ```bash
   brew install ffmpeg
   ```

#### "File cannot be converted" error

**Causes:**
- Corrupted file
- DRM-protected file (e.g., Apple Music downloads)
- Unsupported codec

**Solution:** Try playing the file in another player to verify it's not corrupted. DRM-protected files cannot be converted.

#### Conversion is very slow

**Solutions:**
1. Reduce the number of concurrent conversions in Settings
2. Ensure your drive has sufficient free space
3. Close other CPU-intensive applications
4. Use an SSD instead of HDD for better performance

#### App won't open (macOS security warning)

**Solution:**
1. Go to **System Settings** > **Privacy & Security**
2. Scroll down to "Security"
3. Click **"Open Anyway"** next to Dr. CDJ
4. Confirm in the dialog

#### Converted files don't play on CDJ

**Check:**
1. Did you select the correct CDJ model?
2. Is your USB drive formatted correctly (FAT32 or HFS+)?
3. Are the files in the CDJ_Ready folder?

### Getting Help

If you encounter issues not covered here:

1. Check the [GitHub Issues](https://github.com/IndigoAutomation/DR-CDJ/issues)
2. Email support: demos.indigo@gmail.com
3. Include the log file: `~/Library/Logs/Dr-CDJ/app.log`

---

## FAQ

### General Questions

**Q: Is Dr. CDJ free?**  
A: Yes! Dr. CDJ is completely free and open source under the MIT license.

**Q: Do I need internet to use Dr. CDJ?**  
A: Only for the first launch to download FFmpeg. After that, it works offline.

**Q: Will Dr. CDJ work on Windows or Linux?**  
A: Currently, Dr. CDJ is macOS only. Windows and Linux support may be added in the future.

### Technical Questions

**Q: Does conversion reduce audio quality?**  
A: No. When converting to WAV/AIFF, we use lossless conversion, preserving the original quality. Converting from lossy formats (MP3) to WAV doesn't restore lost data but doesn't degrade quality further.

**Q: Why convert to WAV instead of FLAC?**  
A: While FLAC is smaller, not all CDJ models support it. WAV has universal compatibility across all CDJ players.

**Q: Can I convert back from WAV to FLAC?**  
A: Yes, but it's not necessary for CDJ playback. You can use tools like `ffmpeg` or `XLD` for this.

**Q: Does Dr. CDJ modify my original files?**  
A: No. Original files are never modified. Converted files are saved in a separate `CDJ_Ready` folder.

### Usage Questions

**Q: How do I prepare a USB drive for CDJ?**  
A:
1. Format your USB as FAT32 or HFS+
2. Copy your files (use Dr. CDJ to convert incompatible ones first)
3. Optionally use Rekordbox to create playlists and analyze tracks
4. Test on the actual CDJ before your gig

**Q: Can I use Dr. CDJ with Rekordbox?**  
A: Yes! Use Dr. CDJ to ensure your files are compatible, then import them into Rekordbox for playlist management and hot cue preparation.

**Q: What's the best format for CDJ-3000?**  
A: The CDJ-3000 supports FLAC, so you can keep your FLAC files as-is. For maximum compatibility with older CDJs, use WAV or AIFF.

### Troubleshooting Questions

**Q: Why does analysis take so long?**  
A: Large files or slow drives (HDD, network drives) can slow down analysis. Using an SSD significantly speeds up the process.

**Q: Can I cancel a conversion?**  
A: Yes, click the "Cancel" button during conversion. Partially converted files will be cleaned up automatically.

**Q: Where are the log files?**  
A: Log files are stored at:
- GUI App: `~/Library/Logs/Dr-CDJ/app.log`
- CLI: Check your terminal output

---

## Tips for DJs

### Best Practices

1. **Always test before gigs**: Test your USB drive on the actual CDJ model you'll be using
2. **Keep backups**: Keep your original files and the converted CDJ_Ready folder
3. **Organize by energy**: Create folders like "Warm-up", "Peak-time", "Cool-down"
4. **Use consistent formats**: Stick to WAV or AIFF for maximum compatibility
5. **Check file names**: Avoid special characters in file names that might confuse CDJs

### Workflow Example

**Pre-gig preparation:**
1. Select tracks in your DJ software
2. Export/copy to a working folder
3. Drop folder into Dr. CDJ
4. Convert incompatible files
5. Copy CDJ_Ready folder to USB
6. Import into Rekordbox (optional)
7. Set hot cues and memory points
8. Test on actual CDJ hardware

---

**Dr. CDJ v1.0.1**  
Made with 🖤 for the underground  
https://indigoautomation.github.io/DR-CDJ/
