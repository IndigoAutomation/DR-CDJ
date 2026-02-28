# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Dr. CDJ
Builds a standalone macOS app with bundled FFmpeg
"""

import platform
from pathlib import Path

block_cipher = None

# Determine bundled FFmpeg paths
# These are downloaded by scripts/download-ffmpeg.py before build
bin_dir = Path('src/dr_cdj/bin')
ffmpeg_bundled = bin_dir / 'ffmpeg'
ffprobe_bundled = bin_dir / 'ffprobe'

# Use bundled FFmpeg if available, otherwise fall back to system
binaries = []
if ffmpeg_bundled.exists() and ffprobe_bundled.exists():
    print(f"✅ Using bundled FFmpeg from {bin_dir}")
    binaries = [
        (str(ffmpeg_bundled), 'bin'),
        (str(ffprobe_bundled), 'bin'),
    ]
else:
    print("⚠️  Bundled FFmpeg not found, trying system FFmpeg...")
    import shutil
    ffmpeg_system = shutil.which('ffmpeg')
    ffprobe_system = shutil.which('ffprobe')
    if ffmpeg_system and ffprobe_system:
        binaries = [
            (ffmpeg_system, '.'),
            (ffprobe_system, '.'),
        ]
    else:
        print("⚠️  No FFmpeg found - app will download at runtime")

a = Analysis(
    ['src/dr_cdj/main.py'],
    pathex=['src'],
    binaries=binaries,
    datas=[
        ('src/dr_cdj/splash.py', 'dr_cdj'),
    ],
    hiddenimports=[
        'customtkinter',
        'tkinterdnd2',
        'PIL',
        'PIL._tkinter_finder',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
    ],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,  # IMPORTANTE: per onedir mode
    name='Dr-CDJ',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False per GUI
    disable_windowed_traceback=False,
    argv_emulation=True,  # IMPORTANTE per macOS
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# ONDIR MODE - più stabile per macOS app bundles
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[
        'ffmpeg',      # Don't compress FFmpeg (may cause issues)
        'ffprobe',
    ],
    name='Dr-CDJ'
)

app = BUNDLE(
    coll,
    name='Dr-CDJ.app',
    icon='CDJ-Check.icns',
    bundle_identifier='com.dr-cdj.app',
    info_plist={
        'CFBundleShortVersionString': '1.0.1',
        'CFBundleVersion': '1.0.1',
        'CFBundleName': 'Dr. CDJ',
        'CFBundleDisplayName': 'Dr. CDJ',
        'NSHighResolutionCapable': True,
        'LSBackgroundOnly': False,
        'LSUIElement': False,
        'NSRequiresAquaSystemAppearance': False,  # Supporta dark mode
    },
)
