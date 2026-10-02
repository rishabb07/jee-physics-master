"""
Local Development Server with live filesystem watcher and auto-recompilation.
Serves output/web/ using standard library http.server.
"""

import http.server
import socketserver
import threading
import time
from pathlib import Path
from typing import Optional

from jee_physics.web.compiler import WebCompiler


class DevServer:
    def __init__(self, root_dir: Optional[Path] = None, port: int = 8080, host: str = "127.0.0.1"):
        self.root_dir = root_dir or Path.cwd()
        self.port = port
        self.host = host
        self.compiler = WebCompiler(root_dir=self.root_dir)
        self.dist_dir = self.root_dir / "output" / "web"
        self._stop_event = threading.Event()
        self._server_ready = threading.Event()

    def stop(self):
        self._stop_event.set()

    def start(self, watch: bool = True):
        # Initial compilation
        print("Compiling web application...")
        self.compiler.compile()
        print(f"Compilation complete. Serving {self.dist_dir}")

        if watch:
            watcher_thread = threading.Thread(target=self._watch_loop, daemon=True)
            watcher_thread.start()

        self._serve()

    def _serve(self):
        class Handler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, directory=None, **kwargs):
                super().__init__(*args, directory=str(directory), **kwargs)

            def end_headers(self):
                # Disable caching for instant dev updates
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")
                super().end_headers()

            def log_message(self, format, *args):
                pass  # Quieter dev logs

        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer((self.host, self.port), lambda *args, **kwargs: Handler(*args, directory=self.dist_dir, **kwargs)) as httpd:
            self.port = httpd.server_address[1]
            httpd.timeout = 0.5
            self._server_ready.set()
            print(f"JEE Physics Web Dev Server running at http://{self.host}:{self.port}/")
            print("Press Ctrl+C to stop.")
            try:
                while not self._stop_event.is_set():
                    httpd.handle_request()
            except KeyboardInterrupt:
                print("\nStopping dev server...")
            finally:
                self._stop_event.set()

    def _watch_loop(self):
        watch_dirs = [
            self.root_dir / "kb",
            self.root_dir / "build" / "staging" / "incoming",
            self.root_dir / "curriculum",
            self.root_dir / "question_bank" / "verified",
            self.root_dir / "web",
        ]

        def get_mtimes():
            mtimes = {}
            for d in watch_dirs:
                if d.exists():
                    for f in d.rglob("*"):
                        if f.is_file():
                            try:
                                mtimes[str(f)] = f.stat().st_mtime
                            except Exception:
                                pass
            return mtimes

        last_mtimes = get_mtimes()

        while not self._stop_event.is_set():
            time.sleep(1.0)
            current_mtimes = get_mtimes()
            changed = False
            if len(current_mtimes) != len(last_mtimes):
                changed = True
            else:
                for path, mtime in current_mtimes.items():
                    if path not in last_mtimes or mtime > last_mtimes[path]:
                        changed = True
                        break

            if changed:
                print("[Auto-Update] Detected changes in source knowledge/assets. Recompiling web application...")
                try:
                    self.compiler.compile()
                    print("[Auto-Update] Recompilation successful.")
                except Exception as e:
                    print(f"[Auto-Update] Recompilation failed: {e}")
                last_mtimes = current_mtimes
