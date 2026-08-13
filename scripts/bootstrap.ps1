$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root
Write-Host "== Reality Bridge // Cosmic Conductor Engine =="
if (Get-Command py -ErrorAction SilentlyContinue) { & py -3.12 -m venv .venv } else { & python -m venv .venv }
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -e ".\python[test]"
& .\.venv\Scripts\python.exe -m pytest -q python\tests
if (Get-Command cargo -ErrorAction SilentlyContinue) { cargo test --manifest-path rust\Cargo.toml --all-targets; cargo build --release --manifest-path rust\Cargo.toml } else { Write-Host "[skip] Rust/Cargo not installed" }
if (Get-Command cmake -ErrorAction SilentlyContinue) { cmake -S cpp -B build\cpp -DRB_BUILD_SHARED=ON -DRB_BUILD_TESTS=ON; cmake --build build\cpp --config Release --parallel 2; ctest --test-dir build\cpp -C Release --output-on-failure } else { Write-Host "[skip] CMake not installed" }
Write-Host "Bootstrap complete."
