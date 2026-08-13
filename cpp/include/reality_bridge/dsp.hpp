#pragma once
#include <cstddef>
#include <cstdint>
#include <vector>
namespace reality_bridge {
double midi_to_hz(double midi,double a4=440.0) noexcept;
double hz_to_midi(double hz,double a4=440.0);
class KarplusStrongString {
public:
 explicit KarplusStrongString(double sample_rate=48000.0);
 void set_sample_rate(double sample_rate);
 void pluck(double frequency_hz,double force=.7,double damping=.992,double brightness=.65,double pick_position=.22);
 float process() noexcept; bool active() const noexcept{return active_;} void stop() noexcept;
private:
 double sample_rate_=48000.0;std::vector<float> delay_;std::size_t index_=0;float damping_=.992f,brightness_=.65f,previous_=0,envelope_=0;bool active_=false;std::uint32_t rng_=0xC0FFEEu;float noise() noexcept;
};
class SoftLimiter {public:void set_drive(float drive) noexcept;float process(float x) const noexcept;private:float drive_=1.6f;};
class StereoBody {public:explicit StereoBody(double sample_rate=48000.0);void set_sample_rate(double sample_rate);void set_size(float size) noexcept;void set_resonance(float resonance) noexcept;void process(float in,float& left,float& right) noexcept;private:double sr_=48000.0;float size_=.55f,resonance_=.65f,z1_l_=0,z1_r_=0;};
}
