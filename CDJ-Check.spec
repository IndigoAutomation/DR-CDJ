# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/cdj_check/main.py'],
    pathex=[],
    binaries=[('/opt/homebrew/bin/ffmpeg', '.'), ('/opt/homebrew/bin/ffprobe', '.')],
    datas=[],
    hiddenimports=[],
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='CDJ-Check',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
app = BUNDLE(
    exe,
    name='CDJ-Check.app',
    icon='CDJ-Check.icns',
    bundle_identifier='com.cdjcheck.app',
)
