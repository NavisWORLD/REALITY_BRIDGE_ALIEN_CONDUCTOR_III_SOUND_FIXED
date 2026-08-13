#!/usr/bin/env python3
from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
dst=root/'app'/'capacitor'/'www'
if dst.exists(): shutil.rmtree(dst)
dst.mkdir(parents=True)
for name in ['index.html','REALITY_BRIDGE_ALIEN_CONDUCTOR_III_SOUND_FIXED.html','manifest.webmanifest','sw.js','icon.svg']:
    shutil.copy2(root/name,dst/name)
print('Prepared',dst)
