#!/bin/bash
# Crea DMG finale con README e layout personalizzato

set -e

APP_NAME="Dr-CDJ"
VERSION="1.0.1"
DMG_NAME="${APP_NAME}-${VERSION}-macOS.dmg"

echo "🎨 Creazione DMG finale per ${APP_NAME} v${VERSION}..."

# Verifica
if [ ! -d "dist/${APP_NAME}.app" ]; then
    echo "❌ Errore: dist/${APP_NAME}.app non trovato"
    exit 1
fi

# Prepara directory temporanea
TMP_DIR=$(mktemp -d)
mkdir -p "${TMP_DIR}"

echo "📁 Preparazione contenuti..."

# Copia app
cp -R "dist/${APP_NAME}.app" "${TMP_DIR}/"

# Crea link ad Applications
ln -s /Applications "${TMP_DIR}/Applications"

# Copia README
cp "INSTALL.html" "${TMP_DIR}/README.html"

# Pulisci DMG precedenti
rm -f "${DMG_NAME}" "${DMG_NAME}.temp"

echo "📦 Creazione DMG con create-dmg..."

# Crea DMG con create-dmg
create-dmg \
    --volname "Dr. CDJ" \
    --volicon "CDJ-Check.icns" \
    --window-pos 200 100 \
    --window-size 600 500 \
    --icon-size 100 \
    --icon "Dr-CDJ.app" 150 220 \
    --icon "Applications" 450 220 \
    --icon "README.html" 300 380 \
    --hide-extension "Dr-CDJ.app" \
    --app-drop-link 450 220 \
    --no-internet-enable \
    "${DMG_NAME}" \
    "${TMP_DIR}"

# Pulisci
rm -rf "${TMP_DIR}"

echo ""
echo "✅ Creato: ${DMG_NAME}"
echo "📊 Dimensione: $(du -h "${DMG_NAME}" | cut -f1)"
echo ""
echo "📄 Contenuto:"
echo "   • Dr-CDJ.app"
echo "   • Applications (link)"
echo "   • README.html"
echo ""
echo "💡 Test: open \"${DMG_NAME}\""
