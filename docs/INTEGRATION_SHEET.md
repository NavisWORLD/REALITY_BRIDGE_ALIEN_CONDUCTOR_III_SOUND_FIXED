# Integration Sheet
## Add Reality Bridge to an existing setup

Choose the narrowest integration that solves your problem.

## Browser / website
Use `REALITY_BRIDGE_ALIEN_CONDUCTOR_III_SOUND_FIXED.html` as a self-contained instrument, or deploy the repository root as a PWA. Best for phone performance, installation, teaching and local media transformation. Microphone features need HTTPS/localhost and a user gesture.

## Python control engine
```bash
pip install -e ./python
```
```python
from reality_bridge import AccompanimentEngine, VoiceDNA
engine=AccompanimentEngine(seed=42)
engine.observe_voice(VoiceDNA(220,.9,.6,.4,.5,.8,True,0.0))
events=engine.plan_bar()
```
Render the NoteEvents with your own synth, DAW API, MIDI library or network protocol.

## MIDI bridge
```bash
pip install -e './python[midi]'
reality-bridge midi --bpm 96 --bars 8
```
Select a virtual MIDI cable/hardware output. Map CC20–27 for continuous macros.

## C++ library
```cmake
add_subdirectory(path/to/REALITY_BRIDGE/cpp)
target_link_libraries(your_target PRIVATE reality_bridge)
```
```cpp
reality_bridge::KarplusStrongString string(sampleRate);
string.pluck(110.0,.8,.994,.7,.2);
float x=string.process();
```
Best for low-latency native audio, games, embedded hosts and custom plugins.

## C ABI / FFI
Link `reality_bridge_c` and include `reality_bridge/c_api.h`. This is the easiest route for Rust, C#, Swift, Kotlin/NDK, Python ctypes or another C-FFI language.

## JUCE plugin
```bash
cmake -S plugins/juce -B build/plugin -DJUCE_DIR=/path/to/JUCE
cmake --build build/plugin --config Release
```
Best for a MIDI-driven modeled-string instrument inside a DAW.

## Generic JSON bridge
Use `integrations/BRIDGE_PROTOCOL.md`; the protocol carries **musical state**, not raw media.
```json
{"v":1,"type":"macro","time":4.2,"payload":{"energy":0.8,"entropy":0.2,"life":0.7,"motion":0.5,"gravity":0.9}}
```

## Mobile app
PWA: host the repo root over HTTPS. Native shell:
```bash
python app/prepare_mobile.py
cd app/capacitor
npm install
npx cap add android   # or ios
npx cap sync
```
Build/sign with Android Studio/Xcode.

## Integration safety checklist
- [ ] conservative startup gain
- [ ] panic/all-notes-off
- [ ] clamp feedback/frequency input
- [ ] inference/network/file work off the real-time callback
- [ ] treat harmony/pitch/tempo as estimates when appropriate
- [ ] no microphone/media upload without user knowledge/consent
- [ ] artistic macros are not physical measurements
- [ ] test on the target phone/host/audio route, not only desktop Chrome
