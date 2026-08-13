using System;
using System.Collections.Generic;

namespace RealityBridge.Synaptic;

public sealed class SynapseConfig {
    public double Decay { get; init; } = 2.0;
    public double TraceDecay { get; init; } = 1.0;
    public double Threshold { get; init; } = 0.15;
    public double Gain { get; init; } = 1.0;
    public double Plasticity { get; init; } = 0.05;
    public double WeightMin { get; init; } = 0.10;
    public double WeightMax { get; init; } = 2.0;
    public double TargetActivity { get; init; } = 0.35;
    public double Homeostasis { get; init; } = 0.02;
}

public struct SynapseState {
    public double Potential, Activation, Trace, Weight;
    public double PendingCoupling, LastInput, LastOutput, ThresholdOffset;
    public ulong Tick;
}

public sealed class Synapse {
    public SynapseConfig Config { get; }
    public SynapseState State { get; private set; }

    static double Finite(double v,double fallback)=>double.IsFinite(v)?v:fallback;
    static double Clamp(double v,double lo,double hi)=>Math.Max(lo,Math.Min(hi,v));

    public Synapse(SynapseConfig? config=null){
        var c=config??new SynapseConfig();
        var min=Clamp(Finite(c.WeightMin,0.1),0.001,10);
        Config=new SynapseConfig{
            Decay=Clamp(Finite(c.Decay,2),0,100),TraceDecay=Clamp(Finite(c.TraceDecay,1),0,100),
            Threshold=Clamp(Finite(c.Threshold,0.15),-4,4),Gain=Clamp(Finite(c.Gain,1),0,16),
            Plasticity=Clamp(Finite(c.Plasticity,0.05),0,1),WeightMin=min,
            WeightMax=Clamp(Finite(c.WeightMax,2),min,10),TargetActivity=Clamp(Finite(c.TargetActivity,0.35),0,1),
            Homeostasis=Clamp(Finite(c.Homeostasis,0.02),0,10)};
        Reset();
    }

    public double Pulse(double input,double modulation=0,double dtSeconds=0.01){
        var dt=Clamp(Finite(dtSeconds,0.01),1e-6,1);var x=Clamp(Finite(input,0),-4,4);var m=Clamp(Finite(modulation,0),-4,4);
        var pd=Math.Exp(-Config.Decay*dt);var td=Math.Exp(-Config.TraceDecay*dt);
        var s=State;var drive=x*s.Weight+s.PendingCoupling+m*s.Trace;var threshold=Config.Threshold+s.ThresholdOffset;
        s.Potential=s.Potential*pd+drive*(1-pd);s.Activation=Math.Tanh(Config.Gain*(s.Potential-threshold));
        s.Trace=s.Trace*td+s.Activation*(1-td);s.ThresholdOffset=Clamp(s.ThresholdOffset+Config.Homeostasis*(Math.Abs(s.Activation)-Config.TargetActivity)*dt,-2,2);
        s.PendingCoupling=0;s.LastInput=x;s.LastOutput=s.Activation;s.Tick++;State=s;return s.LastOutput;
    }
    public double Step(double input,double modulation=0,double dtSeconds=0.01)=>Pulse(input,modulation,dtSeconds);
    public void Reinforce(double reward){var s=State;var r=Clamp(Finite(reward,0),-1,1);s.Weight=Clamp(s.Weight+Config.Plasticity*r*s.Trace*s.LastInput,Config.WeightMin,Config.WeightMax);State=s;}
    public void Couple(double sourceOutput,double strength){var s=State;s.PendingCoupling=Clamp(s.PendingCoupling+Clamp(Finite(sourceOutput,0),-1,1)*Clamp(Finite(strength,0),-2,2),-4,4);State=s;}
    public void Reset()=>State=new SynapseState{Weight=Clamp(1,Config.WeightMin,Config.WeightMax)};
    public SynapseState Snapshot()=>State;
    public void Restore(SynapseState s){s.Potential=Clamp(Finite(s.Potential,0),-16,16);s.Activation=Clamp(Finite(s.Activation,0),-1,1);s.Trace=Clamp(Finite(s.Trace,0),-1,1);s.Weight=Clamp(Finite(s.Weight,1),Config.WeightMin,Config.WeightMax);s.PendingCoupling=Clamp(Finite(s.PendingCoupling,0),-4,4);s.LastInput=Clamp(Finite(s.LastInput,0),-4,4);s.LastOutput=Clamp(Finite(s.LastOutput,0),-1,1);s.ThresholdOffset=Clamp(Finite(s.ThresholdOffset,0),-2,2);State=s;}
    public double[] Process(IEnumerable<double> inputs,IReadOnlyList<double>? modulations=null,double dtSeconds=0.01){var output=new List<double>();var i=0;foreach(var x in inputs){output.Add(Pulse(x,modulations is not null&&i<modulations.Count?modulations[i]:0,dtSeconds));i++;}return output.ToArray();}
}
