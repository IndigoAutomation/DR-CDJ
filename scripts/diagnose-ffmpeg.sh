#!/bin/bash
# Dr. CDJ FFmpeg Diagnostic Tool
# Run this if you get "FFmpeg Not Found" error
# Usage: bash diagnose-ffmpeg.sh

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     Dr. CDJ - FFmpeg Diagnostic Tool                      ║"
echo "║     Helps fix "FFmpeg Not Found" errors                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

ERRORS=0
WARNINGS=0

print_section() {
    echo ""
    echo -e "${BLUE}▶ $1${NC}"
    echo "─────────────────────────────────────────────────────────────"
}

print_ok() {
    echo -e "${GREEN}  ✓${NC} $1"
}

print_error() {
    echo -e "${RED}  ✗${NC} $1"
    ((ERRORS++))
}

print_warning() {
    echo -e "${YELLOW}  !${NC} $1"
    ((WARNINGS++))
}

# Check 1: macOS Version
print_section "Checking macOS Version"
OS_VERSION=$(sw_vers -productVersion 2>/dev/null || echo "unknown")
ARCH=$(uname -m)
echo "  macOS: $OS_VERSION"
echo "  Architecture: $ARCH"

if [[ "$OS_VERSION" == 1[0-9]* ]] || [[ "$OS_VERSION" == [2-9][0-9]* ]]; then
    print_ok "macOS version is supported (10.15+)"
else
    print_warning "macOS version may be too old (need 10.15+)"
fi

# Check 2: App Bundle
print_section "Checking Dr. CDJ App Bundle"
APP_PATH=""
if [ -d "/Applications/Dr-CDJ.app" ]; then
    APP_PATH="/Applications/Dr-CDJ.app"
    print_ok "Found app in /Applications"
elif [ -d "$HOME/Applications/Dr-CDJ.app" ]; then
    APP_PATH="$HOME/Applications/Dr-CDJ.app"
    print_ok "Found app in ~/Applications"
else
    print_error "Dr. CDJ.app not found in Applications"
    echo "  Please install Dr. CDJ first"
fi

# Check 3: Bundled FFmpeg
print_section "Checking Bundled FFmpeg"
if [ -n "$APP_PATH" ]; then
    BUNDLED_FOUND=false
    
    for location in "Frameworks/bin" "Resources/bin" "MacOS/bin"; do
        FFMPEG="$APP_PATH/Contents/$location/ffmpeg"
        FFPROBE="$APP_PATH/Contents/$location/ffprobe"
        
        if [ -f "$FFMPEG" ] && [ -f "$FFPROBE" ]; then
            print_ok "Found bundled FFmpeg in $location"
            ls -lh "$FFMPEG" "$FFPROBE" | sed 's/^/    /'
            BUNDLED_FOUND=true
            break
        fi
    done
    
    if [ "$BUNDLED_FOUND" = false ]; then
        print_error "No bundled FFmpeg found in app"
    fi
else
    print_warning "Skipping (app not found)"
fi

# Check 4: Cache Directory
print_section "Checking Dr. CDJ Cache"
CACHE_DIR="$HOME/.dr_cdj/bin"
if [ -d "$CACHE_DIR" ]; then
    print_ok "Cache directory exists"
    
    CACHED_FFMPEG="$CACHE_DIR/ffmpeg"
    CACHED_FFPROBE="$CACHE_DIR/ffprobe"
    
    if [ -f "$CACHED_FFMPEG" ]; then
        print_ok "Cached ffmpeg found"
        
        # Test if working
        if "$CACHED_FFMPEG" -version >/dev/null 2>&1; then
            print_ok "Cached ffmpeg is working"
        else
            print_error "Cached ffmpeg exists but NOT working"
            echo "    Try: rm -rf ~/.dr_cdj/bin/*"
        fi
    else
        print_error "No cached ffmpeg"
    fi
    
    if [ -f "$CACHED_FFPROBE" ]; then
        print_ok "Cached ffprobe found"
    else
        print_error "No cached ffprobe"
    fi
else
    print_error "Cache directory does not exist"
    echo "    This is normal for first launch"
fi

# Check 5: System FFmpeg
print_section "Checking System FFmpeg"
if command -v ffmpeg >/dev/null 2>&1; then
    SYSTEM_FFMPEG=$(which ffmpeg)
    print_ok "System ffmpeg found: $SYSTEM_FFMPEG"
    ffmpeg -version 2>&1 | head -1 | sed 's/^/    /'
else
    print_warning "No system ffmpeg installed"
    echo "    Install with: brew install ffmpeg"
fi

if command -v ffprobe >/dev/null 2>&1; then
    print_ok "System ffprobe found"
else
    print_warning "No system ffprobe installed"
fi

# Check 6: Quarantine
print_section "Checking macOS Security (Quarantine)"
if [ -n "$APP_PATH" ]; then
    QUARANTINE=$(xattr "$APP_PATH" 2>/dev/null | grep -i quarantine || true)
    
    if [ -n "$QUARANTINE" ]; then
        print_error "App has quarantine attributes!"
        echo "    This blocks bundled binaries from running"
        echo ""
        echo -e "${YELLOW}    TO FIX, RUN:${NC}"
        echo "    xattr -rd com.apple.quarantine $APP_PATH"
        echo ""
    else
        print_ok "No quarantine attributes"
    fi
else
    print_warning "Skipping (app not found)"
fi

# Check 7: Log File
print_section "Checking Log File"
LOG_FILE="$HOME/Library/Logs/Dr-CDJ/app.log"
if [ -f "$LOG_FILE" ]; then
    print_ok "Log file exists"
    echo "    Last 5 lines:"
    tail -5 "$LOG_FILE" | sed 's/^/      /'
else
    print_warning "No log file found (app may not have run yet)"
fi

# Summary
echo ""
echo "═════════════════════════════════════════════════════════════"
echo "                      DIAGNOSIS SUMMARY"
echo "═════════════════════════════════════════════════════════════"
echo ""

if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed!${NC}"
    echo ""
    echo "If you're still seeing 'FFmpeg Not Found', please:"
    echo "1. Check Console.app for detailed error messages"
    echo "2. Try reinstalling the app"
    echo "3. Contact support with the log file"
    exit 0
fi

echo -e "${RED}Found $ERRORS error(s) and $WARNINGS warning(s)${NC}"
echo ""

# Offer fixes
echo "═════════════════════════════════════════════════════════════"
echo "                      RECOMMENDED FIXES"
echo "═════════════════════════════════════════════════════════════"
echo ""

# Fix 1: Quarantine
if [ -n "$APP_PATH" ]; then
    QUARANTINE=$(xattr "$APP_PATH" 2>/dev/null | grep -i quarantine || true)
    if [ -n "$QUARANTINE" ]; then
        echo -e "${YELLOW}1. Remove Quarantine (CRITICAL)${NC}"
        echo "   Run this command in Terminal:"
        echo ""
        echo "   xattr -rd com.apple.quarantine \"$APP_PATH\""
        echo ""
    fi
fi

# Fix 2: Missing bundled FFmpeg
if [ -n "$APP_PATH" ] && [ "$BUNDLED_FOUND" = false ]; then
    echo -e "${YELLOW}2. Install FFmpeg Manually${NC}"
    echo "   The app bundle is missing FFmpeg. Install it system-wide:"
    echo ""
    echo "   Option A - Using Homebrew (recommended):"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo "   brew install ffmpeg"
    echo ""
    echo "   Option B - Download manually:"
    echo "   Visit: https://evermeet.cx/ffmpeg/"
    echo "   Download ffmpeg and ffprobe, then extract to ~/.dr_cdj/bin/"
    echo ""
fi

# Fix 3: Cache issues
if [ -d "$CACHE_DIR" ]; then
    if [ ! -f "$CACHE_DIR/ffmpeg" ] || [ ! -f "$CACHE_DIR/ffprobe" ]; then
        echo -e "${YELLOW}3. Fix Cache Directory${NC}"
        echo "   Clear corrupted cache:"
        echo ""
        echo "   rm -rf ~/.dr_cdj/bin/*"
        echo ""
        echo "   Then relaunch the app"
        echo ""
    fi
fi

# Fix 4: First launch without bundled FFmpeg
if [ "$BUNDLED_FOUND" = false ] && [ ! -d "$CACHE_DIR" ]; then
    echo -e "${YELLOW}4. First Launch Setup${NC}"
    echo "   The app needs internet to download FFmpeg on first launch."
    echo "   Ensure you have a stable internet connection and try again."
    echo ""
fi

echo "═════════════════════════════════════════════════════════════"
echo ""
echo "If problems persist, please share this output and the log file:"
echo "  ~/Library/Logs/Dr-CDJ/app.log"
echo ""
echo "Support: demos.indigo@gmail.com"
echo ""
