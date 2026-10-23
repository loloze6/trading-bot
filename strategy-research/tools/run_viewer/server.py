"""
run viewer server (D-180): a read-only, local-network web page over the campaign's run
folders and records. Stdlib http.server + the loaders in this folder.

Start (from strategy-research/):

    & $env:TBOT_PYTHON tools/run_viewer/server.py --runs runs --port 8765 [--host 0.0.0.0]

--root defaults to the parent of --runs. The server binds 127.0.0.1 unless --host is given.
There is no authentication: it is a local-network tool. GET and HEAD only; every other
method answers 405. Nothing is ever written. Every response string passes through
sanitize.py (sealed-window dates masked); if the sealed-window policy cannot be read the
server refuses to start.

Routes (see DESIGN.md):
    /                                              the page (static/index.html)
    /static/<file>                                 files inside tools/run_viewer/static/ only
    /api/runs                                      view 1
    /api/run/<id>                                  view 2
    /api/run/<id>/step/<name>                      view 3
    /api/run/<id>/variant/<v>/window/<label>/bars  view 4, one window
    /api/run/<id>/variant/<v>/equity               view 4, chained equity
"""
import sys

sys.dont_write_bytecode = True  # first, before any import of loaders / sanitize / tools modules

import argparse  # noqa: E402
import json  # noqa: E402
import mimetypes  # noqa: E402
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer  # noqa: E402
from pathlib import Path  # noqa: E402
from urllib.parse import unquote  # noqa: E402

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import loaders  # noqa: E402
import sanitize  # noqa: E402

STATIC_DIR = _HERE / "static"
mimetypes.init()  # read the system mime tables now, not on the first request
NO_START = "run viewer: sealed-window policy unreadable; not starting"
REQUEST_ERROR = "run viewer: request error"


def banner(host, port):
    return sanitize.sanitize_text(
        f"run viewer: read-only, local network only, no authentication -- http://{host}:{port}/")


def _stderr_sink(line):
    sys.stderr.write(line + "\n")
    sys.stderr.flush()


class RunViewerServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, addr, root, runs_dir, log_sink=None):
        self.root = Path(root)
        self.runs_dir = Path(runs_dir)
        self.log_sink = log_sink or _stderr_sink
        super().__init__(addr, Handler)

    def handle_error(self, request, client_address):
        """An exception while serving a request: one fixed line to the log sink, never a
        traceback on stderr (a traceback can carry the request line)."""
        try:
            self.log_sink(REQUEST_ERROR)
        except Exception:  # noqa: BLE001
            pass


def make_server(root, runs_dir, host="127.0.0.1", port=0, log_sink=None):
    """Create (but do not run) the server. Raises (fixed text) if the policy is unreadable."""
    sanitize._ensure_ready()
    return RunViewerServer((host, port), root, runs_dir, log_sink)


class Handler(BaseHTTPRequestHandler):
    server_version = "RunViewer"
    sys_version = ""
    protocol_version = "HTTP/1.0"

    # ---- logging: method, path, status only; always through sanitize_text
    def log_request(self, code="-", size="-"):
        # command / path do not exist yet when the request line itself was bad (414, 400, ...)
        cmd = getattr(self, "command", None) or "-"
        path = getattr(self, "path", None) or "-"
        line = f"{self._clean(cmd)} {self._clean(path)} {code}"
        self.server.log_sink(sanitize.sanitize_text(line)[:300])

    def log_error(self, format, *args):  # noqa: A002 -- stdlib signature
        code = args[0] if args and isinstance(args[0], int) else "-"
        cmd = getattr(self, "command", None) or "-"
        self.server.log_sink(sanitize.sanitize_text(f"{self._clean(cmd)} - {code}")[:300])

    def send_error(self, code, message=None, explain=None):
        """Every error the stdlib raises on its own (400, 414, 501, 505, ...) answers with a
        fixed JSON body: nothing of the request is echoed back."""
        self.close_connection = True
        try:
            self._err(code, "bad request" if code < 500 else "not supported",
                      head_only=getattr(self, "command", None) == "HEAD")
        except Exception:  # noqa: BLE001 -- a peer that went away mid-reply
            pass

    def log_message(self, format, *args):  # noqa: A002
        pass

    @staticmethod
    def _clean(s):
        # printable ASCII only; NOT truncated here -- the caller truncates after sanitising,
        # so a date can never be cut in half and slip past the masks
        return "".join(c if 32 <= ord(c) < 127 else "?" for c in str(s))

    # ---- responses
    def _send(self, code, body: bytes, ctype, head_only=False, extra=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if not head_only:
            for i in range(0, len(body), 32768):
                self.wfile.write(body[i:i + 32768])
            self.wfile.flush()

    def _json(self, code, payload, head_only=False, extra=None):
        try:
            text = json.dumps(sanitize.sanitize(payload), allow_nan=False, ensure_ascii=False)
        except Exception:  # noqa: BLE001 -- sanitize failure must not leak unmasked data
            code, text = 500, json.dumps({"error": "response could not be built"})
        self._send(code, text.encode("utf-8"), "application/json; charset=utf-8", head_only, extra)

    def _err(self, code, msg, head_only=False, extra=None):
        self._json(code, {"error": msg}, head_only, extra)

    # ---- methods
    def do_GET(self):
        self._dispatch(False)

    def do_HEAD(self):
        self._dispatch(True)

    def _not_allowed(self):
        self._err(405, "method not allowed", extra={"Allow": "GET, HEAD"})

    do_POST = do_PUT = do_DELETE = do_PATCH = do_OPTIONS = do_TRACE = do_CONNECT = _not_allowed

    def _dispatch(self, head):
        try:
            raw = self.path.split("?", 1)[0].split("#", 1)[0]
            if raw == "/" or raw == "/index.html":
                return self._static("index.html", head)
            if raw.startswith("/static/"):
                return self._static(unquote(raw[len("/static/"):]), head)
            if raw.startswith("/api/"):
                segs = [unquote(p) for p in raw[len("/api/"):].split("/")]
                return self._api(segs, head)
            return self._err(404, "not found", head)
        except Exception:  # noqa: BLE001
            return self._err(500, "internal error", head)

    # ---- static
    def _static(self, rel, head):
        if not rel or "\x00" in rel or "\\" in rel or rel.startswith("/") or ".." in rel.split("/"):
            return self._err(404, "not found", head)
        try:
            base = STATIC_DIR.resolve()
            p = (STATIC_DIR / rel).resolve()
            p.relative_to(base)
        except (ValueError, OSError):
            return self._err(404, "not found", head)
        if not p.is_file():
            return self._err(404, "not found", head)
        ctype = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        try:
            with open(p, "rb") as fh:
                data = fh.read()
        except OSError:
            return self._err(404, "not found", head)
        # Text static files are masked like any other output. Non-text files (the vendored
        # uPlot assets are .js/.css, so masked too; images or fonts, if ever added) are
        # served byte for byte: they are vendored code, not data.
        if ctype.startswith("text/") or ctype in ("application/javascript", "application/json"):
            try:
                data = sanitize.sanitize_text(data.decode("utf-8")).encode("utf-8")
            except UnicodeDecodeError:
                pass
            ctype += "; charset=utf-8"
        self._send(200, data, ctype, head)

    # ---- api
    def _api(self, segs, head):
        root, runs = self.server.root, self.server.runs_dir
        if segs == ["runs"]:
            return self._json(200, loaders.load_campaign(root, runs), head)
        if len(segs) < 2 or segs[0] != "run":
            return self._err(404, "not found", head)
        run_id = segs[1]
        if not loaders.run_exists(runs, run_id):
            return self._err(404, "unknown run", head)
        rest = segs[2:]
        if not rest:
            return self._json(200, loaders.load_run(root, runs, run_id), head)
        if rest[0] == "step" and len(rest) == 2:
            if rest[1] not in loaders.STEP_NAMES:
                return self._err(404, "unknown step", head)
            return self._json(200, loaders.load_step(root, runs, run_id, rest[1]), head)
        if rest[0] == "variant" and len(rest) >= 3:
            rd = loaders.Reader(root, runs, run_id)
            variant = rest[1]
            if variant not in loaders.list_variants(rd):
                return self._err(404, "unknown variant", head)
            if rest[2:] == ["equity"]:
                return self._json(200, loaders.load_equity(root, runs, run_id, variant), head)
            if len(rest) == 5 and rest[2] == "window" and rest[4] == "bars":
                if rest[3] not in loaders.list_windows(rd, variant):
                    return self._err(404, "unknown window", head)
                return self._json(200, loaders.load_bars(root, runs, run_id, variant, rest[3]), head)
        return self._err(404, "not found", head)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Read-only run viewer (D-180).")
    ap.add_argument("--runs", default="runs", help="the runs folder (default: runs)")
    ap.add_argument("--root", default=None, help="strategy-research root (default: parent of --runs)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args(argv)
    runs_dir = Path(args.runs).resolve()
    root = Path(args.root).resolve() if args.root else runs_dir.parent
    try:
        srv = make_server(root, runs_dir, args.host, args.port)
    except OSError:
        sys.stderr.write("run viewer: cannot bind that host/port\n")
        return 1
    except Exception:  # noqa: BLE001 -- the fixed-text refusal, no cause, no path
        sys.stderr.write(NO_START + "\n")
        return 1
    print(banner(args.host, srv.server_address[1]), flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
