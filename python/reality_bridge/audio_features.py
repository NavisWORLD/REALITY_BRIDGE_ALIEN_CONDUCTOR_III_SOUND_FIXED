"""Small dependency-free WAV analyzer used by the CLI and teaching labs."""
from __future__ import annotations
from dataclasses import dataclass
import math,struct,wave
from pathlib import Path
from .engine import MediaDNA

@dataclass(slots=True)
class WavData:
    sample_rate:int;channels:int;samples:list[float]

def read_wav(path,max_seconds=180.0):
    with wave.open(str(path),'rb') as wf:
        channels=wf.getnchannels();width=wf.getsampwidth();sr=wf.getframerate();frames=min(wf.getnframes(),int(sr*max_seconds));raw=wf.readframes(frames)
    if width not in (1,2,3,4):raise ValueError(f"unsupported PCM sample width: {width}")
    step=width*channels;out=[]
    for off in range(0,len(raw)-step+1,step):
        acc=0.0
        for ch in range(channels):
            b=raw[off+ch*width:off+(ch+1)*width]
            if width==1:v=(b[0]-128)/128.0
            elif width==2:v=struct.unpack_from('<h',b)[0]/32768.0
            elif width==3:
                x=int.from_bytes(b,'little',signed=False);x=x-(1<<24) if x&0x800000 else x;v=x/8388608.0
            else:v=struct.unpack_from('<i',b)[0]/2147483648.0
            acc+=v
        out.append(acc/channels)
    return WavData(sr,channels,out)

def analyze_wav(path):
    wav=read_wav(path);samples,sr=wav.samples,wav.sample_rate
    if not samples:return MediaDNA(source_name=Path(path).name)
    hop=max(128,sr//50);window=max(hop,sr//25);energy=[];transients=[];prev=0.;zc_total=0
    for start in range(0,len(samples),hop):
        block=samples[start:start+window]
        if not block:break
        rms=math.sqrt(sum(x*x for x in block)/len(block));energy.append(rms);flux=max(0.,rms-prev)
        if flux>.045 and rms>.03:transients.append(start/sr)
        prev=.8*prev+.2*rms;zc_total+=sum(1 for a,b in zip(block,block[1:]) if (a<=0<b) or (a>=0>b))
    tempo,conf=_tempo_from_transients(transients);sorted_e=sorted(energy);p10=sorted_e[int(.1*(len(sorted_e)-1))];p90=sorted_e[int(.9*(len(sorted_e)-1))];seconds=len(samples)/sr;zcr_hz=(zc_total/max(seconds,1e-6))/max(1,len(range(0,len(samples),hop)));brightness_hz=min(sr/2,max(0.,zcr_hz*6.))
    return MediaDNA(energy_curve=energy,transients=transients,tempo_bpm=tempo,tempo_confidence=conf,spectral_centroid_hz=brightness_hz,dynamic_range=max(0.,p90-p10),source_name=Path(path).name)

def _tempo_from_transients(ts):
    if len(ts)<4:return None,0.0
    intervals=[b-a for a,b in zip(ts,ts[1:]) if .18<=b-a<=2.0]
    if not intervals:return None,0.0
    bpms=[]
    for dt in intervals:
        bpm=60./dt
        while bpm<70:bpm*=2
        while bpm>180:bpm/=2
        bpms.append(bpm)
    bpms.sort();med=bpms[len(bpms)//2];spread=sum(abs(x-med) for x in bpms)/len(bpms);conf=max(0.,min(1.,1.-spread/35.))*min(1.,len(bpms)/12.);return med,conf
