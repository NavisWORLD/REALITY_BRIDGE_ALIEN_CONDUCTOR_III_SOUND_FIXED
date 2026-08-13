#!/usr/bin/env python3
"""Frozen-app aware desktop launcher for Cosmic Conductor Engine."""
from __future__ import annotations

import argparse
import http.server
import os
import socketserver
import sys
import threading
import webbrowser
from pathlib import Path

APP_FILE = "REALITY_BRIDGE_ALIEN_CONDUCTOR_III_SOUND_FIXED.html"


class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        super().end_headers()


def web_root() -> Path:
    if getattr(sys, "frozen", False):
        bundle = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
        for candidate in (bundle / "www", Path(sys.executable).resolve().parent / "www"):
            if (candidate / APP_FILE).exists():
                return candidate
    root = Path(__file__).resolve().parents[1]
    if (root / APP_FILE).exists():
        return root
    raise FileNotFoundError(f"Could not locate bundled {APP_FILE}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Launch Cosmic Conductor Engine")
    ap.add_argument("--port", type=int, default=0, help="localhost port; 0 chooses a free port")
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()

    root = web_root()
    handler = lambda *a, **kw: NoCache(*a, directory=str(root), **kw)
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", args.port), handler) as server:
        port = int(server.server_address[1])
        url = f"http://127.0.0.1:{port}/index.html"
        os.environ["COSMIC_CONDUCTOR_URL"] = url
        print(f"Cosmic Conductor Engine: {url}")
        if not args.no_browser:
            threading.Timer(0.35, lambda: webbrowser.open_new_tab(url)).start()
        server.serve_forever()


if __name__ == "__main__":
    main()
