# Platform matrix

Reality Bridge // Cosmic Conductor Engine is distributed as multiple host layers rather than pretending one binary is correct for every device.

| Platform | Web/PWA | Python | Rust | C++ | Native app path | Plugin path |
|---|---:|---:|---:|---:|---|---|
| Windows 10/11 | Yes | Yes | Yes | Yes | Python launcher / JUCE Standalone | VST3 |
| macOS | Yes | Yes | Yes | Yes | Python launcher / JUCE Standalone | AU / VST3 |
| Linux | Yes | Yes | Yes | Yes | Python launcher / JUCE Standalone | VST3 where supported |
| iPhone/iPad | Yes | N/A primary | Library target | Library target | PWA / Capacitor + Xcode | host dependent |
| Android | Yes | N/A primary | Library target | Library target | PWA / Capacitor + Android Studio | host dependent |
| ChromeOS | Yes | optional | optional | optional | PWA | host dependent |
| ARM Linux / Raspberry Pi | Yes | Yes | Yes | Yes | PWA / Python / native host | host dependent |

## What ready means

- Web/PWA: directly runnable source in a modern browser; microphone access normally requires HTTPS or localhost.
- Python: installable package/CLI with optional MIDI and ctypes access to C++.
- Rust: dependency-free crate, CLI, rlib, cdylib and staticlib outputs.
- C++: CMake library, C ABI, demo renderer and tests.
- JUCE: source target for VST3/AU/Standalone; JUCE and platform SDKs remain external.
- iOS/Android: PWA is the immediate route; Capacitor is the native-wrapper route and requires platform SDKs/signing.

The Cross-platform engine workflow compiles/tests Python, Rust and C++ on Ubuntu, macOS and Windows. Device-specific acceptance still belongs on real hardware.
