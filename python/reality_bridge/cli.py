from __future__ import annotations
import argparse,json
from dataclasses import asdict
from pathlib import Path
from .engine import AccompanimentEngine,VoiceDNA,serialize_events
from .audio_features import analyze_wav
from .server import serve

def main(argv=None):
    p=argparse.ArgumentParser(prog='reality-bridge',description='Reality Bridge engine, analyzer, MIDI bridge, and local app launcher');sub=p.add_subparsers(dest='cmd',required=True)
    s=sub.add_parser('serve',help='serve the handheld web app locally');s.add_argument('--port',type=int,default=8080);s.add_argument('--root')
    a=sub.add_parser('analyze',help='analyze a PCM WAV into Media DNA');a.add_argument('wav')
    d=sub.add_parser('demo',help='print deterministic accompaniment events');d.add_argument('--seed',type=int,default=42)
    m=sub.add_parser('midi',help='send demo accompaniment to a MIDI output');m.add_argument('--output');m.add_argument('--bpm',type=float,default=96);m.add_argument('--bars',type=int,default=4);args=p.parse_args(argv)
    if args.cmd=='serve':serve(Path(args.root) if args.root else Path(__file__).resolve().parents[2],args.port)
    elif args.cmd=='analyze':print(json.dumps(asdict(analyze_wav(args.wav)),indent=2))
    elif args.cmd=='demo':
        e=AccompanimentEngine(args.seed)
        for i,hz in enumerate((261.63,329.63,392.0,329.63,261.63)):e.observe_voice(VoiceDNA(hz,.92,.65,.45,.5,.88,True,i*.5))
        print(json.dumps({'state':e.state.jsonable(),'bar':serialize_events(e.plan_bar())},indent=2))
    elif args.cmd=='midi':
        from .midi_bridge import run_bridge;run_bridge(args.output,args.bpm,args.bars)
if __name__=='__main__':main()
