//! Reality Bridge // Cosmic Synapse
//!
//! Safe, dependency-free implementation of Synaptic Core Contract v1.

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
        Self {
            decay: 2.0,
            trace_decay: 1.0,
            threshold: 0.15,
            gain: 1.0,
            plasticity: 0.05,
            weight_min: 0.10,
            weight_max: 2.0,
            target_activity: 0.35,
            homeostasis: 0.02,
        }
    }
}

impl SynapseConfig {
    pub fn normalized(self) -> Self {
        let weight_min = finite_or(self.weight_min, 0.10).clamp(0.001, 10.0);
        Self {
            decay: finite_or(self.decay, 2.0).clamp(0.0, 100.0),
            trace_decay: finite_or(self.trace_decay, 1.0).clamp(0.0, 100.0),
            threshold: finite_or(self.threshold, 0.15).clamp(-4.0, 4.0),
            gain: finite_or(self.gain, 1.0).clamp(0.0, 16.0),
            plasticity: finite_or(self.plasticity, 0.05).clamp(0.0, 1.0),
            weight_min,
            weight_max: finite_or(self.weight_max, 2.0).clamp(weight_min, 10.0),
            target_activity: finite_or(self.target_activity, 0.35).clamp(0.0, 1.0),
            homeostasis: finite_or(self.homeostasis, 0.02).clamp(0.0, 10.0),
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct SynapseState {
    pub potential: f64,
    pub activation: f64,
    pub trace: f64,
    pub weight: f64,
    pub pending_coupling: f64,
    pub last_input: f64,
    pub last_output: f64,
    pub threshold_offset: f64,
    pub tick: u64,
}

impl Default for SynapseState {
    fn default() -> Self {
        Self {
            potential: 0.0,
            activation: 0.0,
            trace: 0.0,
            weight: 1.0,
            pending_coupling: 0.0,
            last_input: 0.0,
            last_output: 0.0,
            threshold_offset: 0.0,
            tick: 0,
        }
    }
}

#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Synapse {
    pub config: SynapseConfig,
    state: SynapseState,
}

impl Default for Synapse {
    fn default() -> Self {
        Self::new(SynapseConfig::default())
    }
}

impl Synapse {
    pub fn new(config: SynapseConfig) -> Self {
        let config = config.normalized();
        let mut state = SynapseState::default();
        state.weight = 1.0_f64.clamp(config.weight_min, config.weight_max);
        Self { config, state }
    }

    pub fn state(&self) -> SynapseState {
        self.state
    }

    pub fn pulse(&mut self, input: f64, modulation: f64, dt_seconds: f64) -> f64 {
        let dt = finite_or(dt_seconds, 0.01).clamp(1.0e-6, 1.0);
        let x = finite_or(input, 0.0).clamp(-4.0, 4.0);
        let m = finite_or(modulation, 0.0).clamp(-4.0, 4.0);
        let potential_decay = (-self.config.decay * dt).exp();
        let trace_decay = (-self.config.trace_decay * dt).exp();
        let effective_threshold = self.config.threshold + self.state.threshold_offset;
        let drive = x * self.state.weight + self.state.pending_coupling + m * self.state.trace;

        self.state.potential =
            self.state.potential * potential_decay + drive * (1.0 - potential_decay);
        self.state.activation =
            (self.config.gain * (self.state.potential - effective_threshold)).tanh();
        self.state.trace =
            self.state.trace * trace_decay + self.state.activation * (1.0 - trace_decay);
        self.state.threshold_offset = (self.state.threshold_offset
            + self.config.homeostasis
                * (self.state.activation.abs() - self.config.target_activity)
                * dt)
            .clamp(-2.0, 2.0);
        self.state.pending_coupling = 0.0;
        self.state.last_input = x;
        self.state.last_output = self.state.activation;
        self.state.tick = self.state.tick.saturating_add(1);
        self.state.last_output
    }

    pub fn step(&mut self, input: f64, modulation: f64, dt_seconds: f64) -> f64 {
        self.pulse(input, modulation, dt_seconds)
    }

    pub fn reinforce(&mut self, reward: f64) {
        let reward = finite_or(reward, 0.0).clamp(-1.0, 1.0);
        let delta = self.config.plasticity
            * reward
            * self.state.trace
            * self.state.last_input;
        self.state.weight =
            (self.state.weight + delta).clamp(self.config.weight_min, self.config.weight_max);
    }

    pub fn couple(&mut self, source_output: f64, strength: f64) {
        let source = finite_or(source_output, 0.0).clamp(-1.0, 1.0);
        let strength = finite_or(strength, 0.0).clamp(-2.0, 2.0);
        self.state.pending_coupling =
            (self.state.pending_coupling + source * strength).clamp(-4.0, 4.0);
    }

    pub fn reset(&mut self) {
        self.state = SynapseState::default();
        self.state.weight = 1.0_f64.clamp(self.config.weight_min, self.config.weight_max);
    }

    pub fn snapshot(&self) -> SynapseState {
        self.state
    }

    pub fn restore(&mut self, incoming: SynapseState) {
        self.state = SynapseState {
            potential: finite_or(incoming.potential, 0.0).clamp(-16.0, 16.0),
            activation: finite_or(incoming.activation, 0.0).clamp(-1.0, 1.0),
            trace: finite_or(incoming.trace, 0.0).clamp(-1.0, 1.0),
            weight: finite_or(incoming.weight, 1.0)
                .clamp(self.config.weight_min, self.config.weight_max),
            pending_coupling: finite_or(incoming.pending_coupling, 0.0).clamp(-4.0, 4.0),
            last_input: finite_or(incoming.last_input, 0.0).clamp(-4.0, 4.0),
            last_output: finite_or(incoming.last_output, 0.0).clamp(-1.0, 1.0),
            threshold_offset: finite_or(incoming.threshold_offset, 0.0).clamp(-2.0, 2.0),
            tick: incoming.tick,
        };
    }

    pub fn process<I>(&mut self, inputs: I, modulation: f64, dt_seconds: f64) -> Vec<f64>
    where
        I: IntoIterator<Item = f64>,
    {
        inputs
            .into_iter()
            .map(|input| self.pulse(input, modulation, dt_seconds))
            .collect()
    }
}

fn finite_or(value: f64, fallback: f64) -> f64 {
    if value.is_finite() { value } else { fallback }
}

pub fn conformance_sequence() -> SynapseState {
    let mut synapse = Synapse::default();
    let inputs = [0.25, 0.8, -0.2, 0.6, 0.0, -0.4, 0.9];
    let modulations = [0.0, 0.1, 0.2, -0.1, 0.05, 0.0, 0.15];
    for index in 0..inputs.len() {
        if index == 2 {
            synapse.couple(0.35, 0.4);
        }
        synapse.pulse(inputs[index], modulations[index], 0.01);
        if index == 3 {
            synapse.reinforce(0.7);
        }
        if index == 5 {
            synapse.reinforce(-0.2);
        }
    }
    synapse.state()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn golden_vector_matches_contract() {
        let state = conformance_sequence();
        assert!((state.potential - 0.038840176720408945).abs() < 1.0e-12);
        assert!((state.activation + 0.11044113874970204).abs() < 1.0e-12);
        assert!((state.trace + 0.008475792084489108).abs() < 1.0e-12);
        assert!((state.weight - 0.9998629394170829).abs() < 1.0e-12);
        assert!((state.threshold_offset + 0.00031425539024381897).abs() < 1.0e-12);
        assert_eq!(state.tick, 7);
    }

    #[test]
    fn invalid_configuration_is_bounded() {
        let synapse = Synapse::new(SynapseConfig {
            decay: f64::NAN,
            weight_min: -10.0,
            weight_max: f64::INFINITY,
            ..SynapseConfig::default()
        });
        assert!(synapse.config.decay.is_finite());
        assert!(synapse.config.weight_min > 0.0);
        assert!(synapse.config.weight_max >= synapse.config.weight_min);
    }

    #[test]
    fn snapshot_restore_round_trip() {
        let mut first = Synapse::default();
        first.pulse(0.75, 0.1, 0.01);
        first.reinforce(0.5);
        let snapshot = first.snapshot();

        let mut second = Synapse::default();
        second.restore(snapshot);
        assert_eq!(second.state(), snapshot);
    }
}
