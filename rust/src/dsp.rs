use std::f64::consts::LN_2;

pub fn midi_to_hz(midi: f64, a4: f64) -> f64 {
    let ref_hz = if a4.is_finite() && a4 > 0.0 { a4 } else { 440.0 };
    ref_hz * 2.0_f64.powf((midi - 69.0) / 12.0)
}

pub fn hz_to_midi(hz: f64, a4: f64) -> f64 {
    let ref_hz = if a4.is_finite() && a4 > 0.0 { a4 } else { 440.0 };
    if !hz.is_finite() || hz <= 0.0 { return f64::NEG_INFINITY; }
    69.0 + 12.0 * ((hz / ref_hz).ln() / LN_2)
}

pub fn soft_limit(sample: f32, drive: f32) -> f32 {
    let d = if drive.is_finite() { drive.abs().max(0.0001) } else { 1.0 };
    let norm = d.tanh().max(0.0001);
    ((sample * d).tanh() / norm).clamp(-1.0, 1.0)
}

#[derive(Clone, Debug)]
struct XorShift64 { state: u64 }
impl XorShift64 {
    fn new(seed: u64) -> Self { Self { state: seed.max(1) } }
    fn next_f32(&mut self) -> f32 {
        let mut x = self.state;
        x ^= x << 13; x ^= x >> 7; x ^= x << 17; self.state = x;
        let unit = (x as f64 / u64::MAX as f64) as f32;
        unit * 2.0 - 1.0
    }
}

#[derive(Debug)]
pub struct StringVoice {
    sample_rate: f64,
    buffer: Vec<f32>,
    index: usize,
    damping: f32,
    brightness: f32,
    pick_position: f32,
    last: f32,
    active: bool,
    rng: XorShift64,
}

impl StringVoice {
    pub fn new(sample_rate: f64) -> Self {
        Self { sample_rate: sample_rate.max(8_000.0), buffer: vec![0.0; 2], index: 0, damping: 0.996, brightness: 0.5, pick_position: 0.5, last: 0.0, active: false, rng: XorShift64::new(0x434f_534d_4f53_0667) }
    }
    pub fn pluck(&mut self, hz: f64, force: f32, damping: f32, brightness: f32, pick_position: f32) {
        let safe_hz = hz.clamp(20.0, self.sample_rate * 0.45);
        let delay = (self.sample_rate / safe_hz).round().max(2.0) as usize;
        self.buffer.resize(delay, 0.0);
        self.index = 0;
        self.damping = (0.985 + damping.clamp(0.0, 1.0) * 0.0145).clamp(0.0, 0.9998);
        self.brightness = brightness.clamp(0.0, 1.0);
        self.pick_position = pick_position.clamp(0.02, 0.98);
        self.last = 0.0;
        self.active = true;
        let gain = force.clamp(0.0, 1.0);
        let pick = self.pick_position;
        let len = self.buffer.len() as f32;
        for (i, sample) in self.buffer.iter_mut().enumerate() {
            let phase = i as f32 / len;
            let pick_notch = ((phase - pick).abs() * std::f32::consts::PI).sin().abs();
            *sample = self.rng.next_f32() * gain * (0.35 + 0.65 * self.brightness) * pick_notch;
        }
    }
    pub fn process(&mut self) -> f32 {
        if !self.active || self.buffer.len() < 2 { return 0.0; }
        let next = (self.index + 1) % self.buffer.len();
        let a = self.buffer[self.index];
        let b = self.buffer[next];
        let average = (a + b) * 0.5;
        let filtered = average * (1.0 - self.brightness * 0.32) + a * (self.brightness * 0.32);
        let feedback = filtered * self.damping;
        self.buffer[self.index] = feedback;
        self.index = next;
        self.last = feedback;
        if feedback.abs() < 1e-6 && self.buffer.iter().all(|v| v.abs() < 1e-5) { self.active = false; }
        soft_limit(feedback, 1.25)
    }
    pub fn stop(&mut self) { self.active = false; self.buffer.fill(0.0); self.last = 0.0; }
    pub fn is_active(&self) -> bool { self.active }
    pub fn sample_rate(&self) -> f64 { self.sample_rate }
}
