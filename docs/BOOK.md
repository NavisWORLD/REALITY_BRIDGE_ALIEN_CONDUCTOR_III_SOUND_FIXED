# THE REALITY BRIDGE HANDBOOK
## Alien Conductor III — Sound, Signal, Gesture and the Handheld Instrument
### Open edition · 2026

This book explains the project as an engineering and creative-computing system. It is not a claim of new physics. Its purpose is to make the architecture understandable enough that another musician, student or engineer can rebuild, critique or extend it.

# Chapter 1 — The instrument that listens

A conventional instrument starts with a control the builder already understands. Reality Bridge begins one step earlier. It accepts uncertain evidence from a human or media source and asks: **what musical behavior can be derived from this evidence without pretending certainty we do not have?**

That creates four layers:

1. **measurement** — energy, pitch estimate, brightness, motion, timing;
2. **inference** — phrase boundary, tempo, plausible key/chord context;
3. **mapping** — energy becomes excitation, motion becomes rhythm, gravity becomes harmonic stability;
4. **synthesis** — Web Audio, MIDI or native DSP turns the plan into sound.

Keeping these layers separate makes the system debuggable. If a wrong chord plays, ask whether pitch tracking failed, harmonic inference failed, a mapping was too aggressive, or the renderer played the wrong note. A beautiful interface is not allowed to erase that distinction.

A phone is unusually capable as an instrument: touch, microphone, local file decoding, graphics, real-time audio and storage coexist in one object. Mobile browsers also protect users from unsolicited audio/microphone access, so the performer must explicitly **AWAKEN** the audio system.

# Chapter 2 — Notes, frequencies and musical state

The bridge uses MIDI note number as a language-neutral pitch coordinate. With A4=440 Hz:

`frequency = 440 * 2^((midi - 69)/12)`

`midi = 69 + 12*log2(frequency/440)`

Fractional MIDI can represent microtonal pitch; hosts may instead use cents or pitch bend if conversion is documented.

Random notes from a scale are not musical continuity. The conductor stores recent melody evidence, harmonic hypothesis, macro state and seed. Deterministic seeds aid repeatability. A Python `NoteEvent` carries note, velocity, beat duration, channel and semantic role without caring which renderer produces sound. **Musical decisions are separated from the renderer.**

# Chapter 3 — Voice DNA

A sung note is not a clean MIDI event. The microphone sees room reflections, breath, consonants, noise and sometimes multiple sources. The system therefore works with estimates: pitch, pitch confidence, energy, brightness, articulation, stability, onset and timestamp.

Confidence is central. A held E can plausibly participate in many harmonic contexts. The conductor accumulates observations and scores alternatives.

## Leave space when uncertain
A poor accompanist confidently plays the wrong harmony. A better one leaves room. The reference planner thins the arrangement when harmonic confidence is weak. This is a general inference principle: reduce commitment when evidence is weak instead of producing more output to hide uncertainty.

# Chapter 4 — Harmony as hypothesis

The Python `HarmonyTracker` keeps a decaying twelve-bin pitch-class vector. Confident notes add evidence; older evidence fades. For each root it scores major/minor scale membership, tonic/fifth evidence and outside notes, then scores diatonic chords inside the best key context. The output is deliberately a `HarmonicHypothesis` with confidence, not “the chord.”

The algorithm is readable by design. A production system could substitute a Bayesian model, HMM, neural estimator or DAW harmonic engine without replacing the rest of the architecture.

The browser also uses recent voicings to reduce arbitrary register jumps. Smooth voice-leading often matters more than exotic chord vocabulary.

# Chapter 5 — Gravity Guitar

Gravity Guitar uses physical-model synthesis rather than prerecorded guitar samples.

## Karplus–Strong in practical terms
A short delay line is filled with a pluck-like excitation. Output is fed back through damping/filtering. Delay length establishes approximate pitch; feedback/filtering controls decay and brightness.

The native C++ path:

1. clamps frequency safely;
2. derives delay length from sample rate/frequency;
3. excites the buffer with deterministic noise;
4. uses pick position to shape excitation;
5. creates decay through filtered feedback;
6. adds lightweight stereo body coloration;
7. bounds output with a soft limiter.

This is not a perfect steel/nylon/spruce/material simulation. Interface labels are synthesis personalities mapped to audible DSP.

A digital instrument need not inherit every six-string/one-hand limitation. Alien/impossible modes can use microtonal offsets, wide voicings and unusual resonant relationships while still remaining intentional rather than random.

# Chapter 6 — Media DNA

Media transformation becomes more interesting when the source becomes structured evidence first.

Audio DNA may include RMS/energy, transients, zero-crossing behavior, spectral centroid/flux, pitch-class evidence, tempo confidence, section evidence and dynamic range. The dependency-free Python analyzer implements a readable subset; the browser carries richer analysis.

Visual DNA allows silent video to become control: downsampled luminance, contrast, edge activity, motion and scene changes. Brightness does not physically equal filter cutoff; that is an explicit mapping choice.

Transformation modes can retain different amounts of structure: Ghost, Skeleton, Reincarnate, Guitar Possession, Orchestral Possession, Void and Mirror. The point is to expose the transformation pipeline, not hide copying behind effects.

# Chapter 7 — The five macros

ENERGY, ENTROPY, LIFE, MOTION and GRAVITY are dramatic interface vocabulary, not universal constants. They have explicit musical consequences: excitation/density; mutation/irregularity; persistence/humanization; modulation/activity; tonal attraction/bass weight. Because mapping is explicit, builders can replace it rather than hiding ordinary DSP behind scientific-sounding language.

# Chapter 8 — Three renderers, one musical brain

## Web Audio
The handheld app owns immediate interaction, microphone/media analysis, visuals and synthesis.

## MIDI
MIDI lets Reality Bridge drive an existing DAW/hardware instrument. High-level state becomes notes, velocity, channels and CC.

## Native C++
The C++ DSP core serves hosts where browser audio is inappropriate. The C ABI enables FFI from many languages. JUCE demonstrates conversion of the modeled string core into a plugin instrument.

This architecture prevents one UI from becoming a prison.

# Chapter 9 — Real-time engineering

Native audio callbacks must not parse large JSON, perform network requests, allocate large objects or block on UI locks. Inference occurs elsewhere; the audio thread consumes small bounded state.

A browser can report an AudioContext while the device still is not audibly routed. Reality Bridge includes a direct output test because UI state is not sufficient evidence of sound.

Safe experimentation requires conservative gain, bounded feedback, finite-number validation, frequency clamps, envelope smoothing, limiting/compression where appropriate, and panic/all-notes-off. The goal is not maximum loudness; it is survivable experimentation.

# Chapter 10 — Building on real devices

## PWA
Deploy the repository root over HTTPS. Manifest/service worker support home-screen installation where the platform permits it.

## Desktop launcher
`python app/reality_bridge_app.py` starts localhost and opens the browser, avoiding many `file://` restrictions while remaining local.

## Native shells
Capacitor wraps the web UI for Android/iOS. Store builds still require platform SDKs and the publisher's signing credentials. A repository cannot magically create a signed App Store binary without a publisher identity.

# Chapter 11 — Plugin integration

The JUCE adapter intentionally stays small. MIDI Note On excites one of sixteen modeled-string voices, then body coloration and limiting feed the host. Parameters are automatable.

The whole browser app is not embedded in the plugin because plugin hosts have different real-time, UI and sandbox constraints. Instead use MIDI/CC, host automation, a custom semantic protocol adapter, or a future native in-process inference layer.

# Chapter 12 — Teaching, publishing and falsifiability

The strongest educational value is the demand that every impressive claim be translated into an observable mechanism.

Ask:
- Where did this number come from?
- Is it measured, inferred or mapped?
- What happens if confidence is low?
- Can the same state drive a different renderer?
- What is the failure mode?
- Is output bounded?
- Can someone reproduce the test?

For publication, release exact source, version it, run tests, describe the target hardware/browser/toolchain and archive the release. If a service such as Zenodo issues a DOI, add the **real DOI after issuance**. Never manufacture citation metadata to make work look more established.

# Appendix A — Build recipes

### Python
```bash
cd python
python -m pip install -e '.[test]'
pytest -q
reality-bridge demo
```

### C++
```bash
cmake -S cpp -B build/cpp
cmake --build build/cpp
ctest --test-dir build/cpp --output-on-failure
```

### JUCE
```bash
cmake -S plugins/juce -B build/plugin -DJUCE_DIR=/path/to/JUCE
cmake --build build/plugin --config Release
```

### Mobile wrapper
```bash
python app/prepare_mobile.py
cd app/capacitor
npm install
npx cap add android
# or: npx cap add ios
npx cap sync
```

# Appendix B — The cosmic engineering oath

Create beyond the obvious interface.

Measure before naming.

Report uncertainty instead of hiding it.

Keep the signal path inspectable.

Protect the listener from runaway gain.

Keep the raw source private unless the user chooses otherwise.

Build interfaces that invite play, but code that survives inspection.

**BE UNHINGED WITH CREATION. BE PRECISE WITH DSP.**
