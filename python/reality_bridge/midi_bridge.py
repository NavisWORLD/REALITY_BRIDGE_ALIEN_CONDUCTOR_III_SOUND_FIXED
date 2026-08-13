"""MIDI bridge. Requires optional packages: mido + python-rtmidi."""
from __future__ import annotations
import time
from .engine import AccompanimentEngine

def _mido():
    try:
        import mido;return mido
    except ImportError as e:raise RuntimeError("Install MIDI support: pip install 'reality-bridge[midi]'") from e

def list_ports():
    mido=_mido();return {"inputs":mido.get_input_names(),"outputs":mido.get_output_names()}

def run_bridge(output=None,bpm=96.0,bars=None):
    mido=_mido();ports=mido.get_output_names()
    if not ports:raise RuntimeError("No MIDI output ports found")
    name=output or ports[0];engine=AccompanimentEngine(42);engine.state.bpm=bpm
    from .engine import HarmonicHypothesis
    engine.state.harmonic=HarmonicHypothesis(0,"major",0,"maj",1.0,1.0);beat=60./bpm;bar=0
    with mido.open_output(name) as out:
        while bars is None or bar<bars:
            events=engine.plan_bar()
            for ev in events:out.send(mido.Message('note_on',note=ev.note,velocity=ev.velocity,channel=ev.channel))
            time.sleep(beat*4)
            for ev in events:out.send(mido.Message('note_off',note=ev.note,velocity=0,channel=ev.channel))
            bar+=1
