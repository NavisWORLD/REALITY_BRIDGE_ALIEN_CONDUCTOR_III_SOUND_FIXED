#!/usr/bin/env python3
from pathlib import Path
import base64
import gzip

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / 'web' / 'source_archive'
chunks = sorted(ARCHIVE.glob('standalone.gz.b64.*'))
if not chunks:
    raise SystemExit('No standalone source archive chunks found')

payload = ''.join(p.read_text(encoding='utf-8').strip() for p in chunks)
try:
    source = gzip.decompress(base64.b64decode(payload, validate=True)).decode('utf-8')
except Exception as exc:
    raise SystemExit(f'Could not reconstruct standalone HTML: {exc}') from exc

if 'rel="manifest"' not in source:
    source = source.replace('</head>', '<link rel="manifest" href="manifest.webmanifest">\n<link rel="icon" href="icon.svg" type="image/svg+xml">\n</head>', 1)
if 'navigator.serviceWorker.register' not in source:
    source = source.replace('</body>', '<script>if("serviceWorker" in navigator && location.protocol.startsWith("http")){addEventListener("load",()=>navigator.serviceWorker.register("./sw.js").catch(()=>{}));}</script>\n</body>', 1)

out = ROOT / 'REALITY_BRIDGE_ALIEN_CONDUCTOR_III_SOUND_FIXED.html'
out.write_text(source, encoding='utf-8')
print(f'Reconstructed {out} from {len(chunks)} verified archive chunks ({len(source)} chars)')
