package realitybridge.synaptic;

public final class Synapse {
    public static final class Config {
        public double decay=2.0, traceDecay=1.0, threshold=0.15, gain=1.0;
        public double plasticity=0.05, weightMin=0.10, weightMax=2.0;
        public double targetActivity=0.35, homeostasis=0.02;
    }
    public static final class State {
        public double potential,activation,trace,weight=1.0,pendingCoupling,lastInput,lastOutput,thresholdOffset;
        public long tick;
        public State copy(){State s=new State();s.potential=potential;s.activation=activation;s.trace=trace;s.weight=weight;s.pendingCoupling=pendingCoupling;s.lastInput=lastInput;s.lastOutput=lastOutput;s.thresholdOffset=thresholdOffset;s.tick=tick;return s;}
    }
    public final Config config;
    private State state;
    private static double finite(double v,double f){return Double.isFinite(v)?v:f;}
    private static double clamp(double v,double lo,double hi){return Math.max(lo,Math.min(hi,v));}
    public Synapse(){this(new Config());}
    public Synapse(Config c){double min=clamp(finite(c.weightMin,0.1),0.001,10);config=new Config();config.decay=clamp(finite(c.decay,2),0,100);config.traceDecay=clamp(finite(c.traceDecay,1),0,100);config.threshold=clamp(finite(c.threshold,0.15),-4,4);config.gain=clamp(finite(c.gain,1),0,16);config.plasticity=clamp(finite(c.plasticity,0.05),0,1);config.weightMin=min;config.weightMax=clamp(finite(c.weightMax,2),min,10);config.targetActivity=clamp(finite(c.targetActivity,0.35),0,1);config.homeostasis=clamp(finite(c.homeostasis,0.02),0,10);reset();}
    public State state(){return state.copy();}
    public double pulse(double input){return pulse(input,0,0.01);}
    public double pulse(double input,double modulation,double dtSeconds){double dt=clamp(finite(dtSeconds,0.01),1e-6,1),x=clamp(finite(input,0),-4,4),m=clamp(finite(modulation,0),-4,4),pd=Math.exp(-config.decay*dt),td=Math.exp(-config.traceDecay*dt),drive=x*state.weight+state.pendingCoupling+m*state.trace,threshold=config.threshold+state.thresholdOffset;state.potential=state.potential*pd+drive*(1-pd);state.activation=Math.tanh(config.gain*(state.potential-threshold));state.trace=state.trace*td+state.activation*(1-td);state.thresholdOffset=clamp(state.thresholdOffset+config.homeostasis*(Math.abs(state.activation)-config.targetActivity)*dt,-2,2);state.pendingCoupling=0;state.lastInput=x;state.lastOutput=state.activation;state.tick++;return state.lastOutput;}
    public double step(double input,double modulation,double dtSeconds){return pulse(input,modulation,dtSeconds);}
    public void reinforce(double reward){double r=clamp(finite(reward,0),-1,1);state.weight=clamp(state.weight+config.plasticity*r*state.trace*state.lastInput,config.weightMin,config.weightMax);}
    public void couple(double sourceOutput,double strength){state.pendingCoupling=clamp(state.pendingCoupling+clamp(finite(sourceOutput,0),-1,1)*clamp(finite(strength,0),-2,2),-4,4);}
    public void reset(){state=new State();state.weight=clamp(1,config.weightMin,config.weightMax);}
    public void restore(State s){State n=s.copy();n.potential=clamp(finite(n.potential,0),-16,16);n.activation=clamp(finite(n.activation,0),-1,1);n.trace=clamp(finite(n.trace,0),-1,1);n.weight=clamp(finite(n.weight,1),config.weightMin,config.weightMax);n.pendingCoupling=clamp(finite(n.pendingCoupling,0),-4,4);n.lastInput=clamp(finite(n.lastInput,0),-4,4);n.lastOutput=clamp(finite(n.lastOutput,0),-1,1);n.thresholdOffset=clamp(finite(n.thresholdOffset,0),-2,2);n.tick=Math.max(0,n.tick);state=n;}
}
