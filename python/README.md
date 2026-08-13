# Reality Bridge // Cosmic Conductor Engine — Python

The Python layer is for orchestration, analysis, musical-state planning, automation, MIDI, teaching and host integration.

```bash
python -m pip install -e './python[test]'
cosmic-conductor demo
```

Optional MIDI: `python -m pip install -e './python[midi]'`.

The historical `reality-bridge` CLI remains available for compatibility.

Native C++ DSP can be loaded with `from reality_bridge.native import NativeString`. See `INSTALL.md` and `examples/`.
