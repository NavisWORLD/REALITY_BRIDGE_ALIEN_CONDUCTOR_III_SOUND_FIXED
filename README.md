# REALITY BRIDGE // ALIEN CONDUCTOR III
## SOUND-FIXED // OPEN ENGINE // FULL DISCLOSURE EDITION

> **Sing. Strum. Feed it media. Send it MIDI. Embed the engine. Teach the architecture.**

Reality Bridge Alien Conductor III is an open, handheld-first musical system built around one rule:

**human gesture and media can become musical structure.**

This repository contains the standalone browser instrument, a reusable Python musical-state engine, a native C++ physical-model/DSP core, MIDI integration, a JUCE plugin adapter, cross-platform app packaging scaffolding, tests, a teacher manual, a book, engineering specifications and integration guides.

This project distinguishes **implemented DSP**, **musical inference**, and **artistic naming**. ENERGY / ENTROPY / LIFE / MOTION / GRAVITY are creative musical macros, not established physical constants. A chord inferred from a sung melody is a hypothesis, not proof of the original song's harmony.

## Enter the machine

### Standalone HTML

Open `REALITY_BRIDGE_ALIEN_CONDUCTOR_III_SOUND_FIXED.html`. For microphone features on phones, serve it through HTTPS or localhost rather than a static file preview.

### Desktop launcher

```bash
python app/reality_bridge_app.py
```

### Python engine

```bash
cd python
python -m pip install -e .
reality-bridge demo
reality-bridge analyze path/to/file.wav
reality-bridge serve
```

Optional MIDI:

```bash
python -m pip install -e '.[midi]'
reality-bridge midi
```

### Native C++ DSP

```bash
cmake -S cpp -B build/cpp -DRB_BUILD_SHARED=ON -DRB_BUILD_TESTS=ON
cmake --build build/cpp
ctest --test-dir build/cpp --output-on-failure
./build/cpp/reality_bridge_demo
```

The demo renders `reality_bridge_demo.wav` from the native string/body engine.

## What is actually here

| Layer | Status | What it does |
|---|---|---|
| Handheld Web Instrument | Implemented | Web Audio synthesis, Gravity Guitar, live voice analysis, Media DNA, video sonification, conductor, orbit surface, recording and mobile UI |
| Sound-fixed output path | Implemented | Explicit output unlock/test, safe master route, no persistent source-crossfade silence trap |
| Python musical-state engine | Implemented | Voice DNA, Media DNA model, harmony hypothesis tracker, deterministic accompaniment planner and CLI |
| Python WAV analyzer | Implemented | Dependency-free PCM WAV energy/transient/tempo-oriented analysis |
| MIDI bridge | Implemented with optional deps | Sends accompaniment through `mido` / `python-rtmidi` |
| C++ physical-model core | Implemented | Karplus–Strong-inspired strings, body coloration, bounded soft limiter, frequency helpers and C ABI |
| JUCE plugin adapter | Source included | MIDI-driven VST3/AU/Standalone target; requires JUCE + platform SDK/toolchain |
| PWA | Implemented | Manifest + service worker for installable hosted web app |
| Android/iOS wrapper | Build scaffold included | Capacitor config; native builds require Android Studio/Xcode and signing credentials |
| Perfect source separation | **Not claimed** | Browser build uses spectral/structural analysis, not fake stem labels |
| Exact song/chord recognition | **Not claimed** | Harmony is inferred probabilistically from available evidence |

## Five musical universes

- **CONDUCTOR** — stateful generative accompaniment with transport, harmony and phrase memory.
- **GRAVITY GUITAR** — generated acoustic-string behavior, alternate tunings, impossible voicings, body percussion and touch control.
- **LIVE VOICE // CO-MUSICIAN** — microphone analysis without automatic raw-mic monitoring; pitch confidence, energy, brightness, articulation, stability and phrase timing drive accompaniment.
- **MEDIA TRANSMUTER** — local audio/video becomes structured Audio DNA / Visual DNA before being remapped into new synthesis.
- **ORBIT / VOID** — multidimensional touch performance and coordinated DSP/composition macros.

## Open engine stack

```text
human voice / guitar / touch / MIDI / audio / video
                     │
                     ▼
             observation layer
       Voice DNA / Media DNA / gestures
                     │
                     ▼
              musical inference
      key + chord hypothesis / tempo / state
                     │
                     ▼
             accompaniment plan
        notes / roles / macros / transport
            ┌────────┼───────────┐
            ▼        ▼           ▼
        Web Audio   MIDI      Native C++ DSP
            │        │           │
            └────────┴───────────┘
                     ▼
                   sound
```

A host does not have to use every layer. A DAW can use the MIDI bridge only. A game can call the C ABI. A research notebook can use the Python state engine. A classroom can work entirely in the standalone HTML.

## Integrate it

Start with [`docs/INTEGRATION_SHEET.md`](docs/INTEGRATION_SHEET.md).

Python:

```python
from reality_bridge import AccompanimentEngine, VoiceDNA
engine = AccompanimentEngine(seed=667)
engine.observe_voice(VoiceDNA(
    pitch_hz=220.0, pitch_confidence=0.91, energy=0.62,
    brightness=0.44, articulation=0.35, stability=0.86,
    onset=True, timestamp=0.0,
))
for event in engine.plan_bar():
    print(event)
```

C ABI:

```c
#include <reality_bridge/c_api.h>
rb_string* s = rb_string_create(48000.0);
rb_string_pluck(s, 110.0, 0.8, 0.994, 0.7, 0.2);
float sample = rb_string_process(s);
rb_string_destroy(s);
```

MIDI: use [`integrations/MIDI_MAP.md`](integrations/MIDI_MAP.md). JSON/host integration: use [`integrations/BRIDGE_PROTOCOL.md`](integrations/BRIDGE_PROTOCOL.md).

## App distribution

- **PWA:** deploy the repository root over HTTPS and install from the browser where supported.
- **Desktop:** `python app/reality_bridge_app.py` serves the instrument on localhost.
- **Android/iOS:** run `python app/prepare_mobile.py`, then build the Capacitor wrapper with Android Studio/Xcode and your own signing identity.

The repository does not include Apple/Google signing credentials and does not claim unsigned source is a store-ready binary.

## Plugin / DAW route

`plugins/juce/` contains a source-level JUCE adapter. MIDI Note On excites the native modeled-string core. Parameters cover damping, brightness, pick position, body, resonance and output. Requested formats are VST3, AU and Standalone. JUCE is intentionally not vendored.

## Documentation constellation

- [`docs/BOOK.md`](docs/BOOK.md) — project book.
- [`docs/TEACHER_MANUAL.md`](docs/TEACHER_MANUAL.md) — 12-week course, labs and assessment.
- [`docs/ENGINEERING_SPEC.md`](docs/ENGINEERING_SPEC.md) — architecture and interface specification.
- [`docs/MIDI_PLUGIN_SPEC.md`](docs/MIDI_PLUGIN_SPEC.md) — MIDI/plugin/DAW behavior.
- [`docs/INTEGRATION_SHEET.md`](docs/INTEGRATION_SHEET.md) — integration recipes.
- [`docs/TESTING_AND_VALIDATION.md`](docs/TESTING_AND_VALIDATION.md) — reproducible checks.
- [`docs/PRIVACY_AUDIO_SAFETY.md`](docs/PRIVACY_AUDIO_SAFETY.md) — microphone/media/privacy and safe audio rules.
- [`docs/PUBLISHING_GUIDE.md`](docs/PUBLISHING_GUIDE.md) — releases and citation/DOI workflow.

## Teach it

The core educational sequence is **measurement → inference → mapping → synthesis**:

1. map MIDI notes to frequency;
2. generate a plucked string;
3. measure and bound output;
4. extract energy/onset evidence;
5. infer multiple plausible harmonies from melody;
6. schedule accompaniment;
7. route the same state to Web Audio, MIDI and native DSP;
8. document what is measured versus creatively mapped.

## Tests

```bash
cd python && python -m pip install -e '.[test]' && pytest -q
cd ..
cmake -S cpp -B build/cpp -DRB_BUILD_SHARED=ON -DRB_BUILD_TESTS=ON
cmake --build build/cpp
ctest --test-dir build/cpp --output-on-failure
python tools/reconstruct_standalone.py
node tools/audit_html.mjs
```

CI runs Python, C++ and HTML checks on pushes and pull requests.

## Scientific / engineering honesty

**Reality Bridge**, **Genesis**, **Gravity**, **Void**, **God Mode**, **Divine Light**, and related names are interface/performance language. They do not establish new laws of physics. The repository treats microphone/media features as signal processing and musical mapping. Confidence values are exposed where inference is uncertain.

## Privacy and safety

- Browser media analysis is local unless a host application explicitly adds a network route.
- Raw microphone monitoring is not automatically enabled.
- The master path is conservative and includes dynamics control/panic behavior.
- Use headphones at safe listening levels, especially during development.

## Citation, DOI and license

See `CITATION.cff` for current citation metadata. A DOI is deliberately **not invented**. If you archive a tagged release with Zenodo or another DOI provider, update `CITATION.cff` with the assigned DOI.

Licensed under **Apache License 2.0**. See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).

---

## COSMIC README ATTITUDE

This repository is not asking you to believe the names.

It is asking you to **measure the signal, inspect the state, read the source, rebuild the engine, change the mapping, and make your own instrument.**

Fork the universe responsibly.
