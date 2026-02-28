# 🎨 Icone CDJ-Check

Questa cartella contiene le icone dell'applicazione CDJ-Check.

## Icone Generate

| File | Dimensione | Uso |
|------|-----------|-----|
| `../CDJ-Check.icns` | Multi-risoluzione | Icona app macOS (Dock, Finder) |
| `logo_1024.png` | 1024x1024 | App Store, marketing |
| `logo_512.png` | 512x512 | Icona alta risoluzione |
| `logo_256.png` | 256x256 | Icona media risoluzione |

## Utilizzo con PyInstaller

### Metodo 1: Linea di comando
```bash
pyinstaller --windowed --name="CDJ-Check" --icon=CDJ-Check.icns src/dr_cdj/gui.py
```

### Metodo 2: File .spec
Modifica il file `CDJ-Check.spec`:

```python
app = BUNDLE(
    exe,
    name='CDJ-Check.app',
    icon='CDJ-Check.icns',  # <-- Aggiungi questa riga
    bundle_identifier='com.tuonome.cdjcheck',
)
```

## Utilizzo Manuale (App Bundle)

Per creare manualmente un bundle `.app`:

```bash
# Crea struttura
mkdir -p CDJ-Check.app/Contents/MacOS
mkdir -p CDJ-Check.app/Contents/Resources

# Copia icona
cp CDJ-Check.icns CDJ-Check.app/Contents/Resources/

# Copia eseguibile
cp dist/CDJ-Check CDJ-Check.app/Contents/MacOS/

# Crea Info.plist
cat > CDJ-Check.app/Contents/Info.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>CDJ-Check</string>
    <key>CFBundleIconFile</key>
    <string>CDJ-Check</string>
    <key>CFBundleIdentifier</key>
    <string>com.tuonome.cdjcheck</string>
    <key>CFBundleName</key>
    <string>CDJ-Check</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.12</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF
```

## Design

L'icona rappresenta:
- **Sfondo gradiente** indigo-purple: tema moderno dell'app
- **Disco/Vinile**: riferimento ai CDJ Pioneer
- **Checkmark rosa**: verifica compatibilità completata
- **Ombra**: profondità per il dock macOS

## Rigenera Icone

Se vuoi modificare il design:

```bash
python3 create_icon.py
```

Lo script rigenererà tutte le icone nella cartella `assets/`.
