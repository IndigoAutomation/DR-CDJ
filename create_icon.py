#!/usr/bin/env python3
"""Genera l'icona dell'applicazione CDJ-Check per macOS."""

import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def create_icon(size: int) -> Image.Image:
    """Crea un'icona della dimensione specificata."""
    
    # Crea immagine con trasparenza
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Colori tema (indigo/purple gradient)
    color_primary = (99, 102, 241)  # #6366f1
    color_secondary = (139, 92, 246)  # #8b5cf6
    color_accent = (236, 72, 153)  # #ec4899
    
    # Cerchio sfondo con gradiente simulato
    margin = size // 20
    bbox = [margin, margin, size - margin, size - margin]
    
    # Disegna cerchio sfumato
    for i in range(size // 2, margin, -1):
        ratio = (i - margin) / (size // 2 - margin)
        r = int(color_primary[0] * ratio + color_secondary[0] * (1 - ratio))
        g = int(color_primary[1] * ratio + color_secondary[1] * (1 - ratio))
        b = int(color_primary[2] * ratio + color_secondary[2] * (1 - ratio))
        
        draw.ellipse(
            [size//2 - i, size//2 - i, size//2 + i, size//2 + i],
            fill=(r, g, b, 255)
        )
    
    # Disegna simbolo "vinile/disco" al centro
    center = size // 2
    disc_radius = int(size * 0.28)
    
    # Cerchio esterno (disco)
    draw.ellipse(
        [center - disc_radius, center - disc_radius,
         center + disc_radius, center + disc_radius],
        fill=(30, 30, 35, 230),
        outline=(255, 255, 255, 100),
        width=max(1, size // 50)
    )
    
    # Cerchio intermedio
    mid_radius = int(disc_radius * 0.7)
    draw.ellipse(
        [center - mid_radius, center - mid_radius,
         center + mid_radius, center + mid_radius],
        outline=(255, 255, 255, 60),
        width=max(1, size // 80)
    )
    
    # Cerchio centro (etichetta)
    label_radius = int(disc_radius * 0.35)
    draw.ellipse(
        [center - label_radius, center - label_radius,
         center + label_radius, center + label_radius],
        fill=(236, 72, 153, 200),  # Pink accent
    )
    
    # Checkmark ✓
    check_size = int(size * 0.15)
    check_thickness = max(2, size // 25)
    
    # Coordinate checkmark
    x1 = center - int(check_size * 0.5)
    y1 = center - int(check_size * 0.1)
    x2 = center - int(check_size * 0.1)
    y2 = center + int(check_size * 0.3)
    x3 = center + int(check_size * 0.5)
    y3 = center - int(check_size * 0.4)
    
    # Disegna checkmark
    draw.line([(x1, y1), (x2, y2)], fill=(255, 255, 255, 255), width=check_thickness)
    draw.line([(x2, y2), (x3, y3)], fill=(255, 255, 255, 255), width=check_thickness)
    
    # Aggiungi ombra sotto
    shadow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_offset = size // 15
    shadow_draw.ellipse(
        [margin + shadow_offset, margin + shadow_offset, 
         size - margin + shadow_offset, size - margin + shadow_offset],
        fill=(0, 0, 0, 40)
    )
    
    # Combina ombra e icona
    result = Image.alpha_composite(shadow, img)
    
    return result


def create_icns():
    """Crea il file .icns per macOS."""
    
    sizes = [16, 32, 64, 128, 256, 512, 1024]
    iconset_dir = Path("CDJ-Check.iconset")
    iconset_dir.mkdir(exist_ok=True)
    
    print("🎨 Generazione icone...")
    
    for size in sizes:
        # Dimensione normale
        img = create_icon(size)
        img.save(iconset_dir / f"icon_{size}x{size}.png")
        print(f"  ✓ {size}x{size}")
        
        # Dimensione retina (@2x)
        if size <= 512:
            img_2x = create_icon(size * 2)
            img_2x.save(iconset_dir / f"icon_{size}x{size}@2x.png")
            print(f"  ✓ {size}x{size}@2x")
    
    # Crea file .icns usando iconutil
    icns_path = Path("CDJ-Check.icns")
    
    try:
        subprocess.run(
            ["iconutil", "-c", "icns", str(iconset_dir)],
            check=True,
            capture_output=True
        )
        print(f"\n✅ Icona creata: {icns_path.absolute()}")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Errore creazione .icns: {e}")
        print("   Creazione fallback PNG...")
        
        # Fallback: salva solo l'icona 512x512
        img_512 = create_icon(512)
        img_512.save("CDJ-Check.png")
        print(f"   ✅ Salvato: CDJ-Check.png (512x512)")
    
    # Pulizia directory temporanea
    import shutil
    if iconset_dir.exists():
        shutil.rmtree(iconset_dir)
    
    # Crea anche versioni singole per usi vari
    print("\n📦 Creazione icone aggiuntive...")
    
    # Logo grande per README/app
    logo_1024 = create_icon(1024)
    logo_1024.save("assets/logo_1024.png")
    print("  ✓ assets/logo_1024.png")
    
    # Logo medio per documentazione
    logo_512 = create_icon(512)
    logo_512.save("assets/logo_512.png")
    print("  ✓ assets/logo_512.png")
    
    # Logo piccolo per favicon/UI
    logo_256 = create_icon(256)
    logo_256.save("assets/logo_256.png")
    print("  ✓ assets/logo_256.png")
    
    print("\n✨ Completato!")


def main():
    """Entry point."""
    # Crea directory assets se non esiste
    assets_dir = Path("assets")
    assets_dir.mkdir(exist_ok=True)
    
    create_icns()
    
    print("\n" + "="*50)
    print("📋 ISTRUZIONI PER L'USO:")
    print("="*50)
    print("""
Per usare l'icona con PyInstaller:

1. Aggiungi al file .spec:
   app = BUNDLE(
       ...
       icon='CDJ-Check.icns',
       ...
   )

2. O usa la riga di comando:
   pyinstaller --windowed --icon=CDJ-Check.icns ...

Per creare un bundle .app manuale:
   1. Crea la struttura: CDJ-Check.app/Contents/MacOS/
   2. Crea la struttura: CDJ-Check.app/Contents/Resources/
   3. Copia CDJ-Check.icns in Resources/
   4. Crea il Info.plist con CFBundleIconFile = CDJ-Check
    """)


if __name__ == "__main__":
    main()
