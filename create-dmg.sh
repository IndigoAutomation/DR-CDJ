#!/bin/bash
# Crea il DMG per la release macOS

set -e

APP_NAME="Dr. CDJ"
VERSION="1.0.0"
DMG_NAME="${APP_NAME}-${VERSION}-macOS.dmg"

echo "🎨 Creazione DMG per ${APP_NAME} v${VERSION}..."

# Verifica che l'app esista
if [ ! -d "dist/${APP_NAME}.app" ]; then
    echo "❌ Errore: dist/${APP_NAME}.app non trovato"
    echo "   Esegui prima: pyinstaller Dr. CDJ.spec"
    exit 1
fi

# Crea directory temporanea
TMP_DIR=$(mktemp -d)
mkdir -p "${TMP_DIR}/${APP_NAME}"

# Copia app
cp -R "dist/${APP_NAME}.app" "${TMP_DIR}/${APP_NAME}/"

# Crea link ad Applications
ln -s /Applications "${TMP_DIR}/${APP_NAME}/Applications"

# Crea README
"""cat > "${TMP_DIR}/${APP_NAME}/README.txt" << 'EOF'
Dr. CDJ v1.0.0
================

Grazie per aver scaricato Dr. CDJ!

INSTALLAZIONE:
1. Trascina Dr. CDJ.app nella cartella Applications
2. Doppio click su Dr. CDJ.app per avviare

REQUISITI:
- macOS 12.0 o superiore
- FFmpeg installato (opzionale ma consigliato)

Per installare FFmpeg:
   brew install ffmpeg

SUPPORTO:
https://github.com/tuousername/dr-cdj/issues
EOF
"""

# Crea DMG
echo "📦 Creazione ${DMG_NAME}..."

# Usa hdiutil per creare il DMG
hdiutil create \
    -volname "${APP_NAME}" \
    -srcfolder "${TMP_DIR}/${APP_NAME}" \
    -ov \
    -format UDZO \
    "${DMG_NAME}"

# Pulizia
rm -rf "${TMP_DIR}"

echo "✅ Creato: ${DMG_NAME}"
echo "📊 Dimensione: $(du -h "${DMG_NAME}" | cut -f1)"
