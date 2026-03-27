# -*- mode: python ; coding: utf-8 -*-

hiddenimports = [
    "matplotlib.backends.backend_tkagg",
    "matplotlib.backends.backend_agg",
]

excludes = [
    "matplotlib.backends.backend_qt5agg",
    "matplotlib.backends.backend_qt5",
    "matplotlib.backends.backend_wxagg",
    "matplotlib.backends.backend_gtk3agg",
    "matplotlib.backends.backend_gtk3",
    "matplotlib.backends.backend_cairo",
    "matplotlib.backends.backend_webagg",
]

a = Analysis(
    ['glyphloom/cli/main.py'],
    pathex=[],
    binaries=[],
    datas=[('glyphloom/data', 'glyphloom/data')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='glyphloom',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)