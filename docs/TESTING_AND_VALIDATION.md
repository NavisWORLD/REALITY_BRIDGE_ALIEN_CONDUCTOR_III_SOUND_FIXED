# Testing and Validation

## Automated coverage

### Python
- MIDI/frequency round trips
- bounded harmony hypothesis from known pitch patterns
- generated events remain legal MIDI values
- WAV analyzer returns non-empty features

### C++
- frequency conversion
- modeled string produces non-zero signal after pluck
- limiter output remains bounded

### HTML static audit
`tools/audit_html.mjs` checks JavaScript parsing, duplicate IDs, literal DOM lookups, and absence of inline onclick handlers. Static checks do not replace mobile runtime/audio-route testing.

## Manual phone acceptance
1. Host on HTTPS/localhost.
2. Press AWAKEN.
3. Use AUDIO RUNNING / TEST OUTPUT and verify confirmation notes.
4. Press PLAY and verify transport + audible output.
5. Pluck Gravity Guitar.
6. Enable SING WITH ME and verify pitch/confidence changes without raw mic feedback.
7. Load supported audio/video and verify analysis reaches READY.
8. Test TRANSMUTE and source/bridge mix.
9. Press PANIC and verify active audio clears.
10. Background/foreground and verify resume after user interaction if the OS suspended audio.

## Claims policy
A test demonstrates only what it measures. UI state does not prove audible output. `AudioContext=running` does not prove the phone chose the intended hardware route. Use direct output tests and target-device listening/measurement.
