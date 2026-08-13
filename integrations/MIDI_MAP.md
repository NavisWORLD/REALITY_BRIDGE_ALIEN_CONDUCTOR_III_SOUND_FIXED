# MIDI Bridge Map

Reality Bridge can control a DAW or external synth without requiring a proprietary plugin.

## Notes

- MIDI note numbers are 0–127, velocity 1–127; Note Off or Note On velocity 0 releases.
- Channel 1: pads/harmony
- Channel 2: bass
- Channel 3: Gravity Guitar
- Channel 10: percussion by convention

## Suggested CC map

| CC | Reality Bridge macro | Range |
|---:|---|---|
| 20 | ENERGY | 0–127 |
| 21 | ENTROPY | 0–127 |
| 22 | LIFE | 0–127 |
| 23 | MOTION | 0–127 |
| 24 | GRAVITY | 0–127 |
| 25 | HUMAN ↔ ALIEN | 0–127 |
| 26 | SOURCE PRESERVATION | 0–127 |
| 27 | SYMPATHY | 0–127 |

Pitch bend is reserved for continuous bends/glissandi. Sustain CC64 may hold generated harmony. CC123 must be treated as All Notes Off.

Python: `pip install -e './python[midi]'` then `reality-bridge midi`.
