# JUCE MIDI instrument plugin

This adapter turns the C++ Reality Bridge string core into a normal MIDI-driven instrument. The source is complete, but plugin binaries depend on **JUCE + the platform toolchain** and are not pre-signed here.

```bash
cmake -S plugins/juce -B build/plugin -DJUCE_DIR=/path/to/JUCE
cmake --build build/plugin --config Release
```

Targets requested from JUCE: VST3, AU and Standalone. AU builds require macOS/Xcode. Distribution/signing rules are host/platform-specific.

Current plugin scope is intentionally focused: MIDI note input -> modeled string voices -> body coloration -> safe limiter. The web/Python engines carry the higher-level Voice DNA, Media DNA and generative-conductor logic. See `docs/INTEGRATION_SHEET.md` for connecting them.
