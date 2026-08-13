const clamp=(v,lo,hi)=>Math.max(lo,Math.min(hi,Number.isFinite(v)?v:0));
const finite=(v,f)=>Number.isFinite(Number(v))?Number(v):f;

export class SynapseConfig{
  constructor(v={}){
    const wmin=clamp(finite(v.weightMin,0.10),0.001,10);
    this.decay=clamp(finite(v.decay,2),0,100);
    this.traceDecay=clamp(finite(v.traceDecay,1),0,100);
    this.threshold=clamp(finite(v.threshold,0.15),-4,4);
    this.gain=clamp(finite(v.gain,1),0,16);
    this.plasticity=clamp(finite(v.plasticity,0.05),0,1);
    this.weightMin=wmin;
    this.weightMax=clamp(finite(v.weightMax,2),wmin,10);
    this.targetActivity=clamp(finite(v.targetActivity,0.35),0,1);
    this.homeostasis=clamp(finite(v.homeostasis,0.02),0,10);
  }
}

const freshState=(weight=1)=>({potential:0,activation:0,trace:0,weight,pendingCoupling:0,lastInput:0,lastOutput:0,thresholdOffset:0,tick:0});

export class Synapse{
  constructor(config=new SynapseConfig()){
    this.config=config instanceof SynapseConfig?config:new SynapseConfig(config);
    this._state=freshState(clamp(1,this.config.weightMin,this.config.weightMax));
  }
  get state(){return {...this._state};}
  pulse(input,modulation=0,dtSeconds=0.01){
    const dt=clamp(finite(dtSeconds,0.01),1e-6,1);
    const x=clamp(finite(input,0),-4,4),m=clamp(finite(modulation,0),-4,4);
    const pd=Math.exp(-this.config.decay*dt),td=Math.exp(-this.config.traceDecay*dt);
    const drive=x*this._state.weight+this._state.pendingCoupling+m*this._state.trace;
    const threshold=this.config.threshold+this._state.thresholdOffset;
    this._state.potential=this._state.potential*pd+drive*(1-pd);
    this._state.activation=Math.tanh(this.config.gain*(this._state.potential-threshold));
    this._state.trace=this._state.trace*td+this._state.activation*(1-td);
    this._state.thresholdOffset=clamp(this._state.thresholdOffset+this.config.homeostasis*(Math.abs(this._state.activation)-this.config.targetActivity)*dt,-2,2);
    this._state.pendingCoupling=0;this._state.lastInput=x;this._state.lastOutput=this._state.activation;this._state.tick++;
    return this._state.lastOutput;
  }
  step(input,modulation=0,dtSeconds=0.01){return this.pulse(input,modulation,dtSeconds);}
  reinforce(reward){
    const r=clamp(finite(reward,0),-1,1);
    this._state.weight=clamp(this._state.weight+this.config.plasticity*r*this._state.trace*this._state.lastInput,this.config.weightMin,this.config.weightMax);
  }
  couple(sourceOutput,strength){
    const source=clamp(finite(sourceOutput,0),-1,1),amount=clamp(finite(strength,0),-2,2);
    this._state.pendingCoupling=clamp(this._state.pendingCoupling+source*amount,-4,4);
  }
  reset(){this._state=freshState(clamp(1,this.config.weightMin,this.config.weightMax));}
  snapshot(){return this.state;}
  restore(s){
    this._state={potential:clamp(finite(s.potential,0),-16,16),activation:clamp(finite(s.activation,0),-1,1),trace:clamp(finite(s.trace,0),-1,1),weight:clamp(finite(s.weight,1),this.config.weightMin,this.config.weightMax),pendingCoupling:clamp(finite(s.pendingCoupling??s.pending_coupling,0),-4,4),lastInput:clamp(finite(s.lastInput??s.last_input,0),-4,4),lastOutput:clamp(finite(s.lastOutput??s.last_output,0),-1,1),thresholdOffset:clamp(finite(s.thresholdOffset??s.threshold_offset,0),-2,2),tick:Math.max(0,Math.trunc(finite(s.tick,0)))};
  }
  process(inputs,modulations=null,dtSeconds=0.01){return Array.from(inputs,(x,i)=>this.pulse(x,modulations?.[i]??0,dtSeconds));}
}

export function conformanceSequence(){
  const s=new Synapse(),xs=[0.25,0.8,-0.2,0.6,0,-0.4,0.9],ms=[0,0.1,0.2,-0.1,0.05,0,0.15];
  xs.forEach((x,i)=>{if(i===2)s.couple(0.35,0.4);s.pulse(x,ms[i],0.01);if(i===3)s.reinforce(0.7);if(i===5)s.reinforce(-0.2);});
  return s.state;
}
