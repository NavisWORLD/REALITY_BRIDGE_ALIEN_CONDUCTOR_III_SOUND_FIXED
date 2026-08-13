# TEACHER MANUAL
## Reality Bridge Alien Conductor III
### Creative Coding · DSP · MIDI · Human-Computer Musical Interaction

## Course purpose

This manual turns the repository into a teachable 10–12 week module. Students do not need to accept artistic framing as scientific fact. The course repeatedly classifies values as **measured, inferred, mapped or synthesized**.

Suggested prerequisites: basic Python or JavaScript; algebra/trigonometry; terminal comfort. C++ units can be optional for introductory classes.

## Learning outcomes

Students should be able to:

1. convert MIDI notes and frequencies;
2. describe browser/native audio signal paths;
3. implement and critique a plucked-string delay model;
4. extract simple audio features and discuss estimator limits;
5. explain why melody does not uniquely identify harmony;
6. design confidence-aware accompaniment;
7. route musical state through MIDI/native rendering;
8. distinguish local from cloud processing;
9. test audio software beyond UI behavior;
10. publish a reproducible creative-technology artifact.

# Suggested 12-week sequence

## Week 1 — Sound is data
Sample rate, amplitude, frequency, MIDI mapping. Lab: use `midi_to_hz`/`hz_to_midi`, build an octave table, explain equal temperament and the A4=440 assumption.

## Week 2 — Web Audio and user activation
AudioContext, gain, analyser, mobile restrictions. Lab: run standalone/PWA, output test, compare localhost with raw preview. Failure exercise: master gain zero while animations continue.

## Week 3 — Physical-model strings
Delay line, feedback, damping, stability, excitation. Build C++ core, render `reality_bridge_demo.wav`, change damping/brightness, identify clamps.

## Week 4 — Acoustic body as approximation
Filters/resonance/model scope. Compare direct string vs body-colored output. Explain why presets such as “dreadnought” are synthesis metaphors, not material-science simulations.

## Week 5 — Audio features
RMS, zero crossing, onset, dynamic range, rough tempo. Run `reality-bridge analyze` on student-created WAVs. Identify direct measurements versus estimates.

## Week 6 — Pitch confidence and Voice DNA
Pitch confidence, noise, room conditions, note classes. Use Live Voice with stable vowels, consonants, breath/noise and glissandi. Document uncertainty. Discuss analysis vs raw mic monitoring.

## Week 7 — Harmony is not recognition
Pitch-class history, keys, chords, ambiguity/confidence. Feed C-E-G and A-C-E patterns; create a melody compatible with multiple harmonies. Never call the hypothesis “the true chord” without ground truth.

## Week 8 — Generative accompaniment
Density, role-based events, deterministic seeds. Extend `plan_bar()` with a new role while preserving low-confidence behavior. More notes do not automatically mean better design.

## Week 9 — MIDI bridge and DAW integration
Note on/off, channels, CC, clock authority, panic. Route to a virtual MIDI port/DAW, map CC20–27, intentionally create/recover from a stuck note with all-notes-off.

## Week 10 — Media/video sonification
Structural features, local decoding, visual mappings, scene changes. Use a silent video and audio file; document at least five mappings and label each as artistic. Use licensed/self-created media for publication.

## Week 11 — Native plugin architecture
Real-time callback rules, C ABI, JUCE, SDK boundaries. All students call the C API; advanced students build JUCE Standalone/VST3/AU with their local JUCE checkout.

## Week 12 — Publication and performance
Present an instrument/integration plus source, version/tag, tested platform, one test/measurement, signal-flow diagram, measured-vs-inferred-vs-mapped list, limitations and license/citation info.

# Lab rubric

## Engineering correctness — 40%
Signal path works; output bounded; state validated; code runs on declared target; failure behavior documented.

## Evidence discipline — 25%
Measurements distinguished from estimates; uncertainty acknowledged; no fake stems/chords/physics; tests match claims.

## Musical design — 20%
Intentional mappings; coherent response; low-confidence behavior remains usable; interaction supports performance rather than decoration only.

## Documentation — 15%
Setup, architecture, integration contract, limitations, licensing.

# Teacher demonstrations

### A running UI can be silent
Mute a bus while transport/visuals remain active, then use the direct output test. Lesson: instrumentation must test the layer you claim.

### One melody, several chords
Play/sing E-G-A-G and collect plausible contexts before running the tracker. Ambiguity is a property of evidence, not a bug to hide.

### Same state, different renderer
Generate Python NoteEvents, render through MIDI then another synth/native host. Musical logic can be portable.

### Physical model vs sample playback
Change modeled-pluck damping and compare to a fixed sample. Discuss strengths and limits.

# Student projects

- adaptive singer accompanist with improved confidence-aware tracking;
- new safe Gravity Guitar body/filter personality;
- silent-video sonification score with published mapping rules;
- DAW bridge with Python MIDI + CC automation;
- game-engine C-ABI instrument in Unity/Unreal/Godot/Rust;
- accessibility-focused alternative controller.

# Common misconceptions

**“The system knows the song.”** It infers evidence; that is not exact composition recognition.

**“Gravity is being measured.”** GRAVITY is an artistic macro unless a documented physical sensor is explicitly integrated.

**“The guitar is a real acoustic simulation.”** It is physical-model-inspired synthesis, not full structural/material simulation.

**“Video color has a natural sound.”** Color-to-sound is a mapping choice.

**“Local-first means every fork is private.”** Downstream network features change the privacy model.

# Classroom safety

- start headphone/device volume low;
- do not encourage high-gain feedback experiments;
- use panic;
- do not require private voice/media uploads;
- use licensed/self-created media for public showcases;
- never distribute signing credentials/API keys in repos.

# Oral exam prompts

1. Why can a correct pitch estimate still lead to a wrong chord?
2. What is the difference between a feature and a mapping?
3. Why is network I/O unsafe in a real-time audio callback?
4. Why do browsers require user activation before audio?
5. How does Karplus–Strong delay length relate to pitch?
6. Why include both MIDI and a C ABI?
7. What must panic clear?
8. What extra evidence would strengthen harmony inference?
9. What privacy change occurs when mic frames are uploaded?
10. Which project names are artistic labels rather than scientific quantities?

# Final teacher checklist

- [ ] Students can build at least one renderer.
- [ ] Students can run tests.
- [ ] Students identify observation/inference/mapping/synthesis layers.
- [ ] Students document confidence and uncertainty.
- [ ] Students use safe listening levels.
- [ ] Public projects include license/citation info.
- [ ] No unlicensed proprietary SDK files are committed.
