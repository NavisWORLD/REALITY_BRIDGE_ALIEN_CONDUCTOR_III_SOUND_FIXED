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

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct SynapseConfig {
    pub decay: f64,
    pub trace_decay: f64,
    pub threshold: f64,
    pub gain: f64,
    pub plasticity: f64,
    pub weight_min: f64,
    pub weight_max: f64,
    pub target_activity: f64,
    pub homeostasis: f64,
}
impl Default for SynapseConfig {
    fn default() -> Self {
        Self { decay:2.0, trace_decay:1.0, threshold:0.15, gain:1.0, plasticity:0.05, weight_min:0.10, weight_max:2.0, target_activity:0.35, homeostasis:0.02 }
    }
}
impl SynapseConfig {
    pub fn normalized(self) -> Self {
        let min = finite_or(self.weight_min,0.10).clamp(0.001,10.0);
        Self {
            decay: finite_or(self.decay,2.0).clamp(0.0,100.0),
            trace_decay: finite_or(self.trace_decay,1.0).clamp(0.0,100.0),
            threshold: finite_or(self.threshold,0.15).clamp(-4.0,4.0),
            gain: finite_or(self.gain,1.0).clamp(0.0,16.0),
            plasticity: finite_or(self.plasticity,0.05).clamp(0.0,1.0),
            weight_min: min,
            weight_max: finite_or(self.weight_max,2.0).clamp(min,10.0),
            target_activity: finite_or(self.target_activity,0.35).clamp(0.0,1.0),
            homeostasis: finite_or(self.homeostasis,0.02).clamp(0.0,10.0),
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct SynapseState {
    pub potential:f64,
    pub activation:f64,
    pub trace:f64,
    pub weight:f64,
    pub pending_coupling:f64,
    pub last_input:f64,
    pub last_output:f64,
    pub threshold_offset:f64,
    pub tick:u64,
}
impl Default for SynapseState {
    fn default() -> Self { Self { potential:0.0, activation:0.0, trace:0.0, weight:1.0, pending_coupling:0.0, last_input:0.0, last_output:0.0, threshold_offset:0.0, tick:0 } }
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Synapse { pub config:SynapseConfig, state:SynapseState }
impl Default for Synapse { fn default()->Self { Self::new(SynapseConfig::default()) } }
impl Synapse {
    pub fn new(config:SynapseConfig)->Self {
        let config=config.normalized();
        let mut state=SynapseState::default();
        state.weight=1.0_f64.clamp(config.weight_min,config.weight_max);
        Self{config,state}
    }
    pub fn state(&self)->SynapseState { self.state }
    pub fn pulse(&mut self,input:f64,modulation:f64,dt_seconds:f64)->f64 {
        let dt=finite_or(dt_seconds,0.01).clamp(1.0e-6,1.0);
        let x=finite_or(input,0.0).clamp(-4.0,4.0);
        let m=finite_or(modulation,0.0).clamp(-4.0,4.0);
        let p_decay=(-self.config.decay*dt).exp();
        let t_decay=(-self.config.trace_decay*dt).exp();
        let threshold=self.config.threshold+self.state.threshold_offset;
        let drive=x*self.state.weight+self.state.pending_coupling+m*self.state.trace;
        self.state.potential=self.state.potential*p_decay+drive*(1.0-p_decay);
        self.state.activation=(self.config.gain*(self.state.potential-threshold)).tanh();
        self.state.trace=self.state.trace*t_decay+self.state.activation*(1.0-t_decay);
        self.state.threshold_offset=(self.state.threshold_offset+self.config.homeostasis*(self.state.activation.abs()-self.config.target_activity)*dt).clamp(-2.0,2.0);
        self.state.pending_coupling=0.0;
        self.state.last_input=x;
        self.state.last_output=self.state.activation;
        self.state.tick=self.state.tick.saturating_add(1);
        self.state.last_output
    }
    pub fn step(&mut self,input:f64,modulation:f64,dt_seconds:f64)->f64 { self.pulse(input,modulation,dt_seconds) }
    pub fn reinforce(&mut self,reward:f64) {
        let r=finite_or(reward,0.0).clamp(-1.0,1.0);
        let delta=self.config.plasticity*r*self.state.trace*self.state.last_input;
        self.state.weight=(self.state.weight+delta).clamp(self.config.weight_min,self.config.weight_max);
    }
    pub fn couple(&mut self,source_output:f64,strength:f64) {
        let source=finite_or(source_output,0.0).clamp(-1.0,1.0);
        let amount=finite_or(strength,0.0).clamp(-2.0,2.0);
        self.state.pending_coupling=(self.state.pending_coupling+source*amount).clamp(-4.0,4.0);
    }
    pub fn reset(&mut self) {
        self.state=SynapseState::default();
        self.state.weight=1.0_f64.clamp(self.config.weight_min,self.config.weight_max);
    }
    pub fn restore(&mut self,s:SynapseState) {
        self.state=SynapseState{
            potential:finite_or(s.potential,0.0).clamp(-16.0,16.0),
            activation:finite_or(s.activation,0.0).clamp(-1.0,1.0),
            trace:finite_or(s.trace,0.0).clamp(-1.0,1.0),
            weight:finite_or(s.weight,1.0).clamp(self.config.weight_min,self.config.weight_max),
            pending_coupling:finite_or(s.pending_coupling,0.0).clamp(-4.0,4.0),
            last_input:finite_or(s.last_input,0.0).clamp(-4.0,4.0),
            last_output:finite_or(s.last_output,0.0).clamp(-1.0,1.0),
            threshold_offset:finite_or(s.threshold_offset,0.0).clamp(-2.0,2.0),
            tick:s.tick,
        };
    }
}
fn finite_or(v:f64,fallback:f64)->f64 { if v.is_finite(){v}else{fallback} }

#[cfg(test)] mod tests {
    use super::*;
    #[test] fn macros_stay_normalized(){ let m=ConductorMacros{energy:2.0,entropy:-1.0,life:0.5,motion:0.5,gravity:0.5,alien:0.5}.normalized(); assert_eq!(m.energy,1.0); assert_eq!(m.entropy,0.0); }
    #[test] fn synapse_golden_vector(){
        let mut s=Synapse::default();
        let xs=[0.25,0.8,-0.2,0.6,0.0,-0.4,0.9];
        let ms=[0.0,0.1,0.2,-0.1,0.05,0.0,0.15];
        for i in 0..xs.len(){ if i==2{s.couple(0.35,0.4);} s.pulse(xs[i],ms[i],0.01); if i==3{s.reinforce(0.7);} if i==5{s.reinforce(-0.2);} }
        let st=s.state();
        assert!((st.potential-0.038840176720408945).abs()<1e-12);
        assert!((st.activation+0.11044113874970204).abs()<1e-12);
        assert!((st.trace+0.008475792084489108).abs()<1e-12);
        assert!((st.weight-0.9998629394170829).abs()<1e-12);
        assert!((st.threshold_offset+0.00031425539024381897).abs()<1e-12);
        assert_eq!(st.tick,7);
    }
}
