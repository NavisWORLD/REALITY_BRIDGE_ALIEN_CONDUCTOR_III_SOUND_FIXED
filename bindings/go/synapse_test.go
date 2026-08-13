package synapse

import "testing"

func TestConformance(t *testing.T){
	s:=New(nil); xs:=[]float64{0.25,0.8,-0.2,0.6,0,-0.4,0.9}; ms:=[]float64{0,0.1,0.2,-0.1,0.05,0,0.15}
	for i,x:=range xs{if i==2{s.Couple(0.35,0.4)}; s.Pulse(x,ms[i],0.01); if i==3{s.Reinforce(0.7)}; if i==5{s.Reinforce(-0.2)}}
	e:=State{Potential:0.038840176720408945,Activation:-0.11044113874970204,Trace:-0.008475792084489108,Weight:0.9998629394170829,ThresholdOffset:-0.00031425539024381897,LastOutput:-0.11044113874970204,Tick:7}
	if abs(s.State.Potential-e.Potential)>1e-12||abs(s.State.Activation-e.Activation)>1e-12||abs(s.State.Trace-e.Trace)>1e-12||abs(s.State.Weight-e.Weight)>1e-12||abs(s.State.ThresholdOffset-e.ThresholdOffset)>1e-12||s.State.Tick!=e.Tick{t.Fatalf("conformance mismatch: %+v",s.State)}
}
func abs(v float64)float64{if v<0{return -v};return v}
