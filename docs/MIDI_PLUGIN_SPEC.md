# MIDI + Plugin Bridge Specification
## Reality Bridge v0.1

This specification lets a DAW, hardware synth, plugin, game engine or performance rig participate in Reality Bridge without recreating the browser UI.

## MIDI roles
- Channel 1 — harmonic/pad voice
- Channel 2 — bass
- Channel 3 — Gravity Guitar / modeled string
- Channel 10 — percussion by convention

A host MAY remap channels. Note On velocity communicates excitation/dynamic intent. Note Off releases external sustained voices; modeled plucks may decay naturally.

## CC macros
The recommended CC20–27 map is defined in `integrations/MIDI_MAP.md`. Values map linearly 0..127 to 0..1 unless the host documents another curve. CC123 MUST act as all-notes-off when the bridge owns active voices. CC64 MAY hold generated harmony.

## Pitch bend
Pitch bend is for continuous bends, microtonal movement and Gravity Guitar glissandi. Sender and destination MUST agree on bend range. MPE is a future extension; the current reference does not claim MPE conformance.

## Clock
When DAW-synchronized, host tempo/transport SHOULD be authoritative. Standalone Reality Bridge may own BPM. Do not run competing clocks without explicit master selection.

## JUCE adapter
`plugins/juce/` builds a MIDI instrument with VST3/AU/Standalone targets when JUCE and platform SDKs are supplied.

Processing path: `MIDI Note On -> KarplusStrongString voices -> StereoBody -> SoftLimiter -> host output`.

Automatable parameters: damping, brightness, pick position, body, resonance, output.

## High-level engine connection patterns
1. **MIDI only** — run Python/web conductor externally and send note/CC data.
2. **Host automation** — map Reality Bridge macros to plugin parameters/CC.
3. **Native protocol adapter** — consume `BRIDGE_PROTOCOL.md` and translate to notes/parameters.

## Real-time rules
Inside an audio callback: no network I/O; no per-sample allocation; no large JSON parsing; no blocking UI locks; clamp feedback/gain; process panic/all-notes-off deterministically. Perform inference/file/network work off the audio thread.

## Build matrix
| Target | Source included | External requirement |
|---|---|---|
| MIDI bridge | yes | mido, python-rtmidi, OS MIDI |
| C ABI | yes | C++17 compiler |
| VST3 | yes via JUCE target | JUCE + supported toolchain/SDK |
| AU | yes via JUCE target | macOS + Xcode + JUCE |
| Standalone native plugin | yes via JUCE target | JUCE + platform toolchain |
| Signed binary/store release | no | publisher signing credentials/compliance |
