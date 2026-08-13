"""Portable software signal state with trace memory, coupling, and reward updates.

The terminology is biologically inspired naming for a deterministic software
state machine. It does not model a biological synapse or consciousness.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
import math
from typing import Iterable, Mapping, Sequence

SYNAPSE_VERSION = 1

def _finite(value: float, fallback: float) -> float:
    value=float(value)
    return value if math.isfinite(value) else fallback

def _clamp(value: float, low: float, high: float) -> float:
    return max(low,min(high,value))

@dataclass(slots=True)
class SynapseConfig:
    decay:float=2.0
    trace_decay:float=1.0
    threshold:float=0.15
    gain:float=1.0
    plasticity:float=0.05
    weight_min:float=0.10
    weight_max:float=2.0
    target_activity:float=0.35
    homeostasis:float=0.02

    def normalized(self)->"SynapseConfig":
        weight_min=_clamp(_finite(self.weight_min,0.10),0.001,10.0)
        return SynapseConfig(
            decay=_clamp(_finite(self.decay,2.0),0.0,100.0),
            trace_decay=_clamp(_finite(self.trace_decay,1.0),0.0,100.0),
            threshold=_clamp(_finite(self.threshold,0.15),-4.0,4.0),
            gain=_clamp(_finite(self.gain,1.0),0.0,16.0),
            plasticity=_clamp(_finite(self.plasticity,0.05),0.0,1.0),
            weight_min=weight_min,
            weight_max=_clamp(_finite(self.weight_max,2.0),weight_min,10.0),
            target_activity=_clamp(_finite(self.target_activity,0.35),0.0,1.0),
            homeostasis=_clamp(_finite(self.homeostasis,0.02),0.0,10.0),
        )

@dataclass(slots=True)
class SynapseState:
    potential:float=0.0
    activation:float=0.0
    trace:float=0.0
    weight:float=1.0
    pending_coupling:float=0.0
    last_input:float=0.0
    last_output:float=0.0
    threshold_offset:float=0.0
    tick:int=0
    def to_dict(self)->dict[str,float|int]: return asdict(self)

class Synapse:
    def __init__(self,config:SynapseConfig|None=None):
        self.config=(config or SynapseConfig()).normalized()
        self._state=SynapseState(weight=_clamp(1.0,self.config.weight_min,self.config.weight_max))

    @property
    def state(self)->SynapseState: return SynapseState(**self._state.to_dict())

    def pulse(self,input_value:float,modulation:float=0.0,dt_seconds:float=0.01)->float:
        dt=_clamp(_finite(dt_seconds,0.01),1.0e-6,1.0)
        x=_clamp(_finite(input_value,0.0),-4.0,4.0)
        m=_clamp(_finite(modulation,0.0),-4.0,4.0)
        p_decay=math.exp(-self.config.decay*dt)
        t_decay=math.exp(-self.config.trace_decay*dt)
        effective_threshold=self.config.threshold+self._state.threshold_offset
        drive=x*self._state.weight+self._state.pending_coupling+m*self._state.trace
        self._state.potential=self._state.potential*p_decay+drive*(1.0-p_decay)
        self._state.activation=math.tanh(self.config.gain*(self._state.potential-effective_threshold))
        self._state.trace=self._state.trace*t_decay+self._state.activation*(1.0-t_decay)
        self._state.threshold_offset=_clamp(self._state.threshold_offset+self.config.homeostasis*(abs(self._state.activation)-self.config.target_activity)*dt,-2.0,2.0)
        self._state.pending_coupling=0.0
        self._state.last_input=x
        self._state.last_output=self._state.activation
        self._state.tick+=1
        return self._state.last_output

    step=pulse

    def reinforce(self,reward:float)->None:
        r=_clamp(_finite(reward,0.0),-1.0,1.0)
        delta=self.config.plasticity*r*self._state.trace*self._state.last_input
        self._state.weight=_clamp(self._state.weight+delta,self.config.weight_min,self.config.weight_max)

    def couple(self,source_output:float,strength:float)->None:
        source=_clamp(_finite(source_output,0.0),-1.0,1.0)
        amount=_clamp(_finite(strength,0.0),-2.0,2.0)
        self._state.pending_coupling=_clamp(self._state.pending_coupling+source*amount,-4.0,4.0)

    def reset(self)->None:
        self._state=SynapseState(weight=_clamp(1.0,self.config.weight_min,self.config.weight_max))

    def snapshot(self)->dict[str,float|int]: return self._state.to_dict()

    def restore(self,state:SynapseState|Mapping[str,float|int])->None:
        incoming=state if isinstance(state,SynapseState) else SynapseState(**dict(state))
        self._state=SynapseState(
            potential=_clamp(_finite(incoming.potential,0.0),-16.0,16.0),
            activation=_clamp(_finite(incoming.activation,0.0),-1.0,1.0),
            trace=_clamp(_finite(incoming.trace,0.0),-1.0,1.0),
            weight=_clamp(_finite(incoming.weight,1.0),self.config.weight_min,self.config.weight_max),
            pending_coupling=_clamp(_finite(incoming.pending_coupling,0.0),-4.0,4.0),
            last_input=_clamp(_finite(incoming.last_input,0.0),-4.0,4.0),
            last_output=_clamp(_finite(incoming.last_output,0.0),-1.0,1.0),
            threshold_offset=_clamp(_finite(incoming.threshold_offset,0.0),-2.0,2.0),
            tick=max(0,int(incoming.tick)),
        )

    def process(self,inputs:Iterable[float],modulations:Sequence[float]|None=None,dt_seconds:float=0.01)->list[float]:
        return [self.pulse(x,modulations[i] if modulations is not None and i<len(modulations) else 0.0,dt_seconds) for i,x in enumerate(inputs)]

def conformance_sequence()->SynapseState:
    s=Synapse()
    inputs=[0.25,0.8,-0.2,0.6,0.0,-0.4,0.9]
    mods=[0.0,0.1,0.2,-0.1,0.05,0.0,0.15]
    for i,(x,m) in enumerate(zip(inputs,mods)):
        if i==2:s.couple(0.35,0.4)
        s.pulse(x,m,0.01)
        if i==3:s.reinforce(0.7)
        if i==5:s.reinforce(-0.2)
    return s.state
