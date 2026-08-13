# 🌌 REALITY BRIDGE // COSMIC CONDUCTOR ENGINE

### SING INTO IT. STRUM IT. FEED IT MEDIA. SEND IT MIDI. EMBED THE CORE. TEACH THE MACHINE.

**Cosmic Conductor Engine** is the open-source evolution of Reality Bridge Alien Conductor III: a handheld-first musical engine that turns human gesture, voice, media and control signals into playable musical structure.

This is no longer one giant webpage pretending to be an SDK. It is a multi-runtime music-engine stack:

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

## 📦 Download v0.2.0 — packaged edition

**GitHub Release:** https://github.com/NavisWORLD/REALITY_BRIDGE_ALIEN_CONDUCTOR_III_SOUND_FIXED/releases/tag/v0.2.0

| End-user target | Status | Published artifact |
|---|---|---|
| Windows one-click installer | ✅ | `Cosmic-Conductor-Engine-Setup-v0.2.0.exe` |
| Windows portable app | ✅ | `Cosmic-Conductor-Portable-v0.2.0.exe` |
| macOS app | ✅ | `Cosmic-Conductor-macOS-v0.2.0.app.zip` |
| macOS disk image | ✅ | `Cosmic-Conductor-Engine-v0.2.0.dmg` |
| Linux x86_64 bundle | ✅ | `Cosmic-Conductor-Linux-x86_64-v0.2.0.tar.gz` |
| Android application | ✅ | `Cosmic-Conductor-Android-v0.2.0.apk` |
| iPhone/iPad native app build | ✅ | `Cosmic-Conductor-iOS-Simulator-v0.2.0.app.zip` + Capacitor/Xcode device project |
| iPhone/iPad no-signing install path | ✅ | installable HTTPS PWA package |
| Web/PWA package | ✅ | `Cosmic-Conductor-Web-PWA-v0.2.0.zip` |
| Full source package | ✅ | `Cosmic-Conductor-Engine-Source-v0.2.0.zip` |
| GitHub Release with binaries | ✅ | release `v0.2.0` + `SHA256SUMS.txt` |

The native iOS project is real and the CI-built Simulator `.app` is published. Installing a native app on a physical iPhone or shipping through the App Store additionally requires the publisher's Apple Developer signing certificate/provisioning profile; those private credentials are deliberately not committed to this public repository. The PWA is the zero-signing iPhone/iPad install route. The macOS build is ad-hoc signed but not Apple-notarized; notarization likewise requires the publisher's Apple Developer identity.

See [`docs/INSTALLERS_AND_RELEASES.md`](docs/INSTALLERS_AND_RELEASES.md) for packaging and signing details.

## 🚀 Pick your doorway

### Browser / phone / tablet
Open `REALITY_BRIDGE_ALIEN_CONDUCTOR_III_SOUND_FIXED.html`. For microphone features on mobile, use HTTPS or localhost. The standalone remains the complete interactive instrument: Gravity Guitar, live voice companion, Media DNA, generative conductor, touch/orbit performance, recording and Web Audio synthesis.

### Python
```bash
python -m venv .venv
python -m pip install -e './python[test]'
cosmic-conductor demo
```
Optional MIDI: `python -m pip install -e './python[midi]'`.

The legacy `reality-bridge` command remains for compatibility. Python also includes `reality_bridge.native.NativeString`, a ctypes bridge into the C++ `rb_*` DSP ABI. Start with [`python/INSTALL.md`](python/INSTALL.md).

### Rust 🦀
```bash
cargo test --manifest-path rust/Cargo.toml
cargo run --manifest-path rust/Cargo.toml --bin cosmic-conductor -- demo
cargo run --manifest-path rust/Cargo.toml --bin cosmic-conductor -- render cosmic.wav
```

```rust
use cosmic_conductor::{midi_to_hz,ConductorMacros,StringVoice};
let m=ConductorMacros::default();
let mut voice=StringVoice::new(48_000.0);
voice.pluck(midi_to_hz(60.0,440.0),0.8,m.string_damping(),m.brightness(),0.25);
let sample=voice.process();
```

The dependency-free Rust crate builds as an `rlib`, `cdylib`, `staticlib`, and CLI WAV renderer. Its `cc_*` C ABI lets Swift, Objective-C, Kotlin/JNI, C/C++, C#, game engines and other hosts call the engine. Start with [`rust/README.md`](rust/README.md).

### C++
```bash
cmake -S cpp -B build/cpp -DRB_BUILD_SHARED=ON -DRB_BUILD_TESTS=ON
cmake --build build/cpp --config Release
ctest --test-dir build/cpp -C Release --output-on-failure
```
The C++ engine keeps the original physical-model DSP, bounded limiter, frequency helpers, tests, demo renderer and stable `rb_*` C ABI. Start with [`cpp/README.md`](cpp/README.md).

## 🎛️ What is actually implemented

| Layer | Status | Purpose |
|---|---|---|
| Handheld Web Instrument | ✅ Implemented | Web Audio instrument, voice analysis, Gravity Guitar, Media DNA, conductor and touch UI |
| Python engine | ✅ Implemented | musical-state engine, analysis, deterministic accompaniment and CLI |
| Python MIDI bridge | ✅ Optional dependency | external MIDI output |
| Python → C++ bridge | ✅ Implemented | ctypes wrapper over `rb_*` |
| Rust DSP/state crate | ✅ Implemented | dependency-free native string engine and macro state |
| Rust C ABI | ✅ Implemented | `cc_*` interface for non-Rust hosts |
| C++ DSP core | ✅ Implemented | native physical-model engine and C ABI |
| JUCE adapter | 🧩 Source target included | VST3/AU/Standalone requires JUCE + platform SDK |
| PWA | ✅ Packaged | installable web-app bundle published in v0.2.0 |
| Android application | ✅ Packaged | installable APK published in v0.2.0 |
| iOS application | ✅ Built | Capacitor/Xcode app + CI-built Simulator `.app`; device/App Store signing needs publisher credentials |
| Windows installer | ✅ Packaged | Inno Setup one-click `.exe` published in v0.2.0 |
| macOS application | ✅ Packaged | `.app.zip` and `.dmg` published in v0.2.0 |
| Binary GitHub Release | ✅ Published | multi-platform v0.2.0 assets + SHA-256 manifest |
| Perfect source separation | ❌ Not claimed | structural analysis is not fake stem extraction |
| Exact song recognition | ❌ Not claimed | harmony/pitch interpretation remains inference |

## 🖥️ Platform family

- Windows — packaged installer/portable app + Python + Rust + C++ + PWA + JUCE/VST3 path
- macOS — packaged `.app`/`.dmg` + Python + Rust + C++ + PWA + JUCE AU/VST3 path
- Linux — packaged x86_64 bundle + Python/Rust/C++/PWA
- iPhone/iPad — Capacitor/Xcode app, Simulator artifact and PWA; physical native distribution requires Apple signing
- Android — packaged installable APK + Capacitor + Rust/C++ JNI/NDK path
- ARM Linux/Raspberry Pi — Python/Rust/C++/PWA where the platform toolchain supports them
- DAWs — MIDI bridge or JUCE adapter
- game/research engines — C ABI, Python, or Rust library

See [`docs/PLATFORM_MATRIX.md`](docs/PLATFORM_MATRIX.md) and [`docs/DEVICE_BUILD_GUIDE.md`](docs/DEVICE_BUILD_GUIDE.md).

## ⚡ Build the stack
macOS/Linux: `./scripts/bootstrap.sh`

Windows PowerShell: `.\scripts\bootstrap.ps1`

Manual checks are in [`docs/BUILD_ALL.md`](docs/BUILD_ALL.md).

## 🔌 Integration docs
- [`docs/INTEGRATION_SHEET.md`](docs/INTEGRATION_SHEET.md)
- [`docs/RUST_INTEGRATION.md`](docs/RUST_INTEGRATION.md)
- [`docs/NATIVE_ABI.md`](docs/NATIVE_ABI.md)
- [`docs/MIDI_PLUGIN_SPEC.md`](docs/MIDI_PLUGIN_SPEC.md)
- [`integrations/BRIDGE_PROTOCOL.md`](integrations/BRIDGE_PROTOCOL.md)
- [`integrations/MIDI_MAP.md`](integrations/MIDI_MAP.md)

## 🧠 Teaching/publication
Included: project book, teacher manual, engineering spec, build guide, testing/validation, privacy/audio safety, publishing guide and release-validation record.

The teaching rule is:

```text
MEASUREMENT → INFERENCE → MAPPING → SYNTHESIS
```

## 🧪 Verification
Core CI tests Python, Rust, C++, standalone reconstruction and HTML auditing. Cross-platform GitHub Actions compile/test the native engine family on Ubuntu, macOS and Windows, and target-check Rust for Android ARM64, iOS ARM64, WebAssembly and ARM Linux. The v0.2.0 packaging workflow has successfully built Windows, macOS, Linux, Android, Web/PWA and iOS Simulator artifacts; the published release collects the verified results with cryptographic SHA-256 digests. Real microphones, audio interfaces, DAWs, notarization and store-signing configurations still require target-device/publisher acceptance tests.

## 📦 Repository map
```text
.
├── REALITY_BRIDGE_ALIEN_CONDUCTOR_III_SOUND_FIXED.html
├── python/                 # orchestration, analysis, MIDI, native ctypes
├── rust/                   # safe dependency-free DSP/state core + C ABI
├── cpp/                    # native C++ DSP + C ABI
├── plugins/juce/           # VST3 / AU / Standalone adapter
├── integrations/           # MIDI, protocol and host examples
├── app/                    # frozen desktop launcher + Capacitor mobile wrapper
├── packaging/              # Windows installer and packaging assets
├── web/                    # verified standalone source archive
├── docs/                   # book, teacher manual, specs and guides
├── scripts/                # Windows/macOS/Linux bootstrap
└── .github/workflows/      # CI, device checks, packaging and release publication
```

## 🛡️ License and engineering honesty
Code is Apache-2.0 unless a file states otherwise. The project separates implemented signal processing, musical inference, artistic mapping and experimental interpretation. No fake 100% recognition and no requirement to believe the cosmic naming to use the software.

A singer should be able to make a machine accompany them. A Python developer should be able to import it. A Rust developer should be able to own the audio loop. A C++ developer should be able to embed the DSP. A DAW should be able to receive MIDI or load the plugin build. A phone should be able to run the instrument. A teacher should be able to explain every layer.

**Welcome to the Cosmic Conductor Engine.**
