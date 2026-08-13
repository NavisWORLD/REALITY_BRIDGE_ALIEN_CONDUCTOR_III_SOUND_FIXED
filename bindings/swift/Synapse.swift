import Foundation

public struct SynapseConfig {
    public var decay=2.0, traceDecay=1.0, threshold=0.15, gain=1.0
    public var plasticity=0.05, weightMin=0.10, weightMax=2.0
    public var targetActivity=0.35, homeostasis=0.02
    public init() {}
}

public struct SynapseState {
    public var potential=0.0, activation=0.0, trace=0.0, weight=1.0
    public var pendingCoupling=0.0, lastInput=0.0, lastOutput=0.0, thresholdOffset=0.0
    public var tick: UInt64=0
}

public final class Synapse {
    public let config: SynapseConfig
    public private(set) var state=SynapseState()
    private static func finite(_ v:Double,_ f:Double)->Double{v.isFinite ? v:f}
    private static func clamp(_ v:Double,_ lo:Double,_ hi:Double)->Double{min(hi,max(lo,v))}
    public init(config:SynapseConfig=SynapseConfig()){
        var c=config;let mn=Self.clamp(Self.finite(c.weightMin,0.1),0.001,10)
        c.decay=Self.clamp(Self.finite(c.decay,2),0,100);c.traceDecay=Self.clamp(Self.finite(c.traceDecay,1),0,100);c.threshold=Self.clamp(Self.finite(c.threshold,0.15),-4,4);c.gain=Self.clamp(Self.finite(c.gain,1),0,16);c.plasticity=Self.clamp(Self.finite(c.plasticity,0.05),0,1);c.weightMin=mn;c.weightMax=Self.clamp(Self.finite(c.weightMax,2),mn,10);c.targetActivity=Self.clamp(Self.finite(c.targetActivity,0.35),0,1);c.homeostasis=Self.clamp(Self.finite(c.homeostasis,0.02),0,10);self.config=c;reset()
    }
    @discardableResult public func pulse(_ input:Double,modulation:Double=0,dt:Double=0.01)->Double{
        let dt=Self.clamp(Self.finite(dt,0.01),1e-6,1),x=Self.clamp(Self.finite(input,0),-4,4),m=Self.clamp(Self.finite(modulation,0),-4,4),pd=exp(-config.decay*dt),td=exp(-config.traceDecay*dt),drive=x*state.weight+state.pendingCoupling+m*state.trace,th=config.threshold+state.thresholdOffset
        state.potential=state.potential*pd+drive*(1-pd);state.activation=tanh(config.gain*(state.potential-th));state.trace=state.trace*td+state.activation*(1-td);state.thresholdOffset=Self.clamp(state.thresholdOffset+config.homeostasis*(abs(state.activation)-config.targetActivity)*dt,-2,2);state.pendingCoupling=0;state.lastInput=x;state.lastOutput=state.activation;state.tick &+= 1;return state.lastOutput
    }
    public func step(_ input:Double,modulation:Double=0,dt:Double=0.01)->Double{pulse(input,modulation:modulation,dt:dt)}
    public func reinforce(_ reward:Double){let r=Self.clamp(Self.finite(reward,0),-1,1);state.weight=Self.clamp(state.weight+config.plasticity*r*state.trace*state.lastInput,config.weightMin,config.weightMax)}
    public func couple(_ source:Double,strength:Double){state.pendingCoupling=Self.clamp(state.pendingCoupling+Self.clamp(Self.finite(source,0),-1,1)*Self.clamp(Self.finite(strength,0),-2,2),-4,4)}
    public func reset(){state=SynapseState();state.weight=Self.clamp(1,config.weightMin,config.weightMax)}
    public func snapshot()->SynapseState{state}
    public func restore(_ incoming:SynapseState){var s=incoming;s.potential=Self.clamp(Self.finite(s.potential,0),-16,16);s.activation=Self.clamp(Self.finite(s.activation,0),-1,1);s.trace=Self.clamp(Self.finite(s.trace,0),-1,1);s.weight=Self.clamp(Self.finite(s.weight,1),config.weightMin,config.weightMax);s.pendingCoupling=Self.clamp(Self.finite(s.pendingCoupling,0),-4,4);s.lastInput=Self.clamp(Self.finite(s.lastInput,0),-4,4);s.lastOutput=Self.clamp(Self.finite(s.lastOutput,0),-1,1);s.thresholdOffset=Self.clamp(Self.finite(s.thresholdOffset,0),-2,2);state=s}
}
