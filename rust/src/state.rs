#[derive(Clone, Copy, Debug, PartialEq)]
pub struct ConductorMacros { pub energy: f32, pub entropy: f32, pub life: f32, pub motion: f32, pub gravity: f32, pub alien: f32 }
impl Default for ConductorMacros {
    fn default() -> Self { Self { energy: 0.55, entropy: 0.25, life: 0.62, motion: 0.45, gravity: 0.70, alien: 0.30 } }
}
impl ConductorMacros {
    pub fn normalized(self) -> Self { Self { energy: self.energy.clamp(0.0,1.0), entropy: self.entropy.clamp(0.0,1.0), life: self.life.clamp(0.0,1.0), motion: self.motion.clamp(0.0,1.0), gravity: self.gravity.clamp(0.0,1.0), alien: self.alien.clamp(0.0,1.0) } }
    pub fn string_damping(self) -> f32 { let m=self.normalized(); (0.30+0.55*m.life-0.20*m.entropy).clamp(0.0,1.0) }
    pub fn brightness(self) -> f32 { let m=self.normalized(); (0.20+0.55*m.energy+0.25*m.alien).clamp(0.0,1.0) }
    pub fn density(self) -> f32 { let m=self.normalized(); (0.12+0.46*m.energy+0.18*m.motion+0.12*m.entropy).clamp(0.0,1.0) }
}
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct MusicalState { pub bpm: f32, pub root_midi: i32, pub velocity: f32, pub macros: ConductorMacros }
impl Default for MusicalState { fn default() -> Self { Self { bpm:96.0, root_midi:48, velocity:0.72, macros:ConductorMacros::default() } } }
impl MusicalState {
    pub fn beat_seconds(self) -> f32 { 60.0 / self.bpm.clamp(20.0,400.0) }
    pub fn midi_cc_value(value:f32)->u8 { (value.clamp(0.0,1.0)*127.0).round() as u8 }
}
#[cfg(test)] mod tests { use super::*; #[test] fn macros_stay_normalized(){ let m=ConductorMacros{energy:2.0,entropy:-1.0,life:0.5,motion:0.5,gravity:0.5,alien:0.5}.normalized(); assert_eq!(m.energy,1.0); assert_eq!(m.entropy,0.0); } }
