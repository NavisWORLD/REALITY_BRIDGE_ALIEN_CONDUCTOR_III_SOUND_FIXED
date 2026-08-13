use cosmic_conductor::{midi_to_hz,ConductorMacros,StringVoice};
fn main(){ let m=ConductorMacros::default(); let mut voice=StringVoice::new(48_000.0); voice.pluck(midi_to_hz(57.0,440.0),0.75,m.string_damping(),m.brightness(),0.22); for _ in 0..64 { println!("{}",voice.process()); } }
