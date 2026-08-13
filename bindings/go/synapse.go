package synapse

import "math"

type Config struct {
	Decay, TraceDecay, Threshold, Gain float64
	Plasticity, WeightMin, WeightMax float64
	TargetActivity, Homeostasis float64
}

type State struct {
	Potential, Activation, Trace, Weight float64
	PendingCoupling, LastInput, LastOutput float64
	ThresholdOffset float64
	Tick uint64
}

type Synapse struct { Config Config; State State }

func DefaultConfig() Config { return Config{2,1,0.15,1,0.05,0.10,2,0.35,0.02} }
func clamp(v,lo,hi float64) float64 { if math.IsNaN(v)||math.IsInf(v,0){return lo}; if v<lo{return lo}; if v>hi{return hi}; return v }
func finite(v,f float64) float64 { if math.IsNaN(v)||math.IsInf(v,0){return f}; return v }
func normalize(c Config) Config { c.Decay=clamp(finite(c.Decay,2),0,100); c.TraceDecay=clamp(finite(c.TraceDecay,1),0,100); c.Threshold=clamp(finite(c.Threshold,0.15),-4,4); c.Gain=clamp(finite(c.Gain,1),0,16); c.Plasticity=clamp(finite(c.Plasticity,0.05),0,1); c.WeightMin=clamp(finite(c.WeightMin,0.1),0.001,10); c.WeightMax=clamp(finite(c.WeightMax,2),c.WeightMin,10); c.TargetActivity=clamp(finite(c.TargetActivity,0.35),0,1); c.Homeostasis=clamp(finite(c.Homeostasis,0.02),0,10); return c }
func New(config *Config) *Synapse { c:=DefaultConfig(); if config!=nil{c=*config}; c=normalize(c); s:=&Synapse{Config:c}; s.Reset(); return s }
func (s *Synapse) Reset(){s.State=State{Weight:clamp(1,s.Config.WeightMin,s.Config.WeightMax)}}
func (s *Synapse) Pulse(input,modulation,dt float64) float64 { dt=clamp(finite(dt,0.01),1e-6,1); x:=clamp(finite(input,0),-4,4); m:=clamp(finite(modulation,0),-4,4); pd:=math.Exp(-s.Config.Decay*dt); td:=math.Exp(-s.Config.TraceDecay*dt); drive:=x*s.State.Weight+s.State.PendingCoupling+m*s.State.Trace; threshold:=s.Config.Threshold+s.State.ThresholdOffset; s.State.Potential=s.State.Potential*pd+drive*(1-pd); s.State.Activation=math.Tanh(s.Config.Gain*(s.State.Potential-threshold)); s.State.Trace=s.State.Trace*td+s.State.Activation*(1-td); s.State.ThresholdOffset=clamp(s.State.ThresholdOffset+s.Config.Homeostasis*(math.Abs(s.State.Activation)-s.Config.TargetActivity)*dt,-2,2); s.State.PendingCoupling=0; s.State.LastInput=x; s.State.LastOutput=s.State.Activation; s.State.Tick++; return s.State.LastOutput }
func (s *Synapse) Step(input,modulation,dt float64) float64 { return s.Pulse(input,modulation,dt) }
func (s *Synapse) Reinforce(reward float64){r:=clamp(finite(reward,0),-1,1); s.State.Weight=clamp(s.State.Weight+s.Config.Plasticity*r*s.State.Trace*s.State.LastInput,s.Config.WeightMin,s.Config.WeightMax)}
func (s *Synapse) Couple(source,strength float64){source=clamp(finite(source,0),-1,1); strength=clamp(finite(strength,0),-2,2); s.State.PendingCoupling=clamp(s.State.PendingCoupling+source*strength,-4,4)}
func (s *Synapse) Snapshot() State{return s.State}
func (s *Synapse) Restore(st State){st.Potential=clamp(finite(st.Potential,0),-16,16); st.Activation=clamp(finite(st.Activation,0),-1,1); st.Trace=clamp(finite(st.Trace,0),-1,1); st.Weight=clamp(finite(st.Weight,1),s.Config.WeightMin,s.Config.WeightMax); st.PendingCoupling=clamp(finite(st.PendingCoupling,0),-4,4); st.LastInput=clamp(finite(st.LastInput,0),-4,4); st.LastOutput=clamp(finite(st.LastOutput,0),-1,1); st.ThresholdOffset=clamp(finite(st.ThresholdOffset,0),-2,2); s.State=st}
