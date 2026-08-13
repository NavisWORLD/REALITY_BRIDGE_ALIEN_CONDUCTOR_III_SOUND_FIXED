# Reality Bridge Integration Protocol v0.1

The bridge is host-neutral. A host may exchange events as JSON, MIDI, a C ABI call, or direct Python objects. The semantic event model is the same.

```json
{"v":1,"type":"voice_dna","time":12.4,"payload":{"pitch_hz":220.0,"confidence":0.91,"energy":0.62,"brightness":0.44,"articulation":0.35,"stability":0.86}}
```

Core `type` values:

- `voice_dna` — analyzed live performance evidence.
- `media_dna` — summarized local media features.
- `note_on` / `note_off` — musical note events; MIDI note + velocity are canonical.
- `chord_hypothesis` — root/mode/chord plus confidence; never a claim of exact song recognition.
- `macro` — ENERGY, ENTROPY, LIFE, MOTION, GRAVITY, HUMAN_ALIEN in normalized 0..1 ranges.
- `transport` — BPM, play/stop, beat/bar positions.
- `panic` — immediate all-notes-off / voice clear.

A host MUST clamp untrusted numeric input, MUST expose a panic path, SHOULD timestamp events, and MUST NOT interpret an artistic macro as a physical measurement. Audio/media may stay local; transport of actual source media is outside this protocol.
