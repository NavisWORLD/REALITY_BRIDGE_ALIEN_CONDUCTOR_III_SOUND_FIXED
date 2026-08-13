#include "reality_bridge/dsp.hpp"
#include <cassert>
#include <cmath>
#include <iostream>
int main(){for(double n:{36.,60.,69.,84.})assert(std::abs(reality_bridge::hz_to_midi(reality_bridge::midi_to_hz(n))-n)<1e-9);reality_bridge::KarplusStrongString s(48000);s.pluck(220,.8,.994,.7,.2);double energy=0;for(int i=0;i<4800;++i){float x=s.process();energy+=x*x;}assert(energy>1e-5);reality_bridge::SoftLimiter l;for(float x:{-10.f,-1.f,0.f,1.f,10.f})assert(std::abs(l.process(x))<=1.0001f);std::cout<<"Reality Bridge DSP tests passed\n";}
