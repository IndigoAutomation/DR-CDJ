#!/bin/bash
# Crea DMG manuale con layout

set -e

APP_NAME="Dr-CDJ"
VERSION="1.0.1"
DMG_NAME="${APP_NAME}-${VERSION}-macOS.dmg"
VOLUME_NAME="Dr. CDJ"

echo "🎨 Creazione DMG per ${APP_NAME} v${VERSION}..."

# Verifica
if [ ! -d "dist/${APP_NAME}.app" ]; then
    echo "❌ Errore: dist/${APP_NAME}.app non trovato"
    exit 1
fi

# Pulisci
rm -f "${DMG_NAME}" "${DMG_NAME}.temp"

# Crea DMG temporaneo
echo "📦 Creazione immagine temporanea..."
hdiutil create -size 150m -fs HFS+ -volname "${VOLUME_NAME}" -ov "${DMG_NAME}.temp"

# Monta
echo "📂 Mount..."
hdiutil attach "${DMG_NAME}.temp" -nobrowse
sleep 2

# Trova punto di mount
MOUNT_POINT=$(mount | grep "${VOLUME_NAME}" | grep -v "temp" | head -1 | awk '{print $3}')
if [ -z "$MOUNT_POINT" ]; then
    MOUNT_POINT="/Volumes/${VOLUME_NAME}"
fi

echo "📁 Mount point: ${MOUNT_POINT}"

# Copia contenuti
echo "📋 Copia contenuti..."
cp -R "dist/${APP_NAME}.app" "${MOUNT_POINT}/"
ln -sf /Applications "${MOUNT_POINT}/Applications"
cp "INSTALL.html" "${MOUNT_POINT}/README.html"

# Aspetta che il Finder aggiorni
sleep 2

# Smonta
echo "💾 Smontaggio..."
hdiutil detach "${MOUNT_POINT}" -force

# Converti in DMG compresso
echo "🗜  Compressione..."
hdiutil convert "${DMG_NAME}.temp" -format UDZO -ov -o "${DMG_NAME}"

# Pulisci
rm -f "${DMG_NAME}.temp"

echo ""
echo "✅ Creato: ${DMG_NAME}"
echo "📊 Dimensione: $(du -h "${DMG_NAME}" | cut -f1)"
