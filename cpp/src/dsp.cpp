#include "reality_bridge/dsp.hpp"
#include <algorithm>
#include <cmath>
#include <stdexcept>
namespace reality_bridge {
double midi_to_hz(double midi,double a4) noexcept{return a4*std::pow(2.0,(midi-69.0)/12.0);} 
double hz_to_midi(double hz,double a4){if(!(hz>0.0))throw std::invalid_argument("frequency must be positive");return 69.0+12.0*std::log2(hz/a4);} 
KarplusStrongString::KarplusStrongString(double sr){set_sample_rate(sr);} 
void KarplusStrongString::set_sample_rate(double sr){sample_rate_=std::clamp(sr,8000.0,384000.0);stop();}
float KarplusStrongString::noise() noexcept{rng_^=rng_<<13;rng_^=rng_>>17;rng_^=rng_<<5;return(static_cast<float>(rng_&0xFFFFu)/32767.5f)-1.0f;}
void KarplusStrongString::pluck(double hz,double force,double damping,double brightness,double pick_position){const double maxf=sample_rate_*.45;hz=std::clamp(hz,20.0,maxf);force=std::clamp(force,0.0,1.0);damping_=static_cast<float>(std::clamp(damping,.85,.99995));brightness_=static_cast<float>(std::clamp(brightness,.02,.995));const std::size_t n=std::max<std::size_t>(2,static_cast<std::size_t>(std::llround(sample_rate_/hz)));delay_.assign(n,0);index_=0;previous_=0;const float pick=static_cast<float>(std::clamp(pick_position,.02,.98));const float amp=static_cast<float>(force)*.65f;const std::size_t notch=std::max<std::size_t>(1,static_cast<std::size_t>(pick*n));for(std::size_t i=0;i<n;++i){float v=noise()*amp;if(i>=notch)v-=.45f*delay_[i-notch];delay_[i]=v;}envelope_=1;active_=true;}
float KarplusStrongString::process() noexcept{if(!active_||delay_.empty())return 0;const auto next=(index_+1)%delay_.size();const float current=delay_[index_],avg=.5f*(current+delay_[next]),filtered=brightness_*avg+(1-brightness_)*previous_;previous_=filtered;delay_[index_]=filtered*damping_;index_=next;envelope_*=.999985f;if(std::abs(current)<1e-5f&&envelope_<.02f)stop();return current*envelope_;}
void KarplusStrongString::stop() noexcept{active_=false;delay_.clear();index_=0;previous_=0;envelope_=0;}
void SoftLimiter::set_drive(float drive) noexcept{drive_=std::clamp(drive,.1f,8.f);} 
float SoftLimiter::process(float x) const noexcept{return std::tanh(x*drive_);} 
StereoBody::StereoBody(double sr){set_sample_rate(sr);} 
void StereoBody::set_sample_rate(double sr){sr_=std::clamp(sr,8000.0,384000.0);z1_l_=z1_r_=0;}
void StereoBody::set_size(float size) noexcept{size_=std::clamp(size,0.f,1.f);} 
void StereoBody::set_resonance(float r) noexcept{resonance_=std::clamp(r,0.f,.98f);} 
void StereoBody::process(float in,float& left,float& right) noexcept{const float c1=.12f+.30f*size_,c2=.18f+.24f*(1-size_);z1_l_=in*c1+z1_l_*(resonance_*(1-c1));z1_r_=in*c2+z1_r_*(resonance_*(1-c2));left=in*.72f+z1_l_*.46f;right=in*.72f+z1_r_*.46f;}
}
