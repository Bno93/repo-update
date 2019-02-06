# -*- mode: python -*-

block_cipher = None


a = Analysis(['vcs_lite.py'],
             pathex=['F:\\workspace\\private\\repo-update\\update_repo'],
             binaries=[],
             datas=[('res/icon/*', 'res/icon')],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='vcs-lite',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False , icon='res\\icon\\app.ico')
