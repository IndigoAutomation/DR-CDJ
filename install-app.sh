#!/bin/bash
# Installazione Dr. CDJ per macOS

echo "🎵 Dr. CDJ - Installazione"
echo "=========================="

# Verifica che il DMG sia montato o l'app sia presente
if [ -d "Dr-CDJ.app" ]; then
    APP_PATH="Dr-CDJ.app"
elif [ -d "/Volumes/Dr. CDJ/Dr-CDJ.app" ]; then
    APP_PATH="/Volumes/Dr. CDJ/Dr-CDJ.app"
else
    echo "❌ Errore: Dr-CDJ.app non trovato"
    echo "   Assicurati di aver montato il DMG o di essere nella stessa cartella dell'app"
    exit 1
fi

echo "📦 Installazione da: $APP_PATH"

# Rimuovi vecchia versione
if [ -d "/Applications/Dr-CDJ.app" ]; then
    echo "🗑  Rimozione versione precedente..."
    rm -rf "/Applications/Dr-CDJ.app"
fi

# Copia app
echo "📋 Copia in Applications..."
cp -R "$APP_PATH" "/Applications/Dr-CDJ.app"

# Rimuovi attributo quarantena (permesso da non identificato)
echo "🔓 Rimozione quarantena..."
xattr -rd com.apple.quarantine "/Applications/Dr-CDJ.app" 2>/dev/null || true

# Verifica installazione
if [ -d "/Applications/Dr-CDJ.app" ]; then
    echo ""
    echo "✅ Installazione completata!"
    echo ""
    echo "🚀 Per avviare Dr. CDJ:"
    echo "   open /Applications/Dr-CDJ.app"
    echo "   oppure cerca 'Dr. CDJ' in Spotlight"
    echo ""
    echo "⚠️  Nota: La prima volta potrebbe chiedere conferma per avviare"
    echo "   l'app da uno sviluppatore non identificato."
    echo "   Vai in Preferenze di Sistema > Sicurezza e Privacy per consentire."
else
    echo "❌ Errore durante l'installazione"
    exit 1
fi
