#ifndef REALITY_BRIDGE_SYNAPSE_H
#define REALITY_BRIDGE_SYNAPSE_H
#include <math.h>
#include <stdint.h>

typedef struct rb_synapse_config_v1{double decay,trace_decay,threshold,gain,plasticity,weight_min,weight_max,target_activity,homeostasis;} rb_synapse_config_v1;
typedef struct rb_synapse_state_v1{double potential,activation,trace,weight,pending_coupling,last_input,last_output,threshold_offset;uint64_t tick;} rb_synapse_state_v1;
typedef struct rb_synapse_v1{rb_synapse_config_v1 config;rb_synapse_state_v1 state;} rb_synapse_v1;

static inline double rb_synapse_finite(double v,double f){return isfinite(v)?v:f;}
static inline double rb_synapse_clamp(double v,double lo,double hi){return v<lo?lo:(v>hi?hi:v);}
static inline rb_synapse_config_v1 rb_synapse_default_config_v1(void){rb_synapse_config_v1 c={2.0,1.0,0.15,1.0,0.05,0.10,2.0,0.35,0.02};return c;}
static inline rb_synapse_v1 rb_synapse_make_v1(rb_synapse_config_v1 c){c.decay=rb_synapse_clamp(rb_synapse_finite(c.decay,2.0),0,100);c.trace_decay=rb_synapse_clamp(rb_synapse_finite(c.trace_decay,1.0),0,100);c.threshold=rb_synapse_clamp(rb_synapse_finite(c.threshold,0.15),-4,4);c.gain=rb_synapse_clamp(rb_synapse_finite(c.gain,1.0),0,16);c.plasticity=rb_synapse_clamp(rb_synapse_finite(c.plasticity,0.05),0,1);c.weight_min=rb_synapse_clamp(rb_synapse_finite(c.weight_min,0.1),0.001,10);c.weight_max=rb_synapse_clamp(rb_synapse_finite(c.weight_max,2.0),c.weight_min,10);c.target_activity=rb_synapse_clamp(rb_synapse_finite(c.target_activity,0.35),0,1);c.homeostasis=rb_synapse_clamp(rb_synapse_finite(c.homeostasis,0.02),0,10);rb_synapse_v1 s={0};s.config=c;s.state.weight=rb_synapse_clamp(1.0,c.weight_min,c.weight_max);return s;}
static inline double rb_synapse_pulse_v1(rb_synapse_v1* s,double input,double modulation,double dt){dt=rb_synapse_clamp(rb_synapse_finite(dt,0.01),1e-6,1);input=rb_synapse_clamp(rb_synapse_finite(input,0),-4,4);modulation=rb_synapse_clamp(rb_synapse_finite(modulation,0),-4,4);double pd=exp(-s->config.decay*dt),td=exp(-s->config.trace_decay*dt),drive=input*s->state.weight+s->state.pending_coupling+modulation*s->state.trace,th=s->config.threshold+s->state.threshold_offset;s->state.potential=s->state.potential*pd+drive*(1-pd);s->state.activation=tanh(s->config.gain*(s->state.potential-th));s->state.trace=s->state.trace*td+s->state.activation*(1-td);s->state.threshold_offset=rb_synapse_clamp(s->state.threshold_offset+s->config.homeostasis*(fabs(s->state.activation)-s->config.target_activity)*dt,-2,2);s->state.pending_coupling=0;s->state.last_input=input;s->state.last_output=s->state.activation;s->state.tick++;return s->state.last_output;}
static inline void rb_synapse_reinforce_v1(rb_synapse_v1* s,double reward){reward=rb_synapse_clamp(rb_synapse_finite(reward,0),-1,1);s->state.weight=rb_synapse_clamp(s->state.weight+s->config.plasticity*reward*s->state.trace*s->state.last_input,s->config.weight_min,s->config.weight_max);}
static inline void rb_synapse_couple_v1(rb_synapse_v1* s,double source,double strength){source=rb_synapse_clamp(rb_synapse_finite(source,0),-1,1);strength=rb_synapse_clamp(rb_synapse_finite(strength,0),-2,2);s->state.pending_coupling=rb_synapse_clamp(s->state.pending_coupling+source*strength,-4,4);}
static inline void rb_synapse_reset_v1(rb_synapse_v1* s){rb_synapse_config_v1 c=s->config;*s=rb_synapse_make_v1(c);}
#endif
