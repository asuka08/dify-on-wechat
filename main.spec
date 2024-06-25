# -*- mode: python ; coding: utf-8 -*-
import site
import importlib.util
import os

block_cipher = None

# 动态获取ntwork包的路径
ntwork_spec = importlib.util.find_spec('ntwork')
ntwork_path = os.path.dirname(ntwork_spec.origin)
helper_file_path = os.path.join(ntwork_path, 'wc', 'helper_4.0.8.6027.dat')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        (helper_file_path, 'ntwork/wc/'),
        ('plugins', 'plugins'),  # 包含 plugins 目录
        ('favicon.ico', '.'),
        ('config.json', 'config.json')
    ],
    hiddenimports=['bottle_websocket'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pyinstaller'],
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
    name='客服助手',  # 指定生成的可执行文件名称
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 如果需要无控制台的 exe，则设为 False
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='favicon.ico',  # 指定图标文件的路径
    onefile=True,  # 将所有内容打包成一个 exe 文件
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
