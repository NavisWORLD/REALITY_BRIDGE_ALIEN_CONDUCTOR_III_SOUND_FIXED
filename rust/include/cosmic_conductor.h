#pragma once
#ifdef _WIN32
 #ifdef COSMIC_CONDUCTOR_EXPORTS
  #define CC_API __declspec(dllexport)
 #else
  #define CC_API __declspec(dllimport)
 #endif
#else
 #define CC_API __attribute__((visibility("default")))
#endif
#ifdef __cplusplus
extern "C" {
#endif
CC_API double cc_midi_to_hz(double midi,double a4);
CC_API double cc_hz_to_midi(double hz,double a4);
CC_API float cc_soft_limit(float sample,float drive);
CC_API void* cc_string_create(double sample_rate);
CC_API void cc_string_destroy(void* voice);
CC_API void cc_string_pluck(void* voice,double hz,float force,float damping,float brightness,float pick_position);
CC_API float cc_string_process(void* voice);
CC_API void cc_string_stop(void* voice);
#ifdef __cplusplus
}
#endif
