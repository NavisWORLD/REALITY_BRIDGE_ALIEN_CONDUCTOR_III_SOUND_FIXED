#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
echo "== Reality Bridge // Cosmic Conductor Engine =="
PY="${PYTHON:-python3}"
"$PY" -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e './python[test]'
python -m pytest -q python/tests
if command -v cargo >/dev/null 2>&1; then cargo test --manifest-path rust/Cargo.toml --all-targets; cargo build --release --manifest-path rust/Cargo.toml; else echo "[skip] Rust/Cargo not installed"; fi
if command -v cmake >/dev/null 2>&1; then cmake -S cpp -B build/cpp -DRB_BUILD_SHARED=ON -DRB_BUILD_TESTS=ON; cmake --build build/cpp --config Release --parallel 2; ctest --test-dir build/cpp -C Release --output-on-failure; else echo "[skip] CMake not installed"; fi
echo "Bootstrap complete."
