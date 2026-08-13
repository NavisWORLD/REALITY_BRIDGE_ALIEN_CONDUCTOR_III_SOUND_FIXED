# Python installation — every desktop OS

Requires Python 3.10+.

## Windows PowerShell
```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -e ".\python[test,midi]"
reality-bridge demo
cosmic-conductor demo
```

## macOS / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -e './python[test,midi]'
reality-bridge demo
cosmic-conductor demo
```

Pure Python mode needs no C++ compiler. For native DSP, build `cpp/` then import `reality_bridge.native.NativeString`. Set `COSMIC_CONDUCTOR_NATIVE_LIB` when the shared library is in a custom location.
