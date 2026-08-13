from __future__ import annotations
import http.server,socketserver,threading,webbrowser
from pathlib import Path
class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map={**http.server.SimpleHTTPRequestHandler.extensions_map,'.webmanifest':'application/manifest+json','.wasm':'application/wasm'}
    def end_headers(self):self.send_header('Cache-Control','no-store');super().end_headers()
def serve(root,port=8080,open_browser=True):
    root=Path(root).resolve();factory=lambda *a,**k:Handler(*a,directory=str(root),**k)
    with socketserver.ThreadingTCPServer(('127.0.0.1',port),factory) as httpd:
        url=f'http://127.0.0.1:{port}/';print(f'Reality Bridge serving {root} at {url}')
        if open_browser:threading.Timer(.5,lambda:webbrowser.open(url)).start()
        httpd.serve_forever()
