export interface SynapseState {
  potential:number;
  activation:number;
  trace:number;
  weight:number;
  pendingCoupling:number;
  lastInput:number;
  lastOutput:number;
  thresholdOffset:number;
  tick:number;
}
export interface SynapseConfigInit {
  decay?:number;
  traceDecay?:number;
  threshold?:number;
  gain?:number;
  plasticity?:number;
  weightMin?:number;
  weightMax?:number;
  targetActivity?:number;
  homeostasis?:number;
}
export class SynapseConfig {
  constructor(value?:SynapseConfigInit);
  decay:number;traceDecay:number;threshold:number;gain:number;plasticity:number;
  weightMin:number;weightMax:number;targetActivity:number;homeostasis:number;
}
export class Synapse {
  constructor(config?:SynapseConfig|SynapseConfigInit);
  readonly config:SynapseConfig;
  readonly state:SynapseState;
  pulse(input:number,modulation?:number,dtSeconds?:number):number;
  step(input:number,modulation?:number,dtSeconds?:number):number;
  reinforce(reward:number):void;
  couple(sourceOutput:number,strength:number):void;
  reset():void;
  snapshot():SynapseState;
  restore(state:SynapseState|Record<string,number>):void;
  process(inputs:Iterable<number>,modulations?:readonly number[]|null,dtSeconds?:number):number[];
}
export function conformanceSequence():SynapseState;
