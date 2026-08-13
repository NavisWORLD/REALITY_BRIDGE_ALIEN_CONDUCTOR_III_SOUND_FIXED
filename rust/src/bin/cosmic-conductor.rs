use cosmic_conductor::{midi_to_hz, soft_limit, ConductorMacros, StringVoice};
use std::env;
use std::fs::File;
use std::io::{self, Write};
fn write_wav(path:&str,samples:&[f32],sample_rate:u32)->io::Result<()> {
 let mut file=File::create(path)?; let channels:u16=1; let bits:u16=16; let block=channels*bits/8; let rate=sample_rate*block as u32; let data=samples.len() as u32*block as u32; let riff=36+data;
 file.write_all(b"RIFF")?; file.write_all(&riff.to_le_bytes())?; file.write_all(b"WAVEfmt ")?; file.write_all(&16_u32.to_le_bytes())?; file.write_all(&1_u16.to_le_bytes())?; file.write_all(&channels.to_le_bytes())?; file.write_all(&sample_rate.to_le_bytes())?; file.write_all(&rate.to_le_bytes())?; file.write_all(&block.to_le_bytes())?; file.write_all(&bits.to_le_bytes())?; file.write_all(b"data")?; file.write_all(&data.to_le_bytes())?;
 for sample in samples { let pcm=(sample.clamp(-1.0,1.0)*i16::MAX as f32) as i16; file.write_all(&pcm.to_le_bytes())?; } Ok(())
}
fn render(path:&str)->io::Result<()> { let sr=48_000_u32; let mut voice=StringVoice::new(sr as f64); let m=ConductorMacros::default(); let notes=[48.0,55.0,60.0,64.0,67.0,72.0]; let mut out=Vec::with_capacity(sr as usize*4); for midi in notes { voice.pluck(midi_to_hz(midi,440.0),0.72,m.string_damping(),m.brightness(),0.28); for _ in 0..(sr/2) { out.push(soft_limit(voice.process(),1.1)); } } while out.len()<sr as usize*4 { out.push(voice.process()); } write_wav(path,&out,sr) }
fn usage(){ eprintln!("Reality Bridge // Cosmic Conductor Engine\nusage:\n  cosmic-conductor freq <midi>\n  cosmic-conductor render [output.wav]\n  cosmic-conductor demo"); }
fn main(){ let args:Vec<String>=env::args().collect(); match args.get(1).map(String::as_str) { Some("freq")=>{let midi=args.get(2).and_then(|s|s.parse::<f64>().ok()).unwrap_or(69.0); println!("{:.6}",midi_to_hz(midi,440.0));}, Some("render")=>{let path=args.get(2).map(String::as_str).unwrap_or("cosmic_conductor_demo.wav"); render(path).expect("failed to render WAV"); println!("rendered {path}");}, Some("demo")=>{println!("A4 = {:.3} Hz",midi_to_hz(69.0,440.0)); println!("C4 = {:.3} Hz",midi_to_hz(60.0,440.0)); println!("default macros = {:?}",ConductorMacros::default());}, _=>usage() } }
