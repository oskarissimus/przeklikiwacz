# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['przeklikiwacz1.0.py'],
             pathex=['C:\\Users\\oskar.korczak\\Desktop\\2019_wrzesien\\keep_connected'],
             binaries=[('chromedriver.exe', '.')],
             datas=[('.\\sites_targets.csv', '.')],
             hiddenimports=[],
             hookspath=[],
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
          name='przeklikiwacz1.0',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
		  icon='PSD2.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='przeklikiwacz1.0')
