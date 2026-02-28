# Troubleshooting: "FFmpeg Not Found" Error

This guide helps diagnose and fix the "FFmpeg Not Found" error that some users experience when launching Dr. CDJ.

## Quick Diagnosis

Run this diagnostic script on the user's Mac:

```bash
#!/bin/bash
echo "=== Dr. CDJ FFmpeg Diagnostics ==="
echo ""
echo "1. Checking app bundle..."
ls -la /Applications/Dr-CDJ.app/Contents/Frameworks/bin/ 2>/dev/null || echo "   Not found in Frameworks/bin"
ls -la /Applications/Dr-CDJ.app/Contents/Resources/bin/ 2>/dev/null || echo "   Not found in Resources/bin"

echo ""
echo "2. Checking cache directory..."
ls -la ~/.dr_cdj/bin/ 2>/dev/null || echo "   Cache directory does not exist"

echo ""
echo "3. Checking system FFmpeg..."
which ffmpeg || echo "   ffmpeg not in PATH"
which ffprobe || echo "   ffprobe not in PATH"

echo ""
echo "4. Checking quarantine attributes..."
xattr /Applications/Dr-CDJ.app 2>/dev/null | grep -i quarantine && echo "   WARNING: App is quarantined!"

echo ""
echo "5. Checking log file..."
cat ~/Library/Logs/Dr-CDJ/app.log 2>/dev/null | tail -20 || echo "   No log file found"
```

## Common Causes & Solutions

### 1. App Bundle Missing FFmpeg Binaries

**Symptoms:**
- Fresh install on new Mac
- App shows "FFmpeg Not Found" immediately on launch
- Cache directory doesn't exist or is empty

**Cause:** The build process didn't include FFmpeg binaries in the app bundle.

**Solution:**
```bash
# Check if binaries are in the app
cd /Applications/Dr-CDJ.app/Contents
find . -name "ffmpeg" -o -name "ffprobe"

# If not found, the user needs to either:
# Option A: Install FFmpeg manually
brew install ffmpeg

# Option B: Rebuild the app with binaries included
# (Developer needs to run this before creating the DMG)
python scripts/download-ffmpeg.py
python build.py
```

### 2. Quarantine/Gatekeeper Blocking Binaries

**Symptoms:**
- App was downloaded from browser
- Binaries exist in bundle but don't execute
- Console shows permission denied errors

**Solution:**
```bash
# Remove quarantine attributes
xattr -rd com.apple.quarantine /Applications/Dr-CDJ.app

# Also remove from bundled binaries specifically
xattr -rd com.apple.quarantine /Applications/Dr-CDJ.app/Contents/Frameworks/bin/ffmpeg
xattr -rd com.apple.quarantine /Applications/Dr-CDJ.app/Contents/Frameworks/bin/ffprobe
```

### 3. Cache Directory Permission Issues

**Symptoms:**
- App tries to copy bundled FFmpeg but fails
- Cache directory (~/.dr_cdj/bin) doesn't exist
- Error in logs about "Permission denied"

**Solution:**
```bash
# Create cache directory manually
mkdir -p ~/.dr_cdj/bin

# Copy bundled binaries manually
cp /Applications/Dr-CDJ.app/Contents/Frameworks/bin/ffmpeg ~/.dr_cdj/bin/
cp /Applications/Dr-CDJ.app/Contents/Frameworks/bin/ffprobe ~/.dr_cdj/bin/

# Make executable
chmod +x ~/.dr_cdj/bin/ffmpeg ~/.dr_cdj/bin/ffprobe

# Test
~/.dr_cdj/bin/ffmpeg -version
```

### 4. Network Download Failed

**Symptoms:**
- No bundled FFmpeg in app
- No system FFmpeg installed
- User has internet connection issues
- Cache directory empty

**Solution:**
```bash
# Install FFmpeg via Homebrew (recommended)
brew install ffmpeg

# Or download manually from https://evermeet.cx/ffmpeg/
# Extract to ~/.dr_cdj/bin/
```

### 5. Corrupted Cache

**Symptoms:**
- Cache directory exists with files
- Binaries exist but don't work
- Error when running ffmpeg -version

**Solution:**
```bash
# Clear cache and let app re-download
rm -rf ~/.dr_cdj/bin/*

# Or install fresh copy
curl -L https://evermeet.cx/ffmpeg/ffmpeg-6.1.1.zip -o /tmp/ffmpeg.zip
unzip /tmp/ffmpeg.zip -d ~/.dr_cdj/bin/
mv ~/.dr_cdj/bin/ffmpeg-* ~/.dr_cdj/bin/ffmpeg
chmod +x ~/.dr_cdj/bin/ffmpeg
```

## Detailed Flow

Understanding the FFmpeg detection flow helps diagnose issues:

```
App Launch
    │
    ├─→ 1. Check bundled FFmpeg in app
    │      ├─→ Copy to ~/.dr_cdj/bin/ ✓
    │      └─→ If fails, continue...
    │
    ├─→ 2. Check cached FFmpeg (~/.dr_cdj/bin/) ✓
    │
    ├─→ 3. Check system FFmpeg (PATH) ✓
    │
    └─→ 4. Download from internet ✓
         └─→ If all fail → ERROR "FFmpeg Not Found"
```

## Prevention (For Developers)

### Ensure FFmpeg is bundled in the build:

```bash
# Before building the app:
python scripts/download-ffmpeg.py

# Verify binaries are in place:
ls src/dr_cdj/bin/
# Should show: ffmpeg, ffprobe

# Build the app:
python build.py

# Verify binaries in the built app:
ls dist/Dr-CDJ.app/Contents/Frameworks/bin/
```

### Post-build verification:

```bash
# Create DMG
cd dist
hdiutil create -volname "Dr. CDJ" -srcfolder Dr-CDJ.app -ov -format UDZO Dr-CDJ.dmg

# Test on clean macOS VM or new user account
```

## User Workarounds

If the user can't wait for a fix:

### Option 1: Install FFmpeg via Homebrew (Easiest)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install ffmpeg
```

### Option 2: Manual Download
1. Download FFmpeg from https://evermeet.cx/ffmpeg/
2. Extract the zip file
3. Create directory: `mkdir -p ~/.dr_cdj/bin`
4. Copy files:
   ```bash
   cp ~/Downloads/ffmpeg ~/.dr_cdj/bin/
   cp ~/Downloads/ffprobe ~/.dr_cdj/bin/
   chmod +x ~/.dr_cdj/bin/*
   ```

### Option 3: Use CLI Version
```bash
pip install dr-cdj
dr-cdj analyze /path/to/file.mp3
```

## Reporting Issues

When users report this issue, ask for:

1. **macOS Version**: `sw_vers -productVersion`
2. **App Installation Method**: DMG download / Git clone / pip install
3. **Diagnostic Output**: Run the script at the top of this file
4. **Log File**: `~/Library/Logs/Dr-CDJ/app.log`
5. **Error Screenshot**: What exactly does the error dialog say?

## Known Issues

### Issue: Rosetta 2 on Apple Silicon
**Status:** Fixed in v1.0.1

The x86_64 FFmpeg binary was slow to start via Rosetta 2, causing timeouts. Fixed by checking file existence before verification.

### Issue: Gatekeeper on macOS 14+
**Status:** Investigating

macOS Sonoma may block bundled binaries more aggressively. Solution: Remove quarantine attributes.

---

**Last Updated:** 2024-02-28  
**Applies to:** Dr. CDJ v1.0.1
