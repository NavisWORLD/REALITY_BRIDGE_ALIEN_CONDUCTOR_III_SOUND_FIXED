#pragma once
#include <stddef.h>
#include <stdint.h>
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

#define RB_SYNAPSE_ABI_VERSION 1u

typedef struct rb_synapse rb_synapse;

typedef struct rb_synapse_config {
    uint32_t abi_version;
    uint32_t struct_size;
    double decay;
    double trace_decay;
    double threshold;
    double gain;
    double plasticity;
    double weight_min;
    double weight_max;
    double target_activity;
    double homeostasis;
} rb_synapse_config;

typedef struct rb_synapse_state {
    uint32_t abi_version;
    uint32_t struct_size;
    double potential;
    double activation;
    double trace;
    double weight;
    double pending_coupling;
    double last_input;
    double last_output;
    double threshold_offset;
    uint64_t tick;
} rb_synapse_state;

RB_API uint32_t rb_synapse_abi_version(void);
RB_API void rb_synapse_config_default(rb_synapse_config* out_config);
RB_API rb_synapse* rb_synapse_create(const rb_synapse_config* config);
RB_API rb_synapse* rb_synapse_create_default(void);
RB_API void rb_synapse_destroy(rb_synapse* synapse);
RB_API double rb_synapse_pulse(rb_synapse* synapse,double input,double modulation,double dt_seconds);
RB_API double rb_synapse_step(rb_synapse* synapse,double input,double modulation,double dt_seconds);
RB_API void rb_synapse_reinforce(rb_synapse* synapse,double reward);
RB_API void rb_synapse_couple(rb_synapse* synapse,double source_output,double strength);
RB_API void rb_synapse_reset(rb_synapse* synapse);
RB_API int rb_synapse_get_state(const rb_synapse* synapse,rb_synapse_state* out_state);
RB_API int rb_synapse_set_state(rb_synapse* synapse,const rb_synapse_state* state);
RB_API size_t rb_synapse_process(rb_synapse* synapse,const double* inputs,const double* modulations,size_t count,double dt_seconds,double* outputs);

#ifdef __cplusplus
}
#endif
