#!/bin/bash
# Crea DMG con finestra di installazione stile macOS

set -e

APP_NAME="Dr-CDJ"
VERSION="1.0.1"
DMG_NAME="${APP_NAME}-${VERSION}-macOS.dmg"

echo "🎨 Creazione DMG installer per ${APP_NAME} v${VERSION}..."

# Verifica che l'app esista
if [ ! -d "dist/${APP_NAME}.app" ]; then
    echo "❌ Errore: dist/${APP_NAME}.app non trovato"
    echo "   Esegui prima: pyinstaller Dr-CDJ.spec"
    exit 1
fi

# Rimuovi DMG esistente
rm -f "${DMG_NAME}"

echo "📦 Creazione DMG con create-dmg..."

# Crea il DMG con create-dmg usando --app-drop-link
create-dmg \
    --volname "Dr. CDJ" \
    --volicon "CDJ-Check.icns" \
    --window-pos 200 120 \
    --window-size 600 400 \
    --icon-size 100 \
    --icon "Dr-CDJ.app" 150 185 \
    --hide-extension "Dr-CDJ.app" \
    --app-drop-link 450 185 \
    --no-internet-enable \
    "${DMG_NAME}" \
    "dist/"

echo ""
echo "✅ Creato: ${DMG_NAME}"
echo "📊 Dimensione: $(du -h "${DMG_NAME}" | cut -f1)"
echo ""
echo "💡 Per testare: open \"${DMG_NAME}\""
