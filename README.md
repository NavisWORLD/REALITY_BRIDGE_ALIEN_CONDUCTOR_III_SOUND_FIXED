# 🌌 REALITY BRIDGE // COSMIC CONDUCTOR ENGINE

### SING INTO IT. STRUM IT. FEED IT MEDIA. SEND IT MIDI. EMBED THE CORE. TEACH THE MACHINE.

**Cosmic Conductor Engine** is the source-available evolution of Reality Bridge Alien Conductor III: a handheld-first musical engine that turns human gesture, voice, media and control signals into playable musical structure.

```text
VOICE / GUITAR / TOUCH / MIDI / AUDIO / VIDEO
                    │
                    ▼
             OBSERVATION LAYER
       Voice DNA / Media DNA / Gestures
                    │
                    ▼
             MUSICAL INFERENCE
       tempo / pitch / harmony / state
                    │
                    ▼
             CONDUCTOR STATE
 ENERGY · ENTROPY · LIFE · MOTION · GRAVITY · ALIEN
                    │
       ┌────────────┼──────────────┐
       ▼            ▼              ▼
    WEB AUDIO      MIDI        NATIVE DSP
                              ┌────┴────┐
                              ▼         ▼
                            RUST       C++
```

The six named macros are artistic musical controls, not claims that the program measures literal physical gravity, biological life or thermodynamic entropy.

## 🛡️ Rights and provenance first

Copyright © 2026 Cory Shane Davis / NavisWORLD.

**Current rights boundary:** newly authored or materially revised Cory-owned material distributed under the current `LICENSE` on or after **2026-08-16** is governed by the **Cory Davis Audio / Neural Instrument Research Source Rights Reservation v1.0** unless a file expressly states different terms.

Public visibility is not a general reuse license for that covered current material. Commercial products, hosted services, OEM integration, commercial AI/ML development, commercial redistribution, derivative implementations based on protected expression, and other commercial exploitation require separate written authorization where the current `LICENSE` states so.

**Historical boundary:** the published `v0.2.0` generation and repository state through commit `f8337c71f77edc1fe37da0636ca68c4a41abf516` were distributed under Apache-2.0. Valid Apache-2.0 rights for those historical copies remain intact. They are not revoked or rewritten.

See:

- [`LICENSE`](LICENSE) - current prospective rights reservation
- [`LICENSE_HISTORY.md`](LICENSE_HISTORY.md) - exact historical licensing boundary
- [`COMMERCIAL_RIGHTS.md`](COMMERCIAL_RIGHTS.md) - commercial licensing path
- [`CORY_DAVIS_IP_AND_ACCESS_NOTICE.md`](CORY_DAVIS_IP_AND_ACCESS_NOTICE.md) - IP/access notice

Copyright protects original expression, not abstract ideas, systems, algorithms, mathematical principles, or methods by themselves. Third-party code, frameworks, SDKs, JUCE, platform toolchains, samples, models, and other materials remain under their own licenses and terms.

## 📦 Historical v0.2.0 packaged edition

The existing `v0.2.0` GitHub Release remains available as a historical Apache-2.0 release. The current rights boundary does not rewrite those previously granted rights.

Published artifacts include Windows installer/portable builds, macOS app/disk image, Linux bundle, Android APK, iOS Simulator app, PWA package, source archive and SHA-256 manifests.

Physical-device and store distribution may require publisher signing credentials that are intentionally not committed to this repository.

## 🚀 Pick your doorway

### Browser / phone / tablet
Open `REALITY_BRIDGE_ALIEN_CONDUCTOR_III_SOUND_FIXED.html`. For microphone features on mobile, use HTTPS or localhost. The standalone includes Gravity Guitar, live voice companion, Media DNA, generative conductor, touch/orbit performance, recording and Web Audio synthesis.

### Python
```bash
python -m venv .venv
python -m pip install -e './python[test]'
cosmic-conductor demo
```

### Rust
```bash
cargo test --manifest-path rust/Cargo.toml
cargo run --manifest-path rust/Cargo.toml --bin cosmic-conductor -- demo
```

### C++
```bash
cmake -S cpp -B build/cpp -DRB_BUILD_SHARED=ON -DRB_BUILD_TESTS=ON
cmake --build build/cpp --config Release
ctest --test-dir build/cpp -C Release --output-on-failure
```

Use of current covered source outside rights independently provided by law or the applicable current license requires authorization. Historical licensed copies retain their historical permissions.

## 🎛️ What is implemented

| Layer | Status | Purpose |
|---|---|---|
| Handheld Web Instrument | Implemented | Web Audio instrument, voice analysis, Gravity Guitar, Media DNA, conductor and touch UI |
| Python engine | Implemented | musical-state engine, analysis, deterministic accompaniment and CLI |
| Python MIDI bridge | Optional | external MIDI output |
| Python → C++ bridge | Implemented | ctypes wrapper over native ABI |
| Rust DSP/state crate | Implemented | dependency-free native string engine and macro state |
| Rust C ABI | Implemented | host interface for non-Rust runtimes |
| C++ DSP core | Implemented | native physical-model engine and C ABI |
| JUCE adapter | Source target included | VST3/AU/Standalone requires JUCE + platform SDK |
| PWA | Packaged historically | installable web-app bundle in v0.2.0 |
| Android | Packaged historically | APK in v0.2.0 |
| iOS | Built historically | simulator artifact + Capacitor/Xcode project |
| Windows/macOS/Linux | Packaged historically | v0.2.0 multi-platform assets |

## 🔌 Integration docs

- [`docs/INTEGRATION_SHEET.md`](docs/INTEGRATION_SHEET.md)
- [`docs/RUST_INTEGRATION.md`](docs/RUST_INTEGRATION.md)
- [`docs/NATIVE_ABI.md`](docs/NATIVE_ABI.md)
- [`docs/MIDI_PLUGIN_SPEC.md`](docs/MIDI_PLUGIN_SPEC.md)
- [`integrations/BRIDGE_PROTOCOL.md`](integrations/BRIDGE_PROTOCOL.md)
- [`integrations/MIDI_MAP.md`](integrations/MIDI_MAP.md)

Historical documentation may describe the earlier Apache/open-source generation. Rights for the exact copy or revision used are determined by its applicable license and the chronology in `LICENSE_HISTORY.md`.

## 🧪 Verification

Core CI tests Python, Rust, C++, standalone reconstruction and HTML auditing. Cross-platform workflows compile/test the engine family on multiple targets. Claims remain separated into measurement, inference, artistic mapping and experimental interpretation.

## 📦 Repository map

```text
.
├── REALITY_BRIDGE_ALIEN_CONDUCTOR_III_SOUND_FIXED.html
├── python/                 # orchestration, analysis, MIDI, native ctypes
├── rust/                   # DSP/state core + C ABI
├── cpp/                    # native C++ DSP + C ABI
├── bindings/               # cross-language Synaptic Core bindings
├── plugins/juce/           # VST3 / AU / Standalone adapter
├── integrations/           # MIDI, protocol and host examples
├── app/                    # desktop + mobile wrapper
├── packaging/              # packaging assets
├── web/                    # verified standalone source archive
├── docs/                   # book, manuals, specs and guides
├── LICENSE
├── LICENSE_HISTORY.md
└── COMMERCIAL_RIGHTS.md
```

## 🎓 Research and teaching boundary

The project separates implemented signal processing, musical inference, artistic mapping and experimental interpretation. No fake 100% recognition and no requirement to believe the cosmic naming to use the engineering ideas.

Citation does not grant rights beyond the license governing the exact version used. See [`CITATION.cff`](CITATION.cff).

## Contributing

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before submitting anything. The protected current generation does not automatically accept copyrightable outside contributions without an appropriate written rights agreement.

**Welcome to the Cosmic Conductor Engine.**
