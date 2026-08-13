#include "reality_bridge/synapse.hpp"
#include <cassert>
#include <cmath>

int main(){
    reality_bridge::Synapse s;
    const double first=s.pulse(0.8,0.1,0.01);
    assert(std::isfinite(first));
    assert(first>=-1.0&&first<=1.0);
    s.couple(0.5,0.4);
    const double coupled=s.pulse(0.2,0.0,0.01);
    assert(std::isfinite(coupled));
    const auto before=s.state();
    s.reinforce(0.75);
    const auto learned=s.state();
    assert(learned.weight>=s.config().weight_min);
    assert(learned.weight<=s.config().weight_max);
    s.reset();
    assert(s.state().tick==0);
    s.restore(before);
    assert(s.state().tick==before.tick);
    assert(std::abs(s.state().potential-before.potential)<1e-12);
    return 0;
}
