#include "reality_bridge/synapse.hpp"

#include <algorithm>
#include <cmath>

namespace reality_bridge {
namespace {
double finite_or(double value, double fallback) { return std::isfinite(value) ? value : fallback; }
double clamp(double value, double low, double high) { return std::max(low, std::min(high, value)); }
SynapseConfig sanitize(SynapseConfig c) {
    c.decay = clamp(finite_or(c.decay, 2.0), 0.0, 100.0);
    c.trace_decay = clamp(finite_or(c.trace_decay, 1.0), 0.0, 100.0);
    c.threshold = clamp(finite_or(c.threshold, 0.15), -4.0, 4.0);
    c.gain = clamp(finite_or(c.gain, 1.0), 0.0, 16.0);
    c.plasticity = clamp(finite_or(c.plasticity, 0.05), 0.0, 1.0);
    c.weight_min = clamp(finite_or(c.weight_min, 0.10), 0.001, 10.0);
    c.weight_max = clamp(finite_or(c.weight_max, 2.00), c.weight_min, 10.0);
    c.target_activity = clamp(finite_or(c.target_activity, 0.35), 0.0, 1.0);
    c.homeostasis = clamp(finite_or(c.homeostasis, 0.02), 0.0, 10.0);
    return c;
}
}

Synapse::Synapse(SynapseConfig config) : config_(sanitize(config)) { reset(); }

double Synapse::pulse(double input, double modulation, double dt_seconds) {
    const double dt = clamp(finite_or(dt_seconds, 0.01), 1.0e-6, 1.0);
    const double x = clamp(finite_or(input, 0.0), -4.0, 4.0);
    const double m = clamp(finite_or(modulation, 0.0), -4.0, 4.0);
    const double potential_decay = std::exp(-config_.decay * dt);
    const double trace_decay = std::exp(-config_.trace_decay * dt);
    const double effective_threshold = config_.threshold + state_.threshold_offset;
    const double drive = x * state_.weight + state_.pending_coupling + m * state_.trace;
    state_.potential = state_.potential * potential_decay + drive * (1.0 - potential_decay);
    state_.activation = std::tanh(config_.gain * (state_.potential - effective_threshold));
    state_.trace = state_.trace * trace_decay + state_.activation * (1.0 - trace_decay);
    state_.threshold_offset = clamp(state_.threshold_offset + config_.homeostasis * (std::abs(state_.activation) - config_.target_activity) * dt, -2.0, 2.0);
    state_.pending_coupling = 0.0;
    state_.last_input = x;
    state_.last_output = state_.activation;
    ++state_.tick;
    return state_.last_output;
}

void Synapse::reinforce(double reward) {
    const double r = clamp(finite_or(reward, 0.0), -1.0, 1.0);
    const double delta = config_.plasticity * r * state_.trace * state_.last_input;
    state_.weight = clamp(state_.weight + delta, config_.weight_min, config_.weight_max);
}

void Synapse::couple(double source_output, double strength) {
    const double source = clamp(finite_or(source_output, 0.0), -1.0, 1.0);
    const double amount = clamp(finite_or(strength, 0.0), -2.0, 2.0);
    state_.pending_coupling = clamp(state_.pending_coupling + source * amount, -4.0, 4.0);
}

void Synapse::reset() {
    state_ = SynapseState{};
    state_.weight = clamp(1.0, config_.weight_min, config_.weight_max);
}

void Synapse::restore(const SynapseState& incoming) {
    state_.potential = clamp(finite_or(incoming.potential, 0.0), -16.0, 16.0);
    state_.activation = clamp(finite_or(incoming.activation, 0.0), -1.0, 1.0);
    state_.trace = clamp(finite_or(incoming.trace, 0.0), -1.0, 1.0);
    state_.weight = clamp(finite_or(incoming.weight, 1.0), config_.weight_min, config_.weight_max);
    state_.pending_coupling = clamp(finite_or(incoming.pending_coupling, 0.0), -4.0, 4.0);
    state_.last_input = clamp(finite_or(incoming.last_input, 0.0), -4.0, 4.0);
    state_.last_output = clamp(finite_or(incoming.last_output, 0.0), -1.0, 1.0);
    state_.threshold_offset = clamp(finite_or(incoming.threshold_offset, 0.0), -2.0, 2.0);
    state_.tick = incoming.tick;
}

} // namespace reality_bridge
