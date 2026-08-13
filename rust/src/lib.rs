//! Reality Bridge // Cosmic Conductor Engine
//!
//! Dependency-free Rust DSP/state core with a stable C ABI.

mod dsp;
mod state;

pub use dsp::{hz_to_midi, midi_to_hz, soft_limit, StringVoice};
pub use state::{ConductorMacros, MusicalState};

use std::ptr;

pub const VERSION: &str = env!("CARGO_PKG_VERSION");

#[no_mangle]
pub extern "C" fn cc_midi_to_hz(midi: f64, a4: f64) -> f64 { midi_to_hz(midi, a4) }
#[no_mangle]
pub extern "C" fn cc_hz_to_midi(hz: f64, a4: f64) -> f64 { hz_to_midi(hz, a4) }
#[no_mangle]
pub extern "C" fn cc_soft_limit(sample: f32, drive: f32) -> f32 { soft_limit(sample, drive) }
#[no_mangle]
pub extern "C" fn cc_string_create(sample_rate: f64) -> *mut StringVoice {
    if !sample_rate.is_finite() || sample_rate < 8_000.0 { return ptr::null_mut(); }
    Box::into_raw(Box::new(StringVoice::new(sample_rate)))
}
#[no_mangle]
pub unsafe extern "C" fn cc_string_destroy(voice: *mut StringVoice) {
    if !voice.is_null() { drop(Box::from_raw(voice)); }
}
#[no_mangle]
pub unsafe extern "C" fn cc_string_pluck(voice: *mut StringVoice, hz: f64, force: f32, damping: f32, brightness: f32, pick_position: f32) {
    if let Some(v) = voice.as_mut() { v.pluck(hz, force, damping, brightness, pick_position); }
}
#[no_mangle]
pub unsafe extern "C" fn cc_string_process(voice: *mut StringVoice) -> f32 {
    voice.as_mut().map(StringVoice::process).unwrap_or(0.0)
}
#[no_mangle]
pub unsafe extern "C" fn cc_string_stop(voice: *mut StringVoice) {
    if let Some(v) = voice.as_mut() { v.stop(); }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn frequency_round_trip() {
        for midi in [0.0, 21.0, 60.0, 69.0, 127.0] {
            let hz = midi_to_hz(midi, 440.0);
            assert!((midi - hz_to_midi(hz, 440.0)).abs() < 1e-9);
        }
    }
    #[test]
    fn limiter_is_bounded() {
        for x in [-1000.0_f32, -4.0, -1.0, 0.0, 1.0, 4.0, 1000.0] {
            assert!(soft_limit(x, 1.5).abs() <= 1.0);
        }
    }
}
