#include "reality_bridge/synapse.hpp"
#include <iomanip>
#include <iostream>

int main(){
    reality_bridge::Synapse s;
    const double inputs[]={0.25,0.8,-0.2,0.6,0.0,-0.4,0.9};
    const double mods[]={0.0,0.1,0.2,-0.1,0.05,0.0,0.15};
    for(int i=0;i<7;++i){
        if(i==2) s.couple(0.35,0.4);
        s.pulse(inputs[i],mods[i],0.01);
        if(i==3) s.reinforce(0.7);
        if(i==5) s.reinforce(-0.2);
    }
    const auto& st=s.state();
    std::cout<<std::setprecision(17)
             <<st.potential<<' '<<st.activation<<' '<<st.trace<<' '
             <<st.weight<<' '<<st.threshold_offset<<' '<<st.last_output<<' '
             <<st.tick<<'\n';
    return 0;
}
