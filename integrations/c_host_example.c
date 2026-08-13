#include "../rust/include/cosmic_conductor.h"
#include <stdio.h>
int main(void){ void* voice=cc_string_create(48000.0); if(!voice) return 1; cc_string_pluck(voice,cc_midi_to_hz(60.0,440.0),0.8f,0.7f,0.6f,0.25f); for(int i=0;i<16;++i) printf("%f\n",cc_string_process(voice)); cc_string_destroy(voice); return 0; }
