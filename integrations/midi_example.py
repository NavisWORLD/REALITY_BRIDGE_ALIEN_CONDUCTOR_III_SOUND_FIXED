from reality_bridge import AccompanimentEngine,VoiceDNA,midi_to_hz
from reality_bridge.engine import serialize_events
engine=AccompanimentEngine(667)
for i,n in enumerate([60,64,67,69,67,64]):engine.observe_voice(VoiceDNA(midi_to_hz(n),.9,.65,.5,.55,.85,True,i*.45))
for event in serialize_events(engine.plan_bar()):print(event)
