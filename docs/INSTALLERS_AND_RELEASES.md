# Installers and binary releases

Cosmic Conductor Engine v0.2.0 includes automated packaging for end users and SDK consumers.

## Deliverables

| Target | Release artifact | Status |
|---|---|---|
| Windows 10/11 | one-click Inno Setup `.exe` + portable `.exe` | automated |
| macOS | ad-hoc-signed `.app.zip` + `.dmg` | automated |
| Linux x86_64 | standalone PyInstaller executable `.tar.gz` | automated |
| Android | installable debug-signed APK | automated |
| iPhone/iPad | compiled iOS Simulator `.app.zip` + installable HTTPS PWA | automated |
| Web | PWA ZIP | automated |
| Rust SDK | CLI + cdylib/staticlib outputs where supported | automated for desktop release jobs |
| C++ SDK | shared-library outputs | automated for desktop release jobs |
| GitHub Release | v0.2.0 with artifacts + checksums | automated |

## Why the desktop wrapper uses localhost

The frozen desktop launcher bundles the web instrument inside the executable/app and serves it from `127.0.0.1` on a free port. This preserves browser security behavior needed by Web Audio and microphone APIs more reliably than opening the instrument through `file://`.

## Windows

Download and run `Cosmic-Conductor-Engine-Setup-v0.2.0.exe`. The installer adds Start-menu integration and optionally a desktop shortcut.

## macOS

Open `Cosmic-Conductor-Engine-v0.2.0.dmg` and run the included app. CI uses ad-hoc signing so the bundle has a coherent code signature, but it is not Apple-notarized. Public notarization requires the publisher’s Apple Developer identity.

## Android

`Cosmic-Conductor-Android-v0.2.0.apk` is built with Gradle’s debug signing and can be sideloaded on devices that permit installs from the chosen source. Store publication should use the publisher’s release keystore.

## iPhone/iPad

The CI pipeline compiles a native Capacitor iOS application for the simulator and publishes it as `Cosmic-Conductor-iOS-Simulator-v0.2.0.app.zip`. The same source is ready for Xcode device/archive builds. A distributable physical-device `.ipa` cannot be cryptographically signed without a real Apple Developer certificate/provisioning profile; those secrets belong in repository Actions secrets, never in source control. The hosted PWA is the zero-signing install path on iPhone/iPad.

## Release workflow

`.github/workflows/package-release.yml` builds the platform artifacts and creates/updates GitHub Release `v0.2.0`. Every published file is covered by `SHA256SUMS.txt`.
