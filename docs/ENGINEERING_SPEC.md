# Reality Bridge Engineering Specification
## Version 0.1 — 2026-08-12

This document defines the software architecture and integration behavior of the open engine. Normative words **MUST**, **SHOULD** and **MAY** describe interoperability requirements, not scientific claims.

## 1. Design goal

Reality Bridge converts observations from performance/media into musical control:

`observation -> feature state -> uncertain musical inference -> mapping -> renderer`

A renderer may be Web Audio, MIDI, the native C++ engine, a DAW/plugin host or another synthesis environment.

## 2. Architectural layers

### Observation
Inputs MAY include microphone frames, uploaded media, video frames, pointer gestures or MIDI. Hosts SHOULD preserve timestamps and expose confidence for estimates such as pitch or tempo.

### Voice DNA
Canonical fields: `pitch_hz`, `pitch_confidence`, `energy`, `brightness`, `articulation`, `stability`, `onset`, `timestamp`. Raw microphone monitoring MUST NOT be enabled merely because analysis is enabled.

### Media DNA
The model defines energy curve, transients, tempo estimate/confidence, pitch-class evidence, spectral centroid/flux, dynamic range and optional visual motion/luminance/scene-change features. Media DNA is not an audio stem. Integrations MUST NOT relabel spectral bands as vocals/drums/bass unless an actual source-separation model is present.

### Harmonic hypothesis
A harmonic state includes root pitch class, mode, chord root, quality and confidence. Hosts SHOULD leave texture sparse when confidence is weak instead of treating the hypothesis as ground truth.

### Macro state
`ENERGY`, `ENTROPY`, `LIFE`, `MOTION`, `GRAVITY`, `HUMAN_ALIEN` are dimensionless 0..1 musical controls. Suggested semantics: ENERGY=velocity/density/excitation; ENTROPY=mutation/unpredictability; LIFE=motif persistence/humanization/sympathy; MOTION=modulation/arpeggiation/spatial response; GRAVITY=tonic attraction/bass/stability; HUMAN_ALIEN=conventional toward intentionally impossible behavior. These are artistic mappings.

## 3. Timing
Audio renderers SHOULD schedule from their audio clock, not UI frame time. MIDI/network bridges SHOULD timestamp or buffer enough to avoid jitter. A panic operation MUST be available.

## 4. Frequency and note standard
Unless configured otherwise, MIDI note 69 maps to A4=440 Hz: `f = A4 * 2^((midi - 69)/12)`. Microtonal offsets MAY be represented as fractional MIDI, cents or pitch-bend; integrations MUST document which.

## 5. Physical-model string core
The native C++ core implements a Karplus–Strong-inspired feedback-delay string: frequency is Nyquist-safe; force is excitation; damping is bounded feedback; brightness controls the feedback character; pick position shapes excitation. It is a practical musical model, not a finite-element guitar simulation. Output SHOULD pass through bounded gain/limiting.

## 6. C ABI
Header: `cpp/include/reality_bridge/c_api.h`.

Lifecycle: create → pluck → process once/sample → optional stop → destroy. `rb_string_process()` performs no allocation. Hosts SHOULD allocate voices outside the real-time callback.

## 7. Python API
`AccompanimentEngine.observe_voice()` updates rolling evidence. `plan_bar()` emits host-neutral NoteEvents with note, velocity, duration beats, channel and role. The reference planner is intentionally readable and extensible.

## 8. Web application
The root standalone HTML is the self-contained artifact. PWA assets are optional packaging. AudioContext creation/resume must follow user activation; microphone permission is opt-in; local media processing requires no upload backend; master output must be bounded; source/generated mix state must not silently mute the bridge on a fresh session; optional API failure must not destroy the UI.

## 9. MIDI and plugin
MIDI is a transport, not the engine. See `MIDI_PLUGIN_SPEC.md` and `integrations/MIDI_MAP.md`. The JUCE adapter consumes MIDI and renders the native string core; higher-level Voice/Media DNA may connect through MIDI, automation or host adapters. JUCE and platform SDKs are external dependencies.

## 10. Privacy
Core browser operation does not require telemetry or cloud upload. Integrators adding network features MUST document them and SHOULD default to local processing for microphone/media when feasible.

## 11. Compatibility
Web: current standards-based mobile/desktop browsers with graceful feature detection. Python: 3.10+. Native core: C++17 + CMake 3.20+. Plugin adapter: JUCE-compatible platforms/toolchains.

## 12. Versioning
Public protocol structures begin at `v=1`. Breaking semantic changes SHOULD increment version documentation. Imported state MUST validate unknown/out-of-range fields rather than trusting them blindly.
