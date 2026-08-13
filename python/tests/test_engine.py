from reality_bridge.engine import *

def test_frequency_roundtrip():
    for n in (36,60,69,84):assert abs(hz_to_midi(midi_to_hz(n))-n)<1e-9

def test_tracker_returns_hypothesis():
    t=HarmonyTracker()
    for i,n in enumerate((60,64,67,72,67,64,60)):t.observe(VoiceDNA(midi_to_hz(n),.95,.7,.4,.5,.9,True,i*.5))
    assert t.last is not None;assert t.last.root_pc==0;assert 0<=t.last.confidence<=1

def test_planner_is_valid_midi():
    e=AccompanimentEngine(4)
    for i,n in enumerate((60,64,67,64,60)):e.observe_voice(VoiceDNA(midi_to_hz(n),.9,.6,.3,.3,.8,True,i*.4))
    ev=e.plan_bar();assert ev;assert all(0<=x.note<=127 and 0<=x.velocity<=127 for x in ev)
