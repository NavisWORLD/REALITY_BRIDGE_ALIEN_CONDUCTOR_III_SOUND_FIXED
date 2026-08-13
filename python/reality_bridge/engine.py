"""Reality Bridge musical-state engine.

This module intentionally contains no audio-device dependency. It converts
observations (voice/media/MIDI) into deterministic musical state and note
suggestions that a host can render with Web Audio, a DAW, C++ DSP, or MIDI.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from collections import deque
import math
import random
from typing import Sequence

PITCH_NAMES=("C","C#","D","D#","E","F","F#","G","G#","A","A#","B")
MAJOR=(0,2,4,5,7,9,11)
NAT_MINOR=(0,2,3,5,7,8,10)
CHORD_QUALITIES={"maj":(0,4,7),"min":(0,3,7),"dim":(0,3,6),"sus2":(0,2,7),"sus4":(0,5,7),"maj7":(0,4,7,11),"min7":(0,3,7,10),"7":(0,4,7,10),"add9":(0,4,7,14)}

def midi_to_hz(note:float,a4:float=440.0)->float:return a4*(2.0**((note-69.0)/12.0))
def hz_to_midi(freq:float,a4:float=440.0)->float:
    if freq<=0:raise ValueError("frequency must be positive")
    return 69.0+12.0*math.log2(freq/a4)
def clamp(v,lo,hi):return lo if v<lo else hi if v>hi else v

@dataclass(slots=True)
class VoiceDNA:
    pitch_hz:float=0.0;pitch_confidence:float=0.0;energy:float=0.0;brightness:float=0.0;articulation:float=0.0;stability:float=0.0;onset:bool=False;timestamp:float=0.0
    @property
    def midi(self):return hz_to_midi(self.pitch_hz) if self.pitch_hz>0 else None
    @property
    def pitch_class(self):
        m=self.midi;return int(round(m))%12 if m is not None else None

@dataclass(slots=True)
class MediaDNA:
    energy_curve:list[float]=field(default_factory=list);transients:list[float]=field(default_factory=list);tempo_bpm:float|None=None;tempo_confidence:float=0.0;pitch_classes:list[float]=field(default_factory=lambda:[0.0]*12);spectral_centroid_hz:float=0.0;spectral_flux:float=0.0;dynamic_range:float=0.0;motion:float=0.0;luminance:float=0.0;scene_change:float=0.0;source_name:str=""

@dataclass(slots=True)
class HarmonicHypothesis:
    root_pc:int;mode:str;chord_root_pc:int;chord_quality:str;score:float;confidence:float
    @property
    def key_name(self):return f"{PITCH_NAMES[self.root_pc]} {'major' if self.mode=='major' else 'minor'}"
    @property
    def chord_name(self):
        q={"maj":"","min":"m","dim":"dim"}.get(self.chord_quality,self.chord_quality);return f"{PITCH_NAMES[self.chord_root_pc]}{q}"

class HarmonyTracker:
    """Rolling evidence scorer. Melody does not uniquely identify harmony."""
    def __init__(self,history=64):self.history=deque(maxlen=history);self.weights=[0.0]*12;self.last=None
    def reset(self):self.history.clear();self.weights[:]=[0.0]*12;self.last=None
    def observe(self,dna):
        pc=dna.pitch_class
        if pc is None or dna.pitch_confidence<0.35:return self.last
        weight=clamp(dna.energy,.05,1.0)*clamp(dna.pitch_confidence,0,1);self.history.append((pc,weight,dna.timestamp));self.weights=[w*.965 for w in self.weights];self.weights[pc]+=weight;self.last=self._infer();return self.last
    def _infer(self):
        total=sum(self.weights)
        if total<=1e-8:return None
        candidates=[]
        for root in range(12):
            for mode,scale in (("major",MAJOR),("minor",NAT_MINOR)):
                allowed={(root+x)%12 for x in scale};ins=sum(self.weights[pc] for pc in allowed);outside=total-ins;score=ins+self.weights[root]*.35+self.weights[(root+7)%12]*.12-outside*.8;candidates.append((score,root,mode))
        candidates.sort(reverse=True);best_score,root,mode=candidates[0];second=candidates[1][0];confidence=clamp((best_score-second)/max(total,1e-6)*2.5+min(total/5,.35),0,1);scale=MAJOR if mode=="major" else NAT_MINOR;qualities=("maj","min","min","maj","maj","min","dim") if mode=="major" else ("min","dim","maj","min","min","maj","maj");scores=[]
        for degree,interval in enumerate(scale):
            cr=(root+interval)%12;ints=CHORD_QUALITIES[qualities[degree]];pcs={(cr+i)%12 for i in ints};s=sum(self.weights[p] for p in pcs)+self.weights[cr]*.25
            if self.last and self.last.chord_root_pc==cr:s+=.04*total
            scores.append((s,cr,qualities[degree]))
        scores.sort(reverse=True);_,cr,q=scores[0];return HarmonicHypothesis(root,mode,cr,q,best_score,confidence)

@dataclass(slots=True)
class NoteEvent:
    note:int;velocity:int;duration_beats:float;channel:int=0;role:str="voice"

@dataclass
class BridgeState:
    seed:int=1;bpm:float=96.0;energy:float=.55;entropy:float=.25;life:float=.7;motion:float=.5;gravity:float=.65;human_alien:float=.2;mode:str="FULL_BAND";harmonic:HarmonicHypothesis|None=None;media:MediaDNA|None=None
    def jsonable(self):return asdict(self)

class AccompanimentEngine:
    """Host-neutral accompaniment planner producing MIDI-like NoteEvents."""
    def __init__(self,seed=1):self.state=BridgeState(seed=seed);self.tracker=HarmonyTracker();self.rng=random.Random(seed);self.recent_melody=deque(maxlen=32)
    def genesis(self,seed=None):
        if seed is None:seed=self.rng.randrange(1,2**31-1)
        self.rng.seed(seed);s=self.state;s.seed=seed;s.bpm=self.rng.choice((72,84,92,100,108,120,132));s.energy=self.rng.uniform(.35,.8);s.entropy=self.rng.uniform(.12,.65);s.life=self.rng.uniform(.45,.95);s.motion=self.rng.uniform(.25,.85);s.gravity=self.rng.uniform(.35,.9);s.human_alien=self.rng.uniform(0,.6);self.tracker.reset();self.recent_melody.clear();return s
    def attach_media(self,media):
        self.state.media=media
        if media.tempo_bpm and media.tempo_confidence>.45:self.state.bpm=clamp(media.tempo_bpm,45,190)
    def observe_voice(self,dna):
        h=self.tracker.observe(dna)
        if h:self.state.harmonic=h
        if dna.midi is not None and dna.pitch_confidence>=.45:self.recent_melody.append(int(round(dna.midi)))
        self.state.energy=.82*self.state.energy+.18*clamp(dna.energy,0,1);self.state.motion=.85*self.state.motion+.15*clamp(dna.articulation,0,1);return h
    def chord_notes(self,octave=4,extensions=False):
        h=self.state.harmonic
        if h is None:return [60,64,67]
        ints=list(CHORD_QUALITIES.get(h.chord_quality,CHORD_QUALITIES["maj"]))
        if extensions and len(ints)==3:ints.append(10 if h.chord_quality=="min" else 11)
        base=12*(octave+1)+h.chord_root_pc;return [base+i for i in ints]
    def plan_bar(self,beats=4):
        h=self.state.harmonic;confidence=h.confidence if h else 0.0;events=[];chord=self.chord_notes(4,self.state.entropy>.48);density=clamp(self.state.energy*(.65+.45*confidence),.15,1)
        if confidence>=.22 or h is None:
            vel=int(32+42*density);events.extend(NoteEvent(n,vel,beats,role="pad") for n in chord)
        if h and confidence>=.3:
            bass=36+h.chord_root_pc
            if bass>47:bass-=12
            events.append(NoteEvent(bass,int(48+34*density),beats/2,role="bass"))
            if density>.6:events.append(NoteEvent(bass+7,int(38+26*density),beats/2,role="bass"))
        if self.state.mode in {"MELODY_SHADOW","CALL_RESPONSE"} and self.recent_melody:
            source=list(self.recent_melody)[-min(6,len(self.recent_melody)):];interval=7 if self.state.human_alien<.65 else self.rng.choice((5,7,11,13))
            for n in source:events.append(NoteEvent(max(36,min(96,n+interval)),50,.5,role="response"))
        return events

def serialize_events(events:Sequence[NoteEvent])->list[dict]:return [asdict(e) for e in events]
