# Build everything

macOS/Linux: `./scripts/bootstrap.sh`

Windows PowerShell: `.\scripts\bootstrap.ps1`

Manual verification:
```bash
python -m pytest -q python/tests
cargo test --manifest-path rust/Cargo.toml --all-targets
cargo build --release --manifest-path rust/Cargo.toml
cmake -S cpp -B build/cpp -DRB_BUILD_SHARED=ON -DRB_BUILD_TESTS=ON
cmake --build build/cpp --config Release
ctest --test-dir build/cpp -C Release --output-on-failure
python tools/reconstruct_standalone.py
node tools/audit_html.mjs
```

Source-first publication is deliberate: browser instrument, Python orchestration, Rust safe native core, C++ original native DSP, JUCE plugin path and Capacitor mobile wrapper. Signed store/plugin binaries remain downstream release artifacts because signing credentials belong to the publisher.
