use cosmic_conductor::{midi_to_hz, ConductorMacros, StringVoice};
fn main(){ let mut voice=StringVoice::new(48_000.0); let m=ConductorMacros::default(); voice.pluck(midi_to_hz(60.0,440.0),0.8,m.string_damping(),m.brightness(),0.25); let samples:Vec<f32>=(0..128).map(|_|voice.process()).collect(); println!("{samples:?}"); }
