#pragma once
#include <stddef.h>
#ifdef _WIN32
 #ifdef RB_BUILD_SHARED
  #define RB_API __declspec(dllexport)
 #else
  #define RB_API __declspec(dllimport)
 #endif
#else
 #define RB_API __attribute__((visibility("default")))
#endif
#ifdef __cplusplus
extern "C" {
#endif
typedef struct rb_string rb_string;
RB_API rb_string* rb_string_create(double sample_rate);
RB_API void rb_string_destroy(rb_string* s);
RB_API void rb_string_pluck(rb_string* s,double hz,double force,double damping,double brightness,double pick_position);
RB_API float rb_string_process(rb_string* s);
RB_API void rb_string_stop(rb_string* s);
RB_API double rb_midi_to_hz(double midi,double a4);
RB_API double rb_hz_to_midi(double hz,double a4);
RB_API float rb_soft_limit(float sample,float drive);
#ifdef __cplusplus
}
#endif
