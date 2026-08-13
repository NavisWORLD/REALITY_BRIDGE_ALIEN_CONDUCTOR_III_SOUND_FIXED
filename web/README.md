# Web source lineage

The canonical sound-fixed handheld instrument is generated from the verified gzip/base64 archive under `web/source_archive/`.

Why archive chunks? The standalone is intentionally one large self-contained HTML instrument. Keeping deterministic archive chunks makes connector-safe publication and integrity reconstruction possible without minifying or manually retyping the original source.

Rebuild it with:

```bash
python tools/reconstruct_standalone.py
node tools/audit_html.mjs
```

CI performs the same reconstruction and audit. The `Rebuild Standalone HTML` GitHub Action writes the generated root `REALITY_BRIDGE_ALIEN_CONDUCTOR_III_SOUND_FIXED.html` back to `main` after source-archive changes.
