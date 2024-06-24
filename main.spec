# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config-template.json', 'config-template.json'),
        ('config.json', 'config.json'),
        ('config.py', 'config.py'),
        ('LICENSE', 'LICENSE'),
        ('README.md', 'README.md'),
        ('requirements.txt', 'requirements.txt'),
        ('requirements-optional.txt', 'requirements-optional.txt'),
        ('pyproject.toml', 'pyproject.toml'),
        ('nixpacks.toml', 'nixpacks.toml'),
        ('run.log', 'run.log'),
        ('start.sh', 'start.sh'),
        ('stop.sh', 'stop.sh'),
        ('tail_log.sh', 'tail_log.sh'),
        ('translate', 'translate'),
        ('voice', 'voice'),
        ('webmain.py', 'webmain.py'),
        ('app.py', 'app.py'),
        ('common', 'common'),
        ('channel', 'channel'),
        ('bridge', 'bridge'),
        ('build', 'build'),
        ('docs', 'docs'),
        ('dsl', 'dsl'),
        ('lib', 'lib'),
        ('plugins', 'plugins'),
        ('scripts', 'scripts'),
    ],
    hiddenimports=['bottle_websocket'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],  # 不需要排除任何 Qt 绑定包
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
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # 确保生成控制台可执行文件，如果需要无控制台则设为 False
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)

app = BUNDLE(
    coll,
    name='main.app',
    icon=None,
    bundle_identifier=None,
)