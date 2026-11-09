"""Serve a built study on this computer for testing.

    ~/.venvs/musipam/bin/python serve.py study0            # then open http://localhost:8765/?debug=1

(`python -m http.server` drops connections when the experiment preloads all of its audio
at once; this server queues them, and tells the browser not to cache, so a rebuild shows
up on reload.)
"""
from __future__ import annotations

import argparse
import functools
import http.server
from pathlib import Path

HERE = Path(__file__).resolve().parent


class Server(http.server.ThreadingHTTPServer):
    request_queue_size = 128
    daemon_threads = True


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, *args) -> None:  # quiet
        pass


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("study", nargs="?", default="study0")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()
    root = HERE / "dist" / args.study
    if not (root / "index.html").exists():
        raise SystemExit(f"build it first: python build.py {args.study}")
    with Server(("127.0.0.1", args.port), functools.partial(Handler, directory=str(root))) as httpd:
        print(f"serving {root} at http://localhost:{args.port}/?debug=1  (Ctrl-C stops)", flush=True)
        httpd.serve_forever()


if __name__ == "__main__":
    main()
