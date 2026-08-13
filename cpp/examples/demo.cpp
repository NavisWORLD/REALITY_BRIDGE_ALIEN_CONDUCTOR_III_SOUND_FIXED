#include "reality_bridge/dsp.hpp"
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <vector>
static void u16(std::ofstream& f,std::uint16_t v){f.write(reinterpret_cast<char*>(&v),2);}static void u32(std::ofstream& f,std::uint32_t v){f.write(reinterpret_cast<char*>(&v),4);}
int main(){constexpr int sr=48000,seconds=3;const int frames=sr*seconds;reality_bridge::KarplusStrongString s(sr);reality_bridge::StereoBody body(sr);reality_bridge::SoftLimiter lim;s.pluck(110,.82,.996,.72,.19);std::vector<std::int16_t> pcm;pcm.reserve(frames*2);for(int i=0;i<frames;++i){if(i==sr)s.pluck(146.83,.75,.995,.62,.28);if(i==sr*2)s.pluck(196,.72,.994,.78,.14);float l,r;body.process(s.process(),l,r);l=lim.process(l*.55f);r=lim.process(r*.55f);pcm.push_back((std::int16_t)(std::max(-1.f,std::min(1.f,l))*32767));pcm.push_back((std::int16_t)(std::max(-1.f,std::min(1.f,r))*32767));}std::ofstream f("reality_bridge_demo.wav",std::ios::binary);const std::uint32_t bytes=pcm.size()*2;f.write("RIFF",4);u32(f,36+bytes);f.write("WAVEfmt ",8);u32(f,16);u16(f,1);u16(f,2);u32(f,sr);u32(f,sr*4);u16(f,4);u16(f,16);f.write("data",4);u32(f,bytes);f.write((char*)pcm.data(),bytes);std::cout<<"wrote reality_bridge_demo.wav\n";}
