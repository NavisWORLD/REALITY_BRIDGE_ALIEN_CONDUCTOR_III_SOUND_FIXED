# Rust integration sheet

## Direct Rust dependency
```toml
[dependencies]
cosmic-conductor = { path = "../COSMIC-CONDUCTOR-ENGINE/rust" }
```

```rust
use cosmic_conductor::{midi_to_hz,ConductorMacros,StringVoice};
let m=ConductorMacros::default();
let mut voice=StringVoice::new(48_000.0);
voice.pluck(midi_to_hz(60.0,440.0),0.8,m.string_damping(),m.brightness(),0.25);
let sample=voice.process();
```

## Native library
`cargo build --release --manifest-path rust/Cargo.toml` builds the Rust library. `rust/include/cosmic_conductor.h` exposes the `cc_*` ABI for Swift, Objective-C, Kotlin/JNI, C#, C/C++, Unity, Unreal and other hosts.

## Existing C++ engine from Rust
The C++ core exports `rb_*` in `cpp/include/reality_bridge/c_api.h`. Rust hosts can declare those functions through `extern "C"` and link the CMake product. The pure Rust crate remains independent by default so normal Cargo tests do not need the C++ linker.

Do not allocate, block, print, open files or call the network inside a realtime audio callback.
