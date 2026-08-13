# Device build guide

## Web / PWA
Serve the repository root over HTTPS or localhost and open `index.html`. The canonical standalone is `REALITY_BRIDGE_ALIEN_CONDUCTOR_III_SOUND_FIXED.html`.

## Windows
```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e ".\python[test,midi]"
cosmic-conductor demo
cargo test --manifest-path rust\Cargo.toml
cmake -S cpp -B build\cpp -DRB_BUILD_SHARED=ON -DRB_BUILD_TESTS=ON
cmake --build build\cpp --config Release
ctest --test-dir build\cpp -C Release --output-on-failure
```

## macOS / Linux
```bash
python3 -m pip install -e './python[test,midi]'
cargo test --manifest-path rust/Cargo.toml
cmake -S cpp -B build/cpp -DRB_BUILD_SHARED=ON -DRB_BUILD_TESTS=ON
cmake --build build/cpp --config Release
ctest --test-dir build/cpp -C Release --output-on-failure
```

## iOS / iPadOS
Use the PWA, the existing Capacitor wrapper with Xcode, or compile the Rust/C++ native core for an Apple target and call its C ABI from Swift/Objective-C. App Store distribution requires the publisher's signing identity.

## Android
Use the PWA, Capacitor + Android Studio, or compile Rust/C++ with the Android toolchain and expose the native ABI through JNI/NDK. Play Store distribution requires the publisher's signing key.

## DAWs and game engines
Use the Python MIDI bridge, JUCE adapter, or either native C ABI.
