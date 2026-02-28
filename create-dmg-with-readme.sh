#!/bin/bash
# Crea DMG con README auto-apribile

set -e

APP_NAME="Dr-CDJ"
VERSION="1.0.1"
DMG_NAME="${APP_NAME}-${VERSION}-macOS.dmg"
VOLUME_NAME="Dr. CDJ"

echo "🎨 Creazione DMG con README auto-apribile..."

# Verifica che l'app esista
if [ ! -d "dist/${APP_NAME}.app" ]; then
    echo "❌ Errore: dist/${APP_NAME}.app non trovato"
    exit 1
fi

# Pulizia
rm -f "${DMG_NAME}" "${DMG_NAME}.tmp"

# Crea immagine disco temporanea
TEMP_DMG="${DMG_NAME}.tmp"
TEMP_MOUNT="/Volumes/${VOLUME_NAME} Build"

hdiutil create -size 100m -fs HFS+ -volname "${VOLUME_NAME}" -ov "${TEMP_DMG}"

# Monta
hdiutil attach "${TEMP_DMG}" -nobrowse

# Attendi mount
sleep 2

# Trova punto di mount
MOUNT_POINT=$(mount | grep "${VOLUME_NAME}" | head -1 | awk '{print $3}')
if [ -z "$MOUNT_POINT" ]; then
    MOUNT_POINT="/Volumes/${VOLUME_NAME}"
fi

echo "📁 Mount point: ${MOUNT_POINT}"

# Copia app
cp -R "dist/${APP_NAME}.app" "${MOUNT_POINT}/"

# Crea link ad Applications
ln -s /Applications "${MOUNT_POINT}/Applications"

# Copia README
cp "INSTALL.html" "${MOUNT_POINT}/README.html"

# Imposta README da aprire al mount
# Uso AppleScript per impostare la finestra del Finder
osascript << EOF
tell application "Finder"
    tell disk "${VOLUME_NAME}"
        open
        set current view of container window to icon view
        set toolbar visible of container window to false
        set statusbar visible of container window to false
        set the bounds of container window to {400, 100, 1000, 500}
        set theViewOptions to the icon view options of container window
        set arrangement of theViewOptions to not arranged
        set icon size of theViewOptions to 100
        set text size of theViewOptions to 13
        
        # Posizioni icone
        set position of item "${APP_NAME}.app" to {150, 200}
        set position of item "Applications" to {450, 200}
        set position of item "README.html" to {300, 350}
        
        update without registering applications
    end tell
end tell
EOF

# Apri README in Safari
open "${MOUNT_POINT}/README.html" || true

# Smonta
hdiutil detach "${MOUNT_POINT}" -force

# Converti in DMG compresso
hdiutil convert "${TEMP_DMG}" -format UDZO -ov -o "${DMG_NAME}"

# Pulizia
rm -f "${TEMP_DMG}"

# Aggiungi auto-open per README usando UltraDMG o altri tool
# Altrimenti impostiamo l'attributo extended

# Nota: L'auto-open richiederebbe un tool come dropdmg o create-dmg
# Per ora, il README è visibile e l'utente può doppio-clickarlo

echo ""
echo "✅ Creato: ${DMG_NAME}"
echo "📊 Dimensione: $(du -h "${DMG_NAME}" | cut -f1)"
echo ""
echo "💡 Il file README.html è incluso e visibile nel DMG"
echo "   Per aprirlo automaticamente, l'utente può doppio-clickarlo"
