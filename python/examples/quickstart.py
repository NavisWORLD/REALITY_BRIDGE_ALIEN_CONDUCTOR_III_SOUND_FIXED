from reality_bridge import AccompanimentEngine, VoiceDNA
engine=AccompanimentEngine(seed=667)
engine.observe_voice(VoiceDNA(pitch_hz=220.0,pitch_confidence=0.92,energy=0.65,brightness=0.48,articulation=0.34,stability=0.81,onset=True,timestamp=0.0))
for event in engine.plan_bar(): print(event)
