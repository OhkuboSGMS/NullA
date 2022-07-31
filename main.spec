# -*- mode: python ; coding: utf-8 -*-
import os
import sys

from PyInstaller.utils.hooks import collect_submodules, collect_data_files
from kivy_deps import sdl2, glew

# コンソールから動作させる場合はローカルのパスが通っていないのでパスを追加
sys.path.append(os.path.abspath(os.curdir))

block_cipher = None
a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[('nulla/res', 'nulla/res'),
                    ('assets', 'assets')],
             hiddenimports=['mediapipe',
                            *collect_submodules('nulla')],
             hookspath=['hooks'],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          icon='assets/icon.ico',
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='nulla')
