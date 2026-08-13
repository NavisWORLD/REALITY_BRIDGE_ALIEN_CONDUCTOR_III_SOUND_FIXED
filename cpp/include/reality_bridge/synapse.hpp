#pragma once

#include <cstdint>

namespace reality_bridge {

constexpr std::uint32_t SYNAPSE_ABI_VERSION = 1;

struct SynapseConfig {
    double decay = 2.0;
    double trace_decay = 1.0;
    double threshold = 0.15;
    double gain = 1.0;
    double plasticity = 0.05;
    double weight_min = 0.10;
    double weight_max = 2.00;
    double target_activity = 0.35;
    double homeostasis = 0.02;
};

struct SynapseState {
    double potential = 0.0;
    double activation = 0.0;
    double trace = 0.0;
    double weight = 1.0;
    double pending_coupling = 0.0;
    double last_input = 0.0;
    double last_output = 0.0;
    double threshold_offset = 0.0;
    std::uint64_t tick = 0;
};

class Synapse {
public:
    explicit Synapse(SynapseConfig config = {});
    double pulse(double input, double modulation = 0.0, double dt_seconds = 0.01);
    double step(double input, double modulation = 0.0, double dt_seconds = 0.01) { return pulse(input, modulation, dt_seconds); }
    void reinforce(double reward);
    void couple(double source_output, double strength);
    void reset();
    void restore(const SynapseState& state);
    const SynapseConfig& config() const noexcept { return config_; }
    const SynapseState& state() const noexcept { return state_; }
private:
    SynapseConfig config_;
    SynapseState state_;
};

} // namespace reality_bridge
