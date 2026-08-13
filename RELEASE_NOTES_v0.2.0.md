# Cosmic Conductor Engine v0.2.0 — Packaged Edition

This release turns the open engine into downloadable end-user builds while preserving the full SDK stack.

## Included artifacts

- Windows one-click installer (`Cosmic-Conductor-Engine-Setup-v0.2.0.exe`)
- Windows portable executable
- macOS application bundle ZIP and `.dmg`
- Linux standalone executable bundle
- Android installable APK
- iOS Simulator `.app` ZIP
- Web/PWA ZIP
- source ZIP
- Rust CLI/native-library outputs and C++ shared-library outputs for desktop platforms
- SHA-256 checksums

## iPhone distribution note

The iOS project and simulator app are built in CI. A signed physical-device/App Store IPA requires an Apple Developer signing certificate and provisioning profile owned by the publisher. Those credentials are intentionally not committed to the public repository. The PWA remains installable on iPhone/iPad through Safari when hosted over HTTPS.

## Engineering scope

The release does not change the project’s honesty rules: musical recognition remains inference, artistic macro names are not physical measurements, and signed-store distribution is separated from source/build reproducibility.
