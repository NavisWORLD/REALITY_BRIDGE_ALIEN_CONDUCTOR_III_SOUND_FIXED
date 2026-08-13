#include "reality_bridge/c_api.h"
#include "reality_bridge/dsp.hpp"
#include <new>
struct rb_string{reality_bridge::KarplusStrongString impl;explicit rb_string(double sr):impl(sr){}};
extern "C" {
rb_string* rb_string_create(double sr){try{return new rb_string(sr);}catch(...){return nullptr;}}
void rb_string_destroy(rb_string* s){delete s;}
void rb_string_pluck(rb_string* s,double hz,double force,double damping,double brightness,double pick){if(s)s->impl.pluck(hz,force,damping,brightness,pick);}
float rb_string_process(rb_string* s){return s?s->impl.process():0.f;}
void rb_string_stop(rb_string* s){if(s)s->impl.stop();}
double rb_midi_to_hz(double midi,double a4){return reality_bridge::midi_to_hz(midi,a4);}
double rb_hz_to_midi(double hz,double a4){try{return reality_bridge::hz_to_midi(hz,a4);}catch(...){return 0.;}}
float rb_soft_limit(float sample,float drive){reality_bridge::SoftLimiter l;l.set_drive(drive);return l.process(sample);}
}
