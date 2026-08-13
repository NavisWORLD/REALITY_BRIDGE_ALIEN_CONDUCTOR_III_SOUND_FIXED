use cosmic_conductor::{midi_to_hz, ConductorMacros, StringVoice};
#[test] fn a4_is_440(){ assert!((midi_to_hz(69.0,440.0)-440.0).abs()<1e-9); }
#[test] fn string_emits_finite_audio(){ let mut v=StringVoice::new(48_000.0); let m=ConductorMacros::default(); v.pluck(220.0,0.8,m.string_damping(),m.brightness(),0.3); for _ in 0..10_000 { assert!(v.process().is_finite()); } }
