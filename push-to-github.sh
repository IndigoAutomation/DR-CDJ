#!/bin/bash
# Script per pushare CDJ-Check su GitHub

set -e

echo "🚀 CDJ-Check GitHub Push Script"
echo "================================"
echo ""

# Verifica che git sia inizializzato
if [ ! -d ".git" ]; then
    echo "❌ Repository git non inizializzata!"
    exit 1
fi

# Chiedi conferma username
echo "Il repository verrà pushato su: https://github.com/filippoitaliano/cdj-check"
echo ""
read -p "Premi INVIO per continuare o Ctrl+C per annullare..."

# Configura remote
echo ""
echo "🔧 Configurazione remote..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/filippoitaliano/cdj-check.git

# Assicurati di essere su main
git branch -M main

# Push
echo ""
echo "📤 Push in corso..."
git push -u origin main

echo ""
echo "✅ Push completato con successo!"
echo ""
echo "🌐 Visita la tua repository: https://github.com/filippoitaliano/cdj-check"
