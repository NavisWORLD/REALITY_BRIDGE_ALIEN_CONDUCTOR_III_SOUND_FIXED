# Native ABI reference

The project exposes two C-compatible native APIs.

## C++ — `rb_*`
Header: `cpp/include/reality_bridge/c_api.h`

Core calls: `rb_string_create`, `rb_string_destroy`, `rb_string_pluck`, `rb_string_process`, `rb_string_stop`, `rb_midi_to_hz`, `rb_hz_to_midi`, `rb_soft_limit`.

## Rust — `cc_*`
Header: `rust/include/cosmic_conductor.h`

Core calls: `cc_string_create`, `cc_string_destroy`, `cc_string_pluck`, `cc_string_process`, `cc_string_stop`, `cc_midi_to_hz`, `cc_hz_to_midi`, `cc_soft_limit`.

## Lifetime rules
Create once, keep a single owner for the pointer, process samples, then destroy exactly once. Never use a pointer after destroy.

Avoid blocking locks, file I/O, network calls, logging and plugin discovery in realtime audio callbacks.
