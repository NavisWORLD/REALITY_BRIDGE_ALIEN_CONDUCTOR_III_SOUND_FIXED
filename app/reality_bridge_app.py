#!/usr/bin/env python3
"""Zero-dependency desktop launcher for the web instrument."""
from pathlib import Path
import argparse, http.server, socketserver, threading, webbrowser

class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control','no-store')
        super().end_headers()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--port',type=int,default=8766); ap.add_argument('--no-browser',action='store_true'); a=ap.parse_args()
    root=Path(__file__).resolve().parents[1]
    handler=lambda *args,**kwargs: NoCache(*args,directory=str(root),**kwargs)
    with socketserver.ThreadingTCPServer(('127.0.0.1',a.port),handler) as server:
        url=f'http://127.0.0.1:{a.port}/'
        print('Reality Bridge:',url)
        if not a.no_browser: threading.Timer(.35,lambda:webbrowser.open(url)).start()
        server.serve_forever()
if __name__=='__main__': main()
