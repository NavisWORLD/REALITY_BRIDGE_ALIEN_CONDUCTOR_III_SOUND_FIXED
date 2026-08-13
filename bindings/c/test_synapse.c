#include "synapse.h"
#include <math.h>
#include <stdio.h>

int main(void){
    rb_synapse_v1 s=rb_synapse_make_v1(rb_synapse_default_config_v1());
    const double xs[]={0.25,0.8,-0.2,0.6,0.0,-0.4,0.9};
    const double ms[]={0.0,0.1,0.2,-0.1,0.05,0.0,0.15};
    for(int i=0;i<7;i++){
        if(i==2)rb_synapse_couple_v1(&s,0.35,0.4);
        rb_synapse_pulse_v1(&s,xs[i],ms[i],0.01);
        if(i==3)rb_synapse_reinforce_v1(&s,0.7);
        if(i==5)rb_synapse_reinforce_v1(&s,-0.2);
    }
    const double expected=0.038840176720408945;
    if(fabs(s.state.potential-expected)>1e-12)return 1;
    if(s.state.tick!=7)return 2;
    puts("C Synaptic Core conformance: OK");
    return 0;
}
