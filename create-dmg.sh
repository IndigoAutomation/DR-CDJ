#!/bin/bash
# Create DMG for macOS release

set -e

APP_NAME="Dr-CDJ"
VERSION="1.0.1"
DMG_NAME="Dr-CDJ-${VERSION}-macOS.dmg"

echo "🎨 Creating DMG for ${APP_NAME} v${VERSION}..."

# Check that the app exists
if [ ! -d "dist/${APP_NAME}.app" ]; then
    echo "❌ Error: dist/${APP_NAME}.app not found"
    echo "   Run first: python3 build.py"
    exit 1
fi

# Create temp directory
TMP_DIR=$(mktemp -d)
mkdir -p "${TMP_DIR}/${APP_NAME}"

# Copy app
cp -R "dist/${APP_NAME}.app" "${TMP_DIR}/${APP_NAME}/"

# Ensure FFmpeg binaries inside the bundle are executable
find "${TMP_DIR}/${APP_NAME}/${APP_NAME}.app" \( -name "ffmpeg" -o -name "ffprobe" \) | while read -r f; do
    [ -f "$f" ] && chmod +x "$f"
done

# Create link to Applications
ln -s /Applications "${TMP_DIR}/${APP_NAME}/Applications"

# Copy install guide
cp "INSTALL.html" "${TMP_DIR}/${APP_NAME}/INSTALL.html"

# Create DMG
echo "📦 Creating ${DMG_NAME}..."

# Use hdiutil to create DMG
hdiutil create \
    -volname "Dr. CDJ" \
    -srcfolder "${TMP_DIR}/${APP_NAME}" \
    -ov \
    -format UDZO \
    "${DMG_NAME}"

# Cleanup
rm -rf "${TMP_DIR}"

echo "✅ Created: ${DMG_NAME}"
echo "📊 Size: $(du -h "${DMG_NAME}" | cut -f1)"
