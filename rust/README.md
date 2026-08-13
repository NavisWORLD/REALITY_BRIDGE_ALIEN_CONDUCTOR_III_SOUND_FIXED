# Cosmic Conductor Engine — Rust

The Rust crate is a dependency-free core for users who want the Reality Bridge musical model without Python or browser runtime dependencies.

## Quick start

```bash
cd rust
cargo test
cargo run --bin cosmic-conductor -- demo
cargo run --bin cosmic-conductor -- render cosmic.wav
```

```rust
use cosmic_conductor::{midi_to_hz, ConductorMacros, StringVoice};
let macros = ConductorMacros::default();
let mut voice = StringVoice::new(48_000.0);
voice.pluck(midi_to_hz(60.0,440.0),0.8,macros.string_damping(),macros.brightness(),0.25);
let sample = voice.process();
```

`cargo build --release` produces an rlib plus native cdylib/staticlib where the target supports them. The exported `cc_*` C ABI lets Swift, Objective-C, Kotlin/JNI, C#, C/C++, game engines and other hosts call the Rust core.

The repository also keeps `cpp/` as the original native DSP path. The two native implementations share musical concepts and bounded-output rules but are not claimed to be bit-identical.
