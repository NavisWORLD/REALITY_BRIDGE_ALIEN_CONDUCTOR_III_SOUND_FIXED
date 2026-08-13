# Release Validation — v0.1 Open Engine

Publication date: 2026-08-12 (America/Chicago)

## Published commits

- `7cb06f7b6f4a690b1a35abff5f15d111f02a9690` — full open-engine / learning-repository publication.
- `13e7c1b4ff82e3a1848290a63f72497aea78c03f` — GitHub Actions reconstruction of the canonical root standalone HTML from the verified source archive.

## Hosted CI evidence

GitHub Actions CI run `31656257830` completed successfully on the publication branch after the workflow cleanup. Its job reported success for every stage:

1. checkout;
2. Python installation and tests;
3. native C++ CMake build and CTest;
4. deterministic standalone reconstruction;
5. Node setup;
6. HTML static audit.

The earlier publication CI run also passed. The standalone reconstruction workflow completed successfully and committed the generated root HTML.

## Standalone integrity

Canonical generated artifact:

`REALITY_BRIDGE_ALIEN_CONDUCTOR_III_SOUND_FIXED.html`

SHA-256:

`a23304613961f05f3c2ec08d16ed12ef1ea9d4dbc7a770da3742982843a62ac6`

The source archive checksums are in `web/source_archive/SHA256SUMS`.

Static HTML audit at publication:

- IDs: 186
- duplicate IDs: 0
- literal DOM lookups: 256
- missing literal lookups: 0
- inline JavaScript parses successfully

Static analysis is not a substitute for target-device audio-route testing. See `TESTING_AND_VALIDATION.md` for the phone acceptance procedure.

## GitHub Pages status

The PWA deployment workflow is included, but the connected GitHub integration cannot create the repository's first Pages site. GitHub returned `Resource not accessible by integration` for that administration operation. This does not affect repository downloads, CI, reconstruction, Python/C++ builds, MIDI integration, or the standalone HTML.

To enable the hosted PWA once:

1. Open repository **Settings → Pages**.
2. Under **Build and deployment**, select **GitHub Actions** as the source.
3. Open **Actions → Deploy PWA to Pages**.
4. Choose **Run workflow** on `main`.

The deployment workflow is manual so normal code commits do not show a false red Pages check before the repository-level Pages switch is enabled.

## Native/app scope

The C++ core and Python engine are testable source components. JUCE plugin targets and Capacitor native wrappers are source/build scaffolds that require their external platform SDKs and, for distribution, the publisher's signing credentials. The repository does not claim unsigned source code is a signed App Store, Play Store, AU, or VST3 release binary.
