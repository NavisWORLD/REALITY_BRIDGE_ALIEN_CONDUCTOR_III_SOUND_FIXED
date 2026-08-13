import {conformanceSequence,Synapse} from './synapse.mjs';
const expected={potential:0.038840176720408945,activation:-0.11044113874970204,trace:-0.008475792084489108,weight:0.9998629394170829,thresholdOffset:-0.00031425539024381897,lastOutput:-0.11044113874970204,tick:7};
const got=conformanceSequence();
for(const [k,v] of Object.entries(expected)){
  const delta=Math.abs(got[k]-v);
  if(delta>1e-12)throw new Error(`${k}: ${got[k]} != ${v}; delta=${delta}`);
}
const s=new Synapse();
if(s.process([0.1,0.2]).length!==2)throw new Error('batch processing failed');
console.log('JavaScript Synaptic Core conformance: OK');
