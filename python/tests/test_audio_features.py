import math,struct,wave
from reality_bridge.audio_features import analyze_wav

def test_wav_analyzer(tmp_path):
    p=tmp_path/'tone.wav';sr=8000;data=[int(14000*math.sin(2*math.pi*220*i/sr)) for i in range(sr)]
    with wave.open(str(p),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(b''.join(struct.pack('<h',x) for x in data))
    dna=analyze_wav(p);assert len(dna.energy_curve)>10;assert dna.dynamic_range>=0
