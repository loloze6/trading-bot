"""
loaders.py -- the run viewer's data layer (D-180, read-only, no HTTP).

Pure functions: each view's loader returns one JSON-able document and never raises on a
missing or unparseable file. Every source is reported as
    {"path": <relative to root, forward slashes>, "state": "present"|"absent"|"unreadable",
     "reason"?: <why>}
and the field it would have filled is None (or the string "unreadable (<reason>)" for a
missing key / unexpected type inside a file that did parse). A bug inside one step
loader gives that card status "unreadable" with the reason; the other cards still render.

Reads (all strictly read-only, under the strategy-research root and the runs folder):
    runs/run_NNN/**  (never runs/*/handoffs/), config/campaign_queue.yaml,
    briefs/<name>.md, campaign_record/{campaign_state.yaml, campaign_memory.yaml,
    campaign_log.md, block_registry.yaml}.
Never trading-bot/local_data, never config/campaign_data_policy.yaml (only sanitize.py
reads the policy, once).

Parsed files are cached by (path, mtime_ns, size), so every request rescans cheaply and a
finished run shows up without a restart.
"""
import sys

sys.dont_write_bytecode = True  # before any tools/ import (block_registry): no .pyc under the repo

import json  # noqa: E402
import math  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
from datetime import date, datetime  # noqa: E402
from pathlib import Path  # noqa: E402

import yaml  # noqa: E402

_TOOLS_DIR = Path(__file__).resolve().parents[1]

# yaml.safe_load semantics (the safe loader); the C-accelerated safe loader when available.
_SAFE_LOADER = getattr(yaml, "CSafeLoader", yaml.SafeLoader)

RUN_ID_RE = re.compile(r"^run_[0-9]+\Z")
_STAMP_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*\Z")
_SAFE_NAME_RE = _STAMP_RE
RAW_CAP = 300 * 1024
COST_LABEL = "model cost (stages that called a model)"

STEP_DEFS = [
    ("launch", "Launch"),
    ("config", "Step 1b: config"),
    ("variants", "Step 2: variants"),
    ("data_gate", "Data gate"),
    ("protocol", "Protocol execution"),
    ("replay_gate", "Replay gate"),
    ("profit_bars", "Profit bars"),
    ("grid", "Criteria grid and residual IC"),
    ("claims", "Claim tests"),
    ("analyst", "Analyst lenses"),
    ("decide_next", "Decide-next"),
    ("record", "Record"),
]
STEP_NAMES = [n for n, _ in STEP_DEFS]
_TITLES = dict(STEP_DEFS)

BAR_COLUMNS = {
    "timestamp": "timestamp",
    "close": "close",
    "forecast": "forecast",
    "position": "postRebalance_current_allocation",
    "portfolio_value": "portfolio_value",
    "approved_rebalance": "approved_rebalance",
}
TRADE_FIELDS = ["entry_time", "exit_time", "side", "entry_price", "exit_price",
                "net_profit_loss_percent", "duration_minutes"]

# --------------------------------------------------------------------------- json-able


def _jsonable(o):
    """Datetimes/dates -> ISO strings, NaN/inf -> None, keys -> str, tuples/sets -> lists."""
    if isinstance(o, bool) or o is None or isinstance(o, (str, int)):
        return o
    if isinstance(o, float):
        return o if math.isfinite(o) else None
    if isinstance(o, (datetime, date)):
        return o.isoformat()
    if isinstance(o, dict):
        return {str(k) if not isinstance(k, str) else k: _jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple, set)):
        return [_jsonable(v) for v in o]
    if hasattr(o, "item"):  # numpy scalar
        try:
            return _jsonable(o.item())
        except Exception:  # noqa: BLE001
            return str(o)
    return str(o)


class Unr(str):
    """A field that could not be read: 'unreadable (<reason>)'."""


def _unr(reason):
    return Unr(f"unreadable ({reason})")


def req(obj, *path):
    """Required nested key; a missing key or unexpected type gives an Unr string."""
    cur = obj
    walked = []
    for k in path:
        walked.append(str(k))
        if isinstance(cur, dict):
            if k not in cur:
                return _unr("missing key " + ".".join(walked))
            cur = cur[k]
        elif isinstance(cur, list) and isinstance(k, int) and -len(cur) <= k < len(cur):
            cur = cur[k]
        else:
            where = ".".join(walked[:-1]) or "document"
            return _unr(f"{where} is {type(cur).__name__}, expected mapping")
    return cur


def opt(obj, *path, default=None):
    """Optional nested key; anything missing or of the wrong type -> default."""
    cur = obj
    for k in path:
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        elif isinstance(cur, list) and isinstance(k, int) and -len(cur) <= k < len(cur):
            cur = cur[k]
        else:
            return default
    return cur


def _is_unr(*vals):
    return any(isinstance(v, Unr) for v in vals)


def fmt(v):
    if v is None:
        return "-"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float):
        return f"{v:.6g}"
    if isinstance(v, (dict, list)):
        return json.dumps(_jsonable(v), sort_keys=False, separators=(",", ":"))
    return str(v)


def _as_dict(v):
    return v if isinstance(v, dict) else {}


def _as_list(v):
    return v if isinstance(v, list) else []


# --------------------------------------------------------------------------- file cache

_CACHE = {}
_CACHE_MAX = 400


def _cache_put(key, val):
    if len(_CACHE) >= _CACHE_MAX:
        _CACHE.clear()
    _CACHE[key] = val


def _parse_text(path: Path, kind: str):
    """-> ("ok", value) | ("bad", reason). Read-only open."""
    try:
        with open(path, "r", encoding="utf-8", newline=None) as fh:
            text = fh.read()
    except UnicodeDecodeError:
        return ("bad", "not valid UTF-8 text")
    except OSError as exc:
        return ("bad", f"cannot read file ({type(exc).__name__})")
    if kind == "text":
        return ("ok", text)
    try:
        if kind == "yaml":
            val = yaml.load(text, Loader=_SAFE_LOADER)  # safe loader only
        else:
            val = json.loads(text)
    except Exception as exc:  # noqa: BLE001 -- parse errors of any flavour
        mark = getattr(exc, "problem_mark", None)
        where = f" at line {mark.line + 1}" if mark is not None else ""
        return ("bad", f"unparseable {kind.upper()}{where} ({type(exc).__name__})")
    return ("ok", _jsonable(val))


class Reader:
    """Reads files under the root / runs folder, remembers every source it touched."""

    def __init__(self, root, runs_dir=None, run_id=None):
        self.root = Path(root)
        self.runs_dir = Path(runs_dir) if runs_dir is not None else self.root / "runs"
        self.run_id = run_id
        self.sources = []
        self._seen = {}

    # -- paths
    def run_path(self, rel: str) -> Path:
        return self.runs_dir / self.run_id / rel

    def disp(self, path) -> str:
        p = Path(path)
        for base in (self.root, self.runs_dir.parent):
            try:
                return p.relative_to(base).as_posix()
            except ValueError:
                continue
        return p.name

    def _guard(self, path: Path):
        parts = path.parts
        if ".." in parts or "handoffs" in parts:
            raise ValueError("path not allowed")

    def _note(self, path, state, reason=None):
        d = self.disp(path)
        if d in self._seen:
            return
        rec = {"path": d, "state": state}
        if reason:
            rec["reason"] = reason
        self._seen[d] = rec
        self.sources.append(rec)

    def present_paths(self):
        return [r["path"] for r in self.sources if r["state"] == "present"]

    # -- reads
    def _load(self, path, kind):
        path = Path(path)
        try:
            self._guard(path)
            st = path.stat()
        except ValueError:
            self._note(path, "unreadable", "path not allowed")
            return None
        except OSError:
            self._note(path, "absent")
            return None
        if not path.is_file():
            self._note(path, "absent")
            return None
        key = (str(path), st.st_mtime_ns, st.st_size, kind)
        hit = _CACHE.get(key)
        if hit is None:
            hit = _parse_text(path, kind)
            _cache_put(key, hit)
        if hit[0] == "bad":
            self._note(path, "unreadable", hit[1])
            return None
        self._note(path, "present")
        return hit[1]

    def yaml(self, path):
        return self._load(path, "yaml")

    def json(self, path):
        return self._load(path, "json")

    def text(self, path):
        return self._load(path, "text")

    def exists(self, path) -> bool:
        try:
            return Path(path).is_file()
        except OSError:
            return False

    def listdir(self, path):
        try:
            return sorted(os.listdir(path))
        except OSError:
            return []



# --------------------------------------------------------------------------- csv (bars)


def _read_bars_csv(rd: Reader, path: Path):
    """-> dict of column lists (None for a column the file lacks), or None if unreadable/absent."""
    try:
        rd._guard(path)
        st = path.stat()
    except (OSError, ValueError):
        rd._note(path, "absent")
        return None
    key = (str(path), st.st_mtime_ns, st.st_size, "bars")
    hit = _CACHE.get(key)
    if hit is None:
        try:
            import pandas as pd

            with open(path, "rb") as fh:
                header = list(pd.read_csv(fh, nrows=0).columns)
            wanted = [c for c in BAR_COLUMNS.values() if c in header]
            with open(path, "rb") as fh:
                df = pd.read_csv(fh, usecols=wanted)
            cols = {}
            for out, src in BAR_COLUMNS.items():
                if src not in df.columns:
                    cols[out] = None
                    continue
                s = df[src]
                if out == "timestamp":
                    cols[out] = [None if (isinstance(v, float) and math.isnan(v)) else str(v) for v in s.tolist()]
                elif out == "approved_rebalance":
                    cols[out] = [_bool_or_none(v) for v in s.tolist()]
                else:
                    cols[out] = _jsonable(s.tolist())
            hit = ("ok", cols)
        except Exception as exc:  # noqa: BLE001
            hit = ("bad", f"unparseable CSV ({type(exc).__name__})")
        _cache_put(key, hit)
    if hit[0] == "bad":
        rd._note(path, "unreadable", hit[1])
        return None
    rd._note(path, "present")
    return hit[1]


def _bool_or_none(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return None
    if isinstance(v, (bool, int, float)):
        return bool(v)
    s = str(v).strip().lower()
    if s in ("true", "1", "yes"):
        return True
    if s in ("false", "0", "no"):
        return False
    return None


# --------------------------------------------------------------------------- briefs / queue / log


def parse_brief(text):
    """Front matter between the first two '---' lines -> dict, or None."""
    if not isinstance(text, str):
        return None
    lines = text.splitlines()
    idx = [i for i, ln in enumerate(lines) if ln.strip() == "---"]
    if len(idx) < 2:
        return None
    body = "\n".join(lines[idx[0] + 1: idx[1]])
    try:
        doc = yaml.load(body, Loader=_SAFE_LOADER)
    except Exception:  # noqa: BLE001
        return None
    return _jsonable(doc) if isinstance(doc, dict) else None


_OUTCOME_LINE = re.compile(r"^\s*([A-Z][0-9]*)\.\s+(.*\S)\s*$")


def parse_outcomes(front):
    out = []
    for c in _as_list(opt(front, "constraints")):
        if isinstance(c, str) and "Pre-registered outcomes" in c:
            for ln in c.splitlines()[1:]:
                m = _OUTCOME_LINE.match(ln)
                if m:
                    out.append({"letter": m.group(1), "text": m.group(2)})
                elif out and ln.strip():
                    out[-1]["text"] += " " + ln.strip()
            break
    return out


def _first_paragraph(s):
    if not isinstance(s, str):
        return None
    paras = [p.strip() for p in re.split(r"\n\s*\n", s.strip()) if p.strip()]
    return " ".join(paras[0].split()) if paras else None


def _brief_target(rd: Reader, brief_path):
    """The brief file to read, or None when `brief_path` is not a relative briefs/<name>.md
    whose resolved location is inside <root>/briefs (absolute paths, "..", other folders,
    other suffixes and symlinks out of briefs/ are all refused)."""
    if not isinstance(brief_path, str) or not brief_path or "\x00" in brief_path:
        return None
    try:
        p = Path(brief_path)
        if p.is_absolute() or p.anchor or p.drive or ".." in p.parts:
            return None
        if len(p.parts) < 2 or p.parts[0] != "briefs" or p.suffix != ".md":
            return None
        full = (rd.root / p).resolve()
        full.relative_to((rd.root / "briefs").resolve())
    except (ValueError, OSError):
        return None
    return rd.root / p


def read_brief(rd: Reader, brief_path):
    """-> {"front", "purpose", "purpose_full", "outcomes", "fold", "symbols", "timeframe"}."""
    out = {"front": None, "purpose": None, "purpose_full": None, "outcomes": [],
           "fold": None, "symbols": None, "timeframe": None}
    if brief_path is None:
        return out
    target = _brief_target(rd, brief_path)
    if target is None:
        # the queue names something that is not briefs/<name>.md: read nothing
        out["purpose"] = out["purpose_full"] = _unr("brief_path outside briefs/")
        return out
    text = rd.text(target)
    front = parse_brief(text)
    if not front:
        return out
    out["front"] = front
    goal = front.get("research_goal")
    if isinstance(goal, str):
        out["purpose_full"] = " ".join(goal.split())
        out["purpose"] = _first_paragraph(goal)
    out["outcomes"] = parse_outcomes(front)
    proto = opt(front, "machine_constraints", "protocol")
    out["fold"] = opt(proto, "fold")
    out["symbols"] = opt(proto, "symbols")
    out["timeframe"] = front.get("timeframe")
    return out


def load_queue_doc(rd: Reader):
    doc = rd.yaml(rd.root / "config" / "campaign_queue.yaml")
    entries = [e for e in _as_list(opt(doc, "queue")) if isinstance(e, dict)]
    return entries


def entry_for_run(entries, run_id):
    for e in entries:
        if run_id in _as_list(e.get("run_ids")):
            return e
    return None


_LOG_TS = r"([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z?)"
_LAUNCH_RE = re.compile(r"^- " + _LOG_TS + r" LAUNCH-CARD (\S+) -> (run_[0-9]+)")
_DONE_RE = re.compile(r"^- " + _LOG_TS + r" DONE (\S+) \((run_[0-9]+)\)")


def log_lines(rd: Reader):
    t = rd.text(rd.root / "campaign_record" / "campaign_log.md")
    return t.splitlines() if isinstance(t, str) else []


def log_index(lines):
    """run_id -> {"launch": ts, "done": ts}."""
    idx = {}
    for ln in lines:
        m = _LAUNCH_RE.match(ln)
        if m:
            idx.setdefault(m.group(3), {})["launch"] = m.group(1)
            continue
        m = _DONE_RE.match(ln)
        if m:
            idx.setdefault(m.group(3), {})["done"] = m.group(1)
    return idx


def _parse_ts(s):
    if not isinstance(s, str):
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def run_log_lines(lines, run_id, entry_id):
    """Lines mentioning the run id or its entry id, from this run's LAUNCH-CARD to its DECIDE."""
    keys = [run_id] + ([entry_id] if entry_id else [])

    def mentions(ln):
        return any(k in ln for k in keys)

    start = None
    for i, ln in enumerate(lines):
        if "LAUNCH-CARD" in ln and run_id in ln:
            start = i
    if start is None:
        sel = [ln for ln in lines if run_id in ln]
        return [ln[:600] for ln in sel[:200]]
    end = len(lines) - 1
    for j in range(start, len(lines)):
        if " DECIDE " in lines[j] and mentions(lines[j]):
            end = j
            break
    sel = [ln for ln in lines[start:end + 1] if mentions(ln)]
    return [ln[:600] for ln in sel[:200]]


# --------------------------------------------------------------------------- run helpers


def list_run_ids(runs_dir):
    ids = []
    try:
        names = os.listdir(runs_dir)
    except OSError:
        return []
    for n in names:
        if RUN_ID_RE.match(n) and os.path.isdir(os.path.join(runs_dir, n)):
            ids.append(n)
    ids.sort(key=lambda s: int(s.split("_", 1)[1]), reverse=True)
    return ids


def run_exists(runs_dir, run_id) -> bool:
    return bool(RUN_ID_RE.match(str(run_id))) and os.path.isdir(os.path.join(runs_dir, run_id))


def _variants_index(rd: Reader):
    doc = rd.yaml(rd.run_path("artifacts/variants/index.yaml"))
    v = opt(doc, "variants")
    return v if isinstance(v, dict) else None


def list_variants(rd: Reader):
    idx = _variants_index(rd)
    if idx:
        return [k for k in idx.keys() if _safe_name(k)]
    patches = rd.yaml(rd.run_path("artifacts/variant_patches.yaml"))
    ids = [v.get("variant_id") for v in _as_list(opt(patches, "variants")) if isinstance(v, dict)]
    ids = [i for i in ids if isinstance(i, str) and _safe_name(i)]
    if ids:
        return ids
    return [d for d in rd.listdir(rd.run_path("artifacts/variants"))
            if _safe_name(d) and os.path.isdir(rd.run_path(f"artifacts/variants/{d}"))]


def _safe_name(s):
    return isinstance(s, str) and _SAFE_NAME_RE.match(s) is not None and ".." not in s


def window_map(rd: Reader, variant):
    """[{"label","symbol","window","stamp","index"}] in protocol_result order."""
    doc = rd.yaml(rd.run_path(f"artifacts/variants/{variant}/protocol_result.yaml"))
    results = [r for r in _as_list(opt(doc, "results")) if isinstance(r, dict)]
    counts = {}
    for r in results:
        counts[r.get("window")] = counts.get(r.get("window"), 0) + 1
    out = []
    for i, r in enumerate(results):
        w = r.get("window")
        if not isinstance(w, str):
            continue
        label = f"{r.get('symbol')}:{w}" if counts[w] > 1 else w
        out.append({"label": label, "symbol": r.get("symbol"), "window": w,
                    "stamp": r.get("run_id"), "index": i, "core": r.get("core")})
    return out


def list_windows(rd: Reader, variant):
    return [w["label"] for w in window_map(rd, variant)]


# --------------------------------------------------------------------------- pipeline state


def _pipeline(rd: Reader):
    ps = rd.yaml(rd.run_path("pipeline_state.yaml"))
    return ps if isinstance(ps, dict) else None


def _cost(ps):
    log = opt(ps, "audit_log")
    if not isinstance(log, dict):
        return None
    total = 0.0
    seen = False
    for rec in log.values():
        c = opt(rec, "cost_usd")
        if isinstance(c, (int, float)) and not isinstance(c, bool):
            total += c
            seen = True
    return round(total, 6) if seen else None


def _earliest_audit_ts(ps):
    log = opt(ps, "audit_log")
    if not isinstance(log, dict):
        return None
    ts = [opt(r, "timestamp") for r in log.values()]
    ts = [t for t in ts if isinstance(t, str) and _parse_ts(t)]
    return min(ts, key=lambda t: _parse_ts(t)) if ts else None


def _audit_rows(ps):
    rows = []
    log = opt(ps, "audit_log")
    if not isinstance(log, dict):
        return rows
    for key, rec in log.items():
        models = opt(rec, "models")
        if not isinstance(models, list):
            models = opt(rec, "provenance", "observed_models")
        if not isinstance(models, list):
            req_m = opt(rec, "provenance", "requested")
            models = [req_m] if req_m else []
        rows.append({
            "stage": key,
            "models": models,
            "cost_usd": opt(rec, "cost_usd"),
            "num_turns": opt(rec, "num_turns"),
            "tokens_total": opt(rec, "tokens", "total"),
            "execution_time_seconds": opt(rec, "execution_time_seconds"),
        })
    return rows


def _fold_from_trials(state_doc, run_id):
    for t in _as_list(opt(state_doc, "trial_sharpes")):
        if isinstance(t, dict) and str(t.get("trial_id", "")).startswith(run_id + ":") and t.get("fold"):
            return t["fold"]
    return None


def _coins(rd: Reader, brief):
    idx = _variants_index(rd)
    coins = []
    if idx:
        for v in idx.values():
            if not isinstance(v, dict):
                continue
            c = opt(v, "coverage", "venue_symbol") or v.get("symbol")
            if isinstance(c, str) and c not in coins:
                coins.append(c)
    if coins:
        return coins
    syms = brief.get("symbols")
    return [s for s in syms if isinstance(s, str)] if isinstance(syms, list) else None


def _bars_passed(pb):
    bars = opt(pb, "variants", "base", "bars")
    if not isinstance(bars, list):
        return None
    total = len(bars)
    passed = sum(1 for b in bars if isinstance(b, dict) and b.get("result") == "PASS")
    return {"passed": passed, "total": total}


# --------------------------------------------------------------------------- view 1


def _run_row(root, runs_dir, run_id, entries, state_doc, lidx):
    rd = Reader(root, runs_dir, run_id)
    ps = _pipeline(rd)
    idx = _variants_index(rd)
    pb = rd.yaml(rd.run_path("artifacts/profit_bars_evaluation.yaml"))
    pb_ok = isinstance(opt(pb, "variants"), dict)
    legacy = not (ps is not None and idx is not None and pb_ok)
    entry = entry_for_run(entries, run_id)
    brief = read_brief(rd, entry.get("brief_path") if entry else None)
    ist = rd.yaml(rd.run_path("artifacts/idea_status.yaml"))
    idea = opt(ist, "idea_status")
    if idea is None and ps is not None:
        idea = ps.get("pending_stage")
    fold = brief.get("fold") or _fold_from_trials(state_doc, run_id)
    tf = brief.get("timeframe")
    if tf is None and idx:
        for v in list(idx)[:1]:
            tf = opt(rd.yaml(rd.run_path(f"artifacts/variants/{v}/data_availability_gate.yaml")), "timeframe")
    li = lidx.get(run_id, {})
    launched = li.get("launch") or _earliest_audit_ts(ps)
    done = li.get("done")
    dur = None
    a, b = _parse_ts(launched), _parse_ts(done)
    if a and b:
        try:
            dur = round((b - a).total_seconds(), 1)
        except TypeError:
            dur = None
    return {
        "run_id": run_id,
        "entry_id": entry.get("id") if entry else None,
        "fold": fold,
        "coins": _coins(rd, brief),
        "timeframe": tf,
        "idea_status": idea,
        "outcome_letter": None,
        "outcome_note": "not recorded",
        "pre_registered_letters": [o["letter"] for o in brief["outcomes"]],
        "base_bars": _bars_passed(pb),
        "cost_usd": _cost(ps),
        "cost_label": COST_LABEL,
        "launched_at": launched,
        "done_at": done,
        "duration_seconds": dur,
        "status": opt(ps, "status"),
        "pending_stage": opt(ps, "pending_stage"),
        "legacy_shape": legacy,
    }


def _blocks(root):
    rd = Reader(root)
    path = rd.root / "campaign_record" / "block_registry.yaml"
    try:
        if str(_TOOLS_DIR) not in sys.path:
            sys.path.insert(0, str(_TOOLS_DIR))
        import block_registry  # tools/ sibling

        doc = block_registry.load_registry(path)
    except Exception as exc:  # noqa: BLE001 -- report, never crash
        return {"error": f"{type(exc).__name__} reading block_registry.yaml"}
    doc = _jsonable(doc)
    status = {}
    for rec in _as_list(doc.get("statuses")):
        if isinstance(rec, dict):
            status[rec.get("block_id")] = rec.get("status")
    blocks = []
    for b in _as_list(doc.get("blocks")):
        if not isinstance(b, dict):
            continue
        blocks.append({
            "block_id": b.get("block_id"),
            "validated_by_run": b.get("validated_by_run"),
            "hypothesis_id": b.get("hypothesis_id"),
            "kind": b.get("kind"),
            "status": status.get(b.get("block_id"), "active"),
        })
    return {"revision": doc.get("revision"), "blocks": blocks}


def load_campaign(root, runs_dir):
    """View 1: runs newest first, the queue, the block registry."""
    root = Path(root)
    rd = Reader(root, runs_dir)
    entries = load_queue_doc(rd)
    state_doc = rd.yaml(root / "campaign_record" / "campaign_state.yaml")
    lidx = log_index(log_lines(rd))
    rows = []
    for rid in list_run_ids(runs_dir):
        try:
            rows.append(_run_row(root, runs_dir, rid, entries, state_doc, lidx))
        except Exception as exc:  # noqa: BLE001 -- one bad run never blanks the view
            rows.append({"run_id": rid, "entry_id": None, "legacy_shape": True,
                         "row_error": f"unreadable ({type(exc).__name__})",
                         "outcome_letter": None, "outcome_note": "not recorded",
                         "cost_label": COST_LABEL})
    counts = {}
    queue = []
    for e in entries:
        st = str(e.get("status"))
        counts[st] = counts.get(st, 0) + 1
        if st == "ready" or st.startswith("blocked"):
            notes = e.get("notes")
            queue.append({
                "id": e.get("id"), "status": st, "priority": e.get("priority"),
                "notes": notes[:1000] if isinstance(notes, str) else notes,
                "brief_status_reason": e.get("brief_status_reason"),
            })
    return {
        "runs": rows,
        "queue": {"entries": queue, "counts": counts},
        "blocks": _blocks(root),
        "sources": rd.sources,
    }


# --------------------------------------------------------------------------- table helpers


def by_option_form(columns, rows, key_col, label_col=None):
    """The same table as {"by", "options", "rows_by_option"}: each option's rows as
    [label, value] pairs. A single row per option -> one pair per remaining column; several
    rows -> label = label_col cell, value = 'col=value | ...' of the other cells."""
    if key_col not in columns:
        return None
    ki = columns.index(key_col)
    li = columns.index(label_col) if label_col in columns else None
    options = []
    grouped = {}
    for r in rows:
        opt_v = fmt(r[ki])
        if opt_v not in grouped:
            grouped[opt_v] = []
            options.append(opt_v)
        grouped[opt_v].append(r)
    rbo = {}
    for o, rs in grouped.items():
        pairs = []
        if len(rs) == 1:
            r = rs[0]
            for i, c in enumerate(columns):
                if i != ki:
                    pairs.append([c, r[i]])
        else:
            for r in rs:
                others = [(c, r[i]) for i, c in enumerate(columns) if i not in (ki, li)]
                lab = fmt(r[li]) if li is not None else fmt(r[0])
                pairs.append([lab, " | ".join(f"{c}={fmt(v)}" for c, v in others)])
        rbo[o] = pairs
    return {"by": key_col, "options": options, "rows_by_option": rbo}


def mk_table(title, columns, rows, links=None, by=None, label=None, by_option=...):
    t = {"title": title, "columns": columns, "rows": rows}
    if links is not None:
        t["links"] = links
    if by_option is not ...:
        t["by_option"] = by_option
    else:
        t["by_option"] = by_option_form(columns, rows, by, label) if by else None
    return t


def kv_table(title, pairs):
    """A two-column (label, value) table; already in the selector-free shape."""
    return mk_table(title, ["label", "value"], [[k, v] for k, v in pairs], by_option=None)


# --------------------------------------------------------------------------- step framework


def _inside(path, base) -> bool:
    try:
        Path(path).resolve().relative_to(base)
        return True
    except (ValueError, OSError):
        return False


class Step:
    """One step's accumulating result."""

    def __init__(self, name, rd: Reader):
        self.name = name
        self.title = _TITLES[name]
        self.rd = rd
        self.status = "absent"
        self.headlines = []
        self.line = None
        self.tables = []
        self.text = []

    def head(self, label, value):
        self.headlines.append({"label": label, "value": value if isinstance(value, str) else fmt(value)})

    def table(self, *a, **kw):
        t = mk_table(*a, **kw)
        self.tables.append(t)
        return t

    def add_text(self, title, body, section=None):
        d = {"title": title, "body": body}
        if section:
            d["section"] = section
        self.text.append(d)

    def result(self):
        raw = []
        # raw embeds only this run's own files and the brief; the campaign-wide records
        # (log, state, memory, queue, block registry) stay listed in `sources` only
        run_base = (self.rd.runs_dir / (self.rd.run_id or "")).resolve()
        briefs_base = (self.rd.root / "briefs").resolve()
        for p in self.rd.present_paths():
            if p.endswith(".csv"):
                continue
            ap = self._abs(p)
            if ap is None or not (_inside(ap, run_base) or _inside(ap, briefs_base)):
                continue
            t = self.rd.text(ap)
            if isinstance(t, str):
                trunc = len(t) > RAW_CAP
                raw.append({"path": p, "text": t[:RAW_CAP], "truncated": trunc})
        bad = [r for r in self.rd.sources if r["state"] == "unreadable"]
        if bad and self.status != "unreadable":
            self.status = "unreadable"
            self.line = f"unreadable ({bad[0]['path']}: {bad[0].get('reason')})"
        return {
            "name": self.name, "title": self.title, "status": self.status,
            "headlines": self.headlines, "line": self.line, "sources": self.rd.sources,
            "tables": self.tables, "text": self.text, "raw": raw,
        }

    def _abs(self, disp):
        for base in (self.rd.root, self.rd.runs_dir.parent):
            p = base / disp
            if p.is_file():
                return p
        return None


def card_of(full):
    return {k: full[k] for k in ("name", "title", "status", "headlines", "line", "sources")}


def _cell_actual(b):
    return f"{fmt(b.get('actual'))} / {fmt(b.get('threshold'))} / {b.get('result')}"


def _link(variant, window=None):
    d = {"variant": variant}
    if window is not None:
        d["window"] = window
    return d


def _j(v):
    return json.dumps(_jsonable(v), separators=(",", ":"))


# --------------------------------------------------------------------------- the twelve steps


def _step_launch(s: Step, ctx):
    rd = s.rd
    entries = ctx["entries"]
    entry = ctx["entry"]
    ps = _pipeline(rd)
    brief = ctx["brief"]
    lines = ctx["log_lines"]
    li = [ln[:600] for ln in lines if (ctx["run_id"] in ln and ("LAUNCH-CARD" in ln or "VENUE-CHECK" in ln))]
    rd.yaml(rd.root / "config" / "campaign_queue.yaml")
    rd.text(rd.root / "campaign_record" / "campaign_log.md")
    if entry is not None:
        bt = _brief_target(rd, entry.get("brief_path"))
        if bt is not None:
            rd.text(bt)  # the brief is a source of this step (and the one non-run file its raw embeds)
    if entry is None and ps is None:
        s.status = "absent"
        s.line = "no queue entry and no pipeline_state.yaml for this run"
        return
    fold = brief.get("fold") or ctx["fold"]
    s.head("entry", entry.get("id") if entry else "absent (no queue entry names this run)")
    s.head("fold", fold)
    coins = ctx["coins"]
    s.head("coins x timeframe", f"{', '.join(coins) if coins else '-'} x {brief.get('timeframe') or ctx['timeframe'] or '-'}")
    status = opt(ps, "status")
    s.status = "ok" if (entry is not None and ps is not None) else "warn"
    s.line = f"pipeline status {fmt(status)}, stage {fmt(opt(ps, 'pending_stage'))}"
    if entry:
        s.table("Queue entry", ["label", "value"],
                [[k, fmt(entry.get(k))] for k in ("id", "status", "priority", "source", "relation",
                                                  "brief_path", "run_ids", "outcome", "title")
                 if k in entry], by_option=None)
    if ps:
        s.table("Pipeline state", ["label", "value"],
                [[k, fmt(ps.get(k))] for k in ("status", "current_stage", "pending_stage", "updated_at")]
                + [["completed_stages", ", ".join(map(str, _as_list(ps.get("completed_stages"))))],
                   ["stage_attempts", fmt(ps.get("stage_attempts"))]], by_option=None)
    if brief.get("purpose_full"):
        s.add_text("Brief: research goal", brief["purpose_full"])
    if brief["outcomes"]:
        s.table("Brief: pre-registered outcomes", ["letter", "text"],
                [[o["letter"], o["text"]] for o in brief["outcomes"]], by_option=None)
    if li:
        s.add_text("Campaign log: launch lines", "\n".join(li))


def _step_config(s: Step, ctx):
    rd = s.rd
    cand = rd.json(rd.run_path("artifacts/candidate_strategy_config.json"))
    spec = rd.yaml(rd.run_path("artifacts/backtest_spec.yaml"))
    dev = rd.yaml(rd.run_path("artifacts/deviations.yaml"))
    man = rd.yaml(rd.run_path("artifacts/block_manifest.yaml"))
    dec = rd.yaml(rd.run_path("artifacts/decision.yaml"))
    if cand is None and spec is None and dev is None and man is None:
        s.status = "absent"
        s.line = "no step-1b files"
        return
    hid = opt(spec, "hypothesis_id") or opt(dec, "hypothesis_id")
    if not hid:
        card = rd.yaml(rd.run_path("artifacts/hypothesis_card.yaml"))
        hid = opt(card, "hypothesis_id")
        if not hid:
            # absent files give "absent"; "unreadable" only when a file exists but lacks the key
            hid = "absent" if (spec is None and dec is None and card is None) else _unr(
                "missing key hypothesis_id (backtest_spec, decision, hypothesis_card)")
    s.head("hypothesis id", hid)
    devs = opt(dev, "deviations")
    dstatus = req(dev, "status") if dev is not None else "absent"
    s.head("deviations", f"{dstatus} ({len(devs) if isinstance(devs, list) else '?'} listed)")
    rat = opt(spec, "config_rationale")
    n_rat = len(rat) if isinstance(rat, list) else 0
    n_lines = len(_as_list(opt(dev, "config_rationale_lines")))
    s.head("rationale lines", f"{n_rat} config choices, {n_lines} deviation lines")
    if isinstance(dstatus, Unr):
        s.status = "unreadable"
        s.line = dstatus
    elif dstatus == "absent":
        s.status = "warn"
        s.line = "deviations.yaml absent; deviations not checked"
    elif dstatus != "exact" or (isinstance(devs, list) and devs):
        s.status = "warn"
        s.line = f"deviations status {dstatus}"
    else:
        s.status = "ok"
        s.line = opt(dec, "rationale") or "config written; no deviations"
    if isinstance(rat, list) and rat:
        s.table("Config rationale", ["hypothesis_claim", "config_choice"],
                [[opt(r, "hypothesis_claim"), opt(r, "config_choice")] for r in rat], by_option=None)
    if isinstance(man, dict):
        s.table("Block manifest", ["label", "value"],
                [["kind", opt(man, "block", "kind")],
                 ["config_paths", ", ".join(map(str, _as_list(opt(man, "block", "config_paths"))))],
                 ["scaffolding", ", ".join(map(str, _as_list(man.get("scaffolding"))))],
                 ["rationale", man.get("rationale")]], by_option=None)
    if isinstance(devs, list) and devs:
        s.table("Deviations", ["deviation"], [[fmt(d)] for d in devs], by_option=None)
    if cand is not None:
        s.add_text("Candidate strategy config (JSON)", json.dumps(cand, indent=2))


def _step_variants(s: Step, ctx):
    rd = s.rd
    patches = rd.yaml(rd.run_path("artifacts/variant_patches.yaml"))
    idx = _variants_index(rd)
    anti = rd.yaml(rd.run_path("artifacts/variant_anti_adjacency_result.yaml"))
    if patches is None and idx is None and anti is None:
        s.status = "absent"
        s.line = "no variant files"
        return
    plist = [v for v in _as_list(opt(patches, "variants")) if isinstance(v, dict)]
    ids = list(idx.keys()) if idx else [v.get("variant_id") for v in plist]
    kinds = {}
    for v in plist:
        kinds[v.get("kind")] = kinds.get(v.get("kind"), 0) + 1
    if not kinds and idx:
        for v in idx.values():
            k = opt(v, "kind")
            kinds[k] = kinds.get(k, 0) + 1
    avars = opt(anti, "variants")
    outcomes = {}
    if isinstance(avars, dict):
        for v in avars.values():
            o = opt(v, "outcome")
            outcomes[o] = outcomes.get(o, 0) + 1
    s.head("variants", len(ids))
    s.head("kinds", ", ".join(f"{k} x{n}" for k, n in kinds.items()) or "-")
    s.head("anti-adjacency", ", ".join(f"{k} x{n}" for k, n in outcomes.items()) if outcomes else
           ("unreadable (variant_anti_adjacency_result.yaml has no variants mapping)" if anti is not None else "absent"))
    not_novel = [k for k in outcomes if k != "novel"]
    not_valid = [k for k, v in (idx or {}).items() if opt(v, "status") != "validated"]
    if anti is None or idx is None or patches is None:
        s.status = "warn"
        s.line = "one of the three variant files is missing or unreadable"
    elif not_novel or not_valid:
        s.status = "warn"
        s.line = "anti-adjacency outcome other than novel, or a variant not validated"
    else:
        s.status = "ok"
        s.line = f"{len(ids)} variants admitted, all novel"
    if plist:
        rows = [[v.get("variant_id"), v.get("kind"), v.get("symbol"), _j(v.get("patch")), v.get("rationale")] for v in plist]
        s.table("Variant patches", ["variant_id", "kind", "symbol", "patch", "rationale"], rows,
                links=[_link(v.get("variant_id")) for v in plist], by="variant_id", label="kind")
    if idx:
        rows, links = [], []
        for k, v in idx.items():
            cov = opt(v, "coverage")
            rows.append([k, opt(v, "status"), opt(v, "kind"), opt(v, "symbol"),
                         opt(cov, "fraction") if cov else None,
                         ", ".join(map(str, _as_list(opt(cov, "windows_run")))) if cov else "",
                         ", ".join(map(str, _as_list(opt(cov, "uncovered")))) if cov else ""])
            links.append(_link(k))
        s.table("Variant index", ["variant", "status", "kind", "symbol", "coverage_fraction", "windows_run", "uncovered"],
                rows, links=links, by="variant")
    if isinstance(avars, dict):
        rows = [[k, opt(v, "outcome"), opt(v, "route"), opt(v, "layer"), "; ".join(map(str, _as_list(opt(v, "reasons"))))]
                for k, v in avars.items()]
        s.table("Anti-adjacency", ["variant", "outcome", "route", "layer", "reasons"], rows,
                links=[_link(k) for k in avars], by="variant")


def _gate_rows(rd, variants):
    out = []
    for v in variants:
        g = rd.yaml(rd.run_path(f"artifacts/variants/{v}/data_availability_gate.yaml"))
        out.append((v, g))
    return out


def _step_data_gate(s: Step, ctx):
    rd = s.rd
    variants = ctx["variants"]
    gates = _gate_rows(rd, variants)
    if all(g is None for _, g in gates):
        s.status = "absent"
        s.line = "no data_availability_gate.yaml for any variant"
        return
    rows, links = [], []
    per = []
    tot_ok = tot = 0
    any_valid_variant = False
    all_valid = True
    for v, g in gates:
        wins = [w for w in _as_list(opt(g, "windows")) if isinstance(w, dict)]
        ok = sum(1 for w in wins if w.get("outcome") == "validate")
        tot_ok += ok
        tot += len(wins)
        per.append(f"{v} {ok}/{len(wins)}" if g is not None else f"{v} absent")
        if g is None or opt(g, "outcome") != "validate" or ok != len(wins):
            all_valid = False
        if g is not None and ok > 0:
            any_valid_variant = True
        wl = set(list_windows(Reader(rd.root, rd.runs_dir, rd.run_id), v))
        for w in wins:
            rows.append([v, w.get("label"), w.get("symbol"), w.get("rows"), w.get("missing_fraction"),
                         w.get("outcome"), w.get("reason")])
            links.append(_link(v, w.get("label")) if w.get("label") in wl else _link(v))
    s.head("windows validated", f"{tot_ok}/{tot}")
    s.head("per variant", ", ".join(per))
    if all_valid:
        s.status, s.line = "ok", "every window of every variant validated"
    elif any_valid_variant:
        s.status, s.line = "warn", "some windows or variants did not validate"
    else:
        s.status, s.line = "fail", "no variant has a validated window"
    s.table("Data availability by window",
            ["variant", "window", "symbol", "rows", "missing_fraction", "outcome", "reason"],
            rows, links=links, by="variant", label="window")
    gate_rows = [[v, opt(g, "outcome"), "; ".join(map(str, _as_list(opt(g, "reasons")))), opt(g, "gap_tolerance"),
                  opt(g, "exchange"), opt(g, "timeframe")] for v, g in gates if g is not None]
    s.table("Gate outcome per variant", ["variant", "outcome", "reasons", "gap_tolerance", "exchange", "timeframe"],
            gate_rows, links=[_link(r[0]) for r in gate_rows], by="variant")


def _step_protocol(s: Step, ctx):
    rd = s.rd
    variants = ctx["variants"]
    docs = [(v, rd.yaml(rd.run_path(f"artifacts/variants/{v}/protocol_result.yaml"))) for v in variants]
    probe = rd.yaml(rd.run_path("artifacts/forecast_size_probe.yaml"))
    if all(d is None for _, d in docs):
        s.status = "absent"
        s.line = "no protocol_result.yaml for any variant"
        return
    rows, links = [], []
    per_trades = []
    n_win = 0
    fault = False
    missing = []
    for v, d in docs:
        if d is None:
            missing.append(v)
            per_trades.append(f"{v} absent")
            continue
        results = [r for r in _as_list(opt(d, "results")) if isinstance(r, dict)]
        wm = window_map(rd, v)
        labels = {w["index"]: w["label"] for w in wm}
        tr = 0
        for i, r in enumerate(results):
            core = _as_dict(r.get("core"))
            tc = core.get("trade_count")
            tr += tc if isinstance(tc, (int, float)) else 0
            n_win += 1
            if opt(r, "component_errors", "count") or r.get("nan_forecast"):
                fault = True
            label = labels.get(i)
            rows.append([v, label or r.get("window"), r.get("symbol"), tc, core.get("net_return_pct"),
                         core.get("sharpe"), core.get("max_drawdown_pct"), core.get("forecast_return_corr")])
            links.append(_link(v, label) if label else _link(v))
        per_trades.append(f"{v} {int(tr)}")
    s.head("trades per variant", ", ".join(per_trades))
    s.head("windows run", n_win)
    if fault:
        s.status, s.line = "fail", "component errors or NaN forecasts reported"
    elif missing:
        s.status, s.line = "warn", "no protocol result for: " + ", ".join(missing)
    else:
        s.status, s.line = "ok", f"{n_win} windows run"
    s.table("Protocol results by window",
            ["variant", "window", "symbol", "trade_count", "net_return_pct", "sharpe", "max_drawdown_pct",
             "forecast_return_corr"], rows, links=links, by="variant", label="window")
    probes = [p for p in _as_list(opt(probe, "probes")) if isinstance(p, dict)]
    if probes:
        s.table("Forecast size probe", ["variant", "stage", "status", "n_bars", "n_nan", "max_abs", "share_nonzero",
                                        "threshold"],
                [[p.get("variant_id"), p.get("stage"), p.get("status"), p.get("n_bars"), p.get("n_nan"),
                  p.get("max_abs"), p.get("share_nonzero"), p.get("threshold")] for p in probes],
                by="variant", label="stage")
    if missing:
        s.add_text("Variants without a protocol result",
                   ", ".join(missing) + " (gated out or not run)")


def _step_replay_gate(s: Step, ctx):
    rd = s.rd
    g = rd.yaml(rd.run_path("artifacts/config_replay_gate.yaml"))
    if g is None:
        s.status = "absent"
        s.line = "no config_replay_gate.yaml"
        return
    verdict = req(g, "verdict")
    series = opt(g, "series")
    series = series if isinstance(series, dict) else {}
    diff = sum(1 for v in series.values() if (opt(v, "forecast_or_regime_differences") or 0) > 0)
    s.head("verdict", verdict)
    s.head("series with differences", f"{diff}/{len(series)}")
    s.head("identical json", opt(g, "identical_json"))
    if isinstance(verdict, Unr):
        s.status, s.line = "unreadable", verdict
    elif verdict == "VALID":
        s.status, s.line = "ok", "replay matches the hand-written config"
    else:
        s.status, s.line = "fail", f"replay verdict {verdict}"
    s.table("Replay series", ["series", "bars", "differences", "nonzero_forecasts_brief", "required_bars"],
            [[k, opt(v, "bars"), opt(v, "forecast_or_regime_differences"), opt(v, "nonzero_forecasts_brief"),
              ", ".join(map(str, _as_list(opt(v, "required_bars"))))] for k, v in series.items()],
            by="series")


def _step_profit_bars(s: Step, ctx):
    rd = s.rd
    pb = rd.yaml(rd.run_path("artifacts/profit_bars_evaluation.yaml"))
    if pb is None:
        s.status = "absent"
        s.line = "no profit_bars_evaluation.yaml"
        return
    vs = req(pb, "variants")
    result = req(pb, "result")
    if isinstance(vs, Unr) or not isinstance(vs, dict):
        s.status, s.line = "unreadable", (vs if isinstance(vs, Unr) else _unr("variants is not a mapping"))
        return
    base = _bars_passed(pb)
    s.head("base bars passed", f"{base['passed']}/{base['total']}" if base else "unreadable (no base variant bars)")
    s.head("result per variant", ", ".join(f"{k} {opt(v, 'result')}" for k, v in vs.items()))
    dsr = opt(pb, "dsr_basis")
    if isinstance(dsr, dict):
        s.head("DSR trials", f"{dsr.get('n_trials')} (N={dsr.get('n_dsr_total')}, K={dsr.get('n_same_basis')})")
    if isinstance(result, Unr):
        s.status, s.line = "unreadable", result
    else:
        s.status = {"PASS": "ok", "FAIL": "fail"}.get(result, "warn")
        s.line = f"overall {result}; passing variants: {len(_as_list(opt(pb, 'passing')))}"
    names = []
    for v in vs.values():
        for b in _as_list(opt(v, "bars")):
            if isinstance(b, dict) and b.get("name") not in names:
                names.append(b.get("name"))
    vnames = list(vs.keys())
    rows = []
    for n in names:
        row = [n]
        for vn in vnames:
            b = next((b for b in _as_list(opt(vs[vn], "bars")) if isinstance(b, dict) and b.get("name") == n), None)
            row.append(_cell_actual(b) if b else "unreadable (bar missing)")
        rows.append(row)
    rows.append(["variant result"] + [fmt(opt(vs[vn], "result")) for vn in vnames])
    t = {"title": "Bars: actual / threshold / result", "columns": ["bar"] + vnames, "rows": rows,
         "links": [None] * len(rows)}
    t["by_option"] = {"by": "variant", "options": vnames,
                      "rows_by_option": {vn: [[r[0], r[i + 1]] for r in rows] for i, vn in enumerate(vnames)}}
    t["column_links"] = [None] + [_link(vn) for vn in vnames]
    s.tables.append(t)
    if isinstance(dsr, dict):
        s.table("Deflated Sharpe basis", ["label", "value"], [[k, fmt(v)] for k, v in dsr.items()
                                                              if not isinstance(v, dict)], by_option=None)
    fs_keys = []
    for v in vs.values():
        for k in _as_dict(opt(v, "forecast_shape")):
            if k not in fs_keys:
                fs_keys.append(k)
    if fs_keys:
        s.table("Forecast shape", ["metric"] + vnames,
                [[k] + [opt(vs[vn], "forecast_shape", k) for vn in vnames] for k in fs_keys], by_option=None)
        t = s.tables[-1]
        t["by_option"] = {"by": "variant", "options": vnames,
                          "rows_by_option": {vn: [[r[0], r[i + 1]] for r in t["rows"]] for i, vn in enumerate(vnames)}}
    brows = []
    for vn in vnames:
        for b in _as_list(opt(vs[vn], "bars")):
            if isinstance(b, dict):
                brows.append([vn, b.get("name"), b.get("comparator"), b.get("basis"), b.get("note")])
    if brows:
        s.table("Bar basis and notes", ["variant", "bar", "comparator", "basis", "note"], brows,
                links=[_link(r[0]) for r in brows], by="variant", label="bar")
    rrows = [[vn, "; ".join(map(str, _as_list(opt(vs[vn], "reasons"))))] for vn in vnames]
    s.table("Failing bars per variant", ["variant", "reasons"], rrows, by="variant")


def _step_grid(s: Step, ctx):
    rd = s.rd
    grid = rd.yaml(rd.run_path("artifacts/grid_evaluation.yaml"))
    ric = rd.yaml(rd.run_path("artifacts/residual_ic.yaml"))
    ist = rd.yaml(rd.run_path("artifacts/idea_status.yaml"))
    if grid is None and ist is None and ric is None:
        s.status = "absent"
        s.line = "no grid_evaluation.yaml, residual_ic.yaml or idea_status.yaml"
        return
    idea = req(ist, "idea_status") if ist is not None else (req(grid, "idea_status") if grid is not None else "absent")
    g = opt(grid, "grid")
    g = g if isinstance(g, dict) else {}
    cells = fails = incon = 0
    rows, links = [], []
    for crit, per in g.items():
        if not isinstance(per, dict):
            continue
        for vn, c in per.items():
            c = _as_dict(c)
            cells += 1
            fails += c.get("result") == "FAIL"
            incon += c.get("result") == "INCONCLUSIVE"
            rows.append([crit, vn, c.get("value"), c.get("threshold"), c.get("comparator"), c.get("result"),
                         c.get("n_windows"), c.get("n_trades"), c.get("reason")])
            links.append(_link(vn))
    s.head("idea_status", idea)
    s.head("FAIL cells", f"{fails}/{cells}" + (f" ({incon} inconclusive)" if incon else ""))
    if isinstance(idea, Unr):
        s.status, s.line = "unreadable", idea
    else:
        s.status = {"refuted": "fail", "validated": "ok"}.get(idea, "warn")
        s.line = opt(ist, "reason") or opt(grid, "reason") or f"idea_status {idea}"
    s.table("Criteria grid", ["criterion", "variant", "value", "threshold", "comparator", "result", "n_windows",
                              "n_trades", "reason"], rows, links=links, by="variant", label="criterion")
    rv = opt(ric, "variants")
    if isinstance(rv, dict):
        s.table("Residual IC", ["variant", "value", "p_value_one_sided", "correlation_to_composite", "n_eff",
                                "n_bars", "fully_explained"],
                [[vn, opt(v, "value"), opt(v, "p_value_one_sided"), opt(v, "correlation_to_composite"),
                  opt(v, "n_eff"), opt(v, "n_bars"), opt(v, "fully_explained")] for vn, v in rv.items()],
                links=[_link(vn) for vn in rv], by="variant")
        ids = opt(ric, "composite", "block_ids")
        s.add_text("Residual IC composite", "block_ids: " + (", ".join(map(str, ids)) if isinstance(ids, list) else "-")
                   + f"\nkind: {fmt(opt(ric, 'composite', 'kind'))}; method: "
                   + fmt(next((opt(v, 'method') for v in rv.values()), None)))
    elif ric is not None:
        s.add_text("Residual IC", fmt(opt(ric, "skipped")) if opt(ric, "skipped") else "unreadable (variants is not a mapping)")
    if ist is not None:
        s.table("Idea status", ["label", "value"], [[k, fmt(opt(ist, k))] for k in
                ("idea_status", "result", "hypothesis_verdict", "lineage_routing", "reason")], by_option=None)


def _step_claims(s: Step, ctx):
    rd = s.rd
    meas = rd.yaml(rd.run_path("artifacts/claim_measurement.yaml"))
    dig = rd.yaml(rd.run_path("artifacts/claim_result_digest.yaml"))
    fs = rd.yaml(rd.run_path("artifacts/findings_summary.yaml"))
    cts = [(v, rd.yaml(rd.run_path(f"artifacts/variants/{v}/claim_test.yaml"))) for v in ctx["variants"]]
    if meas is None and dig is None and fs is None and all(c is None for _, c in cts):
        s.status = "absent"
        s.line = "no claim files"
        return
    cstat = req(meas, "claim_status") if meas is not None else (req(dig, "claim_status") if dig is not None else "absent")
    tests = [t for t in _as_list(opt(meas, "tests")) if isinstance(t, dict)]
    measured = opt(meas, "n_tests_measured")
    s.head("claim_status", cstat)
    s.head("tests measured", f"{measured if measured is not None else '?'}/{len(tests) if tests else '?'}")
    if fs is not None:
        s.head("findings", opt(fs, "n_findings"))
    if isinstance(cstat, Unr):
        s.status, s.line = "unreadable", cstat
    elif cstat == "measured":
        s.status, s.line = "ok", opt(meas, "label") or "claims measured"
    else:
        s.status, s.line = "warn", f"claim_status {cstat}"
    if tests:
        s.table("Claim tests by variant", ["variant", "test", "status", "spec_hash"],
                [[t.get("variant"), t.get("test"), t.get("status"), t.get("spec_hash")] for t in tests],
                links=[_link(t.get("variant")) if _safe_name(t.get("variant")) else None for t in tests],
                by="variant", label="test")
    rows = []
    for v, c in cts:
        if c is None:
            continue
        td = opt(c, "tests")
        for tn, t in (td.items() if isinstance(td, dict) else []):
            rows.append([v, tn, opt(t, "status"), opt(t, "outcome"), opt(t, "label"), opt(t, "statistic"),
                         opt(t, "direction"), len(_as_list(opt(t, "floor_not_met")))])
    if rows:
        s.table("Per-variant claim test detail", ["variant", "test", "status", "outcome", "label", "statistic",
                                                  "direction", "floors_not_met"], rows,
                links=[_link(r[0]) for r in rows], by="variant", label="test")
    if dig is not None:
        st = opt(dig, "statement")
        if isinstance(st, str):
            s.add_text("Claim statement", st)
        n = opt(dig, "statistics_note")
        if isinstance(n, str):
            s.add_text("Statistics note", n)


def _lens_blocks(s: Step, rd: Reader, an_dir, q_dir, section=None, prefix=""):
    lenses = [f[:-5] for f in rd.listdir(rd.run_path(an_dir)) if f.endswith(".yaml") and _safe_name(f[:-5])]
    lrows, qrows = [], []
    texts = []
    tot_cost = 0.0
    tot_turns = 0
    outcomes = []
    status = "ok"
    for lens in lenses:
        d = rd.yaml(rd.run_path(f"{an_dir}/{lens}.yaml"))
        q = rd.yaml(rd.run_path(f"{q_dir}/{lens}.yaml"))
        if d is None:
            status = "warn" if status == "ok" else status
            continue
        att = [a for a in _as_list(opt(d, "attempts")) if isinstance(a, dict)]
        cost = sum(a["cost_usd"] for a in att if isinstance(a.get("cost_usd"), (int, float)))
        turns = sum(a["num_turns"] for a in att if isinstance(a.get("num_turns"), (int, float)))
        tot_cost += cost
        tot_turns += turns
        outcome = req(d, "outcome")
        outcomes.append(f"{lens}: {outcome}")
        if isinstance(outcome, Unr):
            status = "unreadable"
        elif att and att[-1].get("status") != "accepted" or opt(d, "outcome_flipped_on_retry"):
            status = "warn" if status == "ok" else status
        claim = opt(d, "claim")
        nc = opt(d, "no_claim")
        br = opt(nc, "best_rejected")
        obs = [o for o in _as_list(opt(nc, "observations")) if isinstance(o, dict)]
        summary = (opt(claim, "statement") if isinstance(claim, dict) else None) or opt(nc, "reason")
        lrows.append([lens, outcome, summary, opt(br, "statement"), len(obs), round(cost, 6), turns,
                      opt(d, "model"), opt(d, "outcome_flipped_on_retry")])
        if opt(nc, "reason"):
            texts.append((f"{prefix}{lens}: no_claim reason", str(nc["reason"])))
        if isinstance(claim, dict) and claim.get("statement"):
            texts.append((f"{prefix}{lens}: claim", str(claim["statement"])))
        if br:
            texts.append((f"{prefix}{lens}: best rejected", fmt(br)))
        for i, o in enumerate(obs):
            texts.append((f"{prefix}{lens}: observation {i + 1}", str(o.get("statement", fmt(o))).strip()))
        for qq in [x for x in _as_list(opt(q, "queries")) if isinstance(x, dict)]:
            qrows.append([lens, qq.get("id"), qq.get("function"), _j(qq.get("params")), qq.get("status"),
                          qq.get("n_comparisons"), qq.get("digest")])
    t1 = mk_table(prefix + "Lenses", ["lens", "outcome", "claim or no_claim reason", "best_rejected", "observations",
                                      "cost_usd", "num_turns", "model", "flipped_on_retry"], lrows, by="lens")
    t2 = mk_table(prefix + "Queries", ["lens", "id", "function", "params", "status", "n_comparisons", "digest"],
                  qrows, by="lens", label="id")
    if section:
        t1["section"] = section
        t2["section"] = section
    return {"lenses": lenses, "tables": [t1, t2], "texts": texts, "cost": tot_cost, "turns": tot_turns,
            "outcomes": outcomes, "status": status, "n_queries": len(qrows)}


def _step_analyst(s: Step, ctx):
    rd = s.rd
    main = _lens_blocks(s, rd, "artifacts/analyst", "artifacts/analyst_queries")
    rerun_dir = rd.run_path("artifacts/analyst_rerun")
    has_rerun = os.path.isdir(rerun_dir)
    if not main["lenses"] and not has_rerun:
        s.status = "absent"
        s.line = "no analyst lens files"
        return
    s.head("outcome per lens", ", ".join(main["outcomes"]) or "-")
    s.head("queries", main["n_queries"])
    s.head("cost", f"${main['cost']:.4f} over {int(main['turns'])} turns")
    s.status = main["status"] if main["lenses"] else "absent"
    s.line = "; ".join(main["outcomes"]) if main["outcomes"] else "no lens file read"
    s.tables.extend(main["tables"])
    for title, body in main["texts"]:
        s.add_text(title, body)
    if has_rerun:
        sec = "re-run on a copy"
        rr = _lens_blocks(s, rd, "artifacts/analyst_rerun", "artifacts/analyst_rerun/analyst_queries",
                          section=sec, prefix=sec + ": ")
        if rr["lenses"]:
            s.line += "; re-run on a copy present"
            s.tables.extend(rr["tables"])
            for title, body in rr["texts"]:
                s.add_text(title, body, section=sec)
        readme = rd.text(rd.run_path("artifacts/analyst_rerun/README.md"))
        if isinstance(readme, str):
            s.add_text(sec + ": README", readme, section=sec)


def _step_decide_next(s: Step, ctx):
    rd = s.rd
    d = rd.yaml(rd.run_path("artifacts/decision_record.yaml"))
    rd.text(rd.root / "campaign_record" / "campaign_log.md")
    if d is None:
        s.status = "absent"
        s.line = "no decision_record.yaml"
        return
    cands = [c for c in _as_list(opt(d, "candidates")) if isinstance(c, dict)]
    picked = d.get("picked", _unr("missing key picked"))
    if isinstance(picked, dict):  # an R2 request rather than a candidate
        picked = "R2 request: " + str(picked.get("queue_entry_id") or picked.get("r2_request") or "?")
    elig = sum(1 for c in cands if c.get("eligible") is True)
    s.head("candidates", len(cands))
    s.head("eligible", elig)
    s.head("picked", picked if picked else f"none ({fmt(opt(d, 'stop', 'reason'))})")
    if isinstance(picked, Unr):
        s.status, s.line = "unreadable", picked
    elif picked:
        s.status, s.line = "ok", f"picked {picked}"
    else:
        s.status, s.line = "warn", fmt(opt(d, "stop", "reason")) + ": " + fmt(opt(d, "stop", "detail"))
    rows = []
    for c in cands:
        reasons = []
        for gname, g in _as_dict(c.get("gates")).items():
            if isinstance(g, dict):
                for r in _as_list(g.get("reasons")):
                    reasons.append(f"{gname}: {r}")
        rows.append([c.get("candidate_id"), c.get("origin"), c.get("kind"), c.get("eligible"),
                     " | ".join(reasons), bool(picked) and c.get("candidate_id") == picked])
    s.table("Candidates", ["candidate_id", "origin", "kind", "eligible", "reasons", "picked"], rows,
            by="kind", label="candidate_id")
    s.table("Decision record", ["label", "value"],
            [["decided_at", fmt(d.get("decided_at"))], ["after_run", fmt(opt(d, "trigger", "after_run"))],
             ["after_entry", fmt(opt(d, "trigger", "after_entry"))], ["idea_status", fmt(opt(d, "trigger", "idea_status"))],
             ["picked", fmt(picked)], ["stop reason", fmt(opt(d, "stop", "reason"))],
             ["stop detail", fmt(opt(d, "stop", "detail"))]], by_option=None)
    dl = [ln[:900] for ln in ctx["log_lines"] if " DECIDE " in ln and ctx["run_id"] in ln]
    if dl:
        s.add_text("Campaign log: DECIDE line", "\n".join(dl))


def _step_record(s: Step, ctx):
    rd = s.rd
    summ = rd.yaml(rd.run_path("artifacts/registry_summary.yaml"))
    tried = rd.yaml(rd.run_path("artifacts/tried_ideas.yaml"))
    state_doc = rd.yaml(rd.root / "campaign_record" / "campaign_state.yaml")
    mem = rd.yaml(rd.root / "campaign_record" / "campaign_memory.yaml")
    reg = rd.yaml(rd.root / "campaign_record" / "block_registry.yaml")
    rd.text(rd.root / "campaign_record" / "campaign_log.md")
    rid = ctx["run_id"]
    trials = [t for t in _as_list(opt(state_doc, "trial_sharpes"))
              if isinstance(t, dict) and str(t.get("trial_id", "")).startswith(rid + ":")]
    mentry = opt(mem, "runs", rid)
    blocks = [b for b in _as_list(opt(reg, "blocks")) if isinstance(b, dict) and b.get("validated_by_run") == rid]
    done = [ln[:600] for ln in ctx["log_lines"] if " DONE " in ln and f"({rid})" in ln]
    have = [summ is not None, bool(trials), isinstance(mentry, dict)]
    if not any(have) and not tried:
        s.status = "absent"
        s.line = "no registry summary, trial rows or memory entry"
        return
    s.head("trial rows", len(trials))
    s.head("blocks registered by this run", len(blocks))
    s.head("idea_status", opt(summ, "this_run", "idea_status") or opt(mentry, "idea_status"))
    s.status = "ok" if all(have) else "warn"
    s.line = (done[0] if done else "no DONE line in the campaign log")
    if trials:
        rows = [[t.get("trial_id"), t.get("sharpe"), t.get("expectancy_bps"), t.get("n_trades"),
                 t.get("statistic_valid"), t.get("below_floor_pct"), t.get("fold"),
                 ", ".join(map(str, _as_list(t.get("symbols"))))] for t in trials]
        s.table("Trial rows", ["trial_id", "sharpe", "expectancy_bps", "n_trades", "statistic_valid",
                               "below_floor_pct", "fold", "symbols"], rows,
                links=[_link(str(t["trial_id"]).split(":", 1)[1]) if ":" in str(t["trial_id"]) and
                       _safe_name(str(t["trial_id"]).split(":", 1)[1]) else None for t in trials],
                by="trial_id")
    if isinstance(mentry, dict):
        s.table("Campaign memory entry", ["label", "value"],
                [[k, fmt(v)] for k, v in mentry.items() if not isinstance(v, (dict, list))], by_option=None)
    if blocks:
        s.table("Blocks registered by this run", ["block_id", "kind", "hypothesis_id", "timeframe"],
                [[b.get("block_id"), b.get("kind"), b.get("hypothesis_id"), b.get("timeframe")] for b in blocks],
                by="block_id")
    rs = opt(summ, "registry")
    if isinstance(rs, dict):
        s.table("Registry summary", ["label", "value"], [[k, fmt(v)] for k, v in rs.items()], by_option=None)
    tr = [r for r in _as_list(opt(tried, "runs")) if isinstance(r, dict)]
    if tr:
        s.table("Tried ideas (recent runs)", ["run_id", "hypothesis_id", "symbols", "timeframe", "idea_status",
                                              "variants_tested"],
                [[r.get("run_id"), r.get("hypothesis_id"), ", ".join(map(str, _as_list(r.get("symbols")))),
                  r.get("timeframe"), r.get("idea_status"), r.get("variants_tested")] for r in tr],
                by="idea_status", label="run_id")
    if done:
        s.add_text("Campaign log: DONE line", "\n".join(done))


_STEP_FUNCS = {
    "launch": _step_launch, "config": _step_config, "variants": _step_variants,
    "data_gate": _step_data_gate, "protocol": _step_protocol, "replay_gate": _step_replay_gate,
    "profit_bars": _step_profit_bars, "grid": _step_grid, "claims": _step_claims,
    "analyst": _step_analyst, "decide_next": _step_decide_next, "record": _step_record,
}


def _run_ctx(root, runs_dir, run_id):
    rd0 = Reader(root, runs_dir, run_id)
    entries = load_queue_doc(rd0)
    entry = entry_for_run(entries, run_id)
    brief = read_brief(rd0, entry.get("brief_path") if entry else None)
    state_doc = rd0.yaml(Path(root) / "campaign_record" / "campaign_state.yaml")
    lines = log_lines(rd0)
    idx = _variants_index(rd0)
    return {
        "run_id": run_id, "entries": entries, "entry": entry, "brief": brief,
        "fold": _fold_from_trials(state_doc, run_id), "coins": _coins(rd0, brief),
        "timeframe": brief.get("timeframe"), "log_lines": lines,
        "variants": list_variants(rd0),
        "_rd0": rd0, "_idx": idx,
    }


def build_step(root, runs_dir, run_id, name, ctx=None):
    """The full step document (card fields + tables/text/raw). Never raises."""
    ctx = ctx or _run_ctx(root, runs_dir, run_id)
    rd = Reader(root, runs_dir, run_id)
    s = Step(name, rd)
    try:
        _STEP_FUNCS[name](s, ctx)
    except Exception as exc:  # noqa: BLE001 -- one step's bug never blanks the run
        s.status = "unreadable"
        s.line = f"unreadable ({type(exc).__name__}: {str(exc)[:200]})"
    return s.result()


# --------------------------------------------------------------------------- view 2 / 3


def load_run(root, runs_dir, run_id):
    """View 2: header + the twelve step cards."""
    root = Path(root)
    ctx = _run_ctx(root, runs_dir, run_id)
    rd = Reader(root, runs_dir, run_id)
    ps = _pipeline(rd)
    entry = ctx["entry"]
    brief = ctx["brief"]
    steps = [card_of(build_step(root, runs_dir, run_id, n, ctx)) for n in STEP_NAMES]
    header = {
        "run_id": run_id,
        "entry_id": entry.get("id") if entry else None,
        "status": opt(ps, "status"),
        "pending_stage": opt(ps, "pending_stage"),
        "completed_stages": opt(ps, "completed_stages"),
        "cost_usd": _cost(ps),
        "cost_label": COST_LABEL,
        "audit": _audit_rows(ps),
        "stage_attempts": opt(ps, "stage_attempts"),
        "purpose": brief.get("purpose"),
        "purpose_full": brief.get("purpose_full"),
        "outcomes": brief.get("outcomes"),
        "outcome_letter": None,
        "outcome_note": "not recorded",
        "campaign_log": run_log_lines(ctx["log_lines"], run_id, entry.get("id") if entry else None),
        "variants": ctx["variants"],
    }
    sources = list(rd.sources) + list(ctx["_rd0"].sources)
    return {"header": header, "steps": steps, "sources": _dedupe_sources(sources)}


def _dedupe_sources(srcs):
    seen, out = set(), []
    for r in srcs:
        if r["path"] not in seen:
            seen.add(r["path"])
            out.append(r)
    return out


def load_step(root, runs_dir, run_id, name):
    """View 3: the card plus tables / text / raw."""
    return build_step(root, runs_dir, run_id, name)


# --------------------------------------------------------------------------- view 4


def _window_paths(rd: Reader, variant, w):
    stamp = w.get("stamp")
    if not isinstance(stamp, str) or not _STAMP_RE.match(stamp):
        return None
    base = rd.run_path(f"variants/{variant}/results/{stamp}")
    return base / "bars.csv", base / "trades.json"


def load_bars(root, runs_dir, run_id, variant, label):
    rd = Reader(root, runs_dir, run_id)
    wm = {w["label"]: w for w in window_map(rd, variant)}
    w = wm.get(label)
    out = {"variant": variant, "label": label, "symbol": opt(w, "symbol"), "window": opt(w, "window"),
           "columns": {k: None for k in BAR_COLUMNS}, "n_bars": None, "trades": None,
           "metrics": opt(w, "core"), "sources": rd.sources}
    if w is None:
        return out
    paths = _window_paths(rd, variant, w)
    if paths is None:
        return out
    bars_p, trades_p = paths
    cols = _read_bars_csv(rd, bars_p)
    if cols is not None:
        out["columns"] = cols
        ts = cols.get("timestamp") or cols.get("close") or []
        out["n_bars"] = len(ts)
    trades = rd.json(trades_p)
    if isinstance(trades, list):
        out["trades"] = [{k: t.get(k) for k in TRADE_FIELDS} for t in trades if isinstance(t, dict)]
    return out


def load_equity(root, runs_dir, run_id, variant):
    rd = Reader(root, runs_dir, run_id)
    windows = []
    prev_end = 1.0
    for w in window_map(rd, variant):
        paths = _window_paths(rd, variant, w)
        cols = _read_bars_csv(rd, paths[0]) if paths else None
        pv = cols.get("portfolio_value") if cols else None
        ts = cols.get("timestamp") if cols else None
        entry = {"label": w["label"], "symbol": w["symbol"], "timestamps": None, "equity": None}
        if pv and ts and len(pv) == len(ts):
            first = next((v for v in pv if isinstance(v, (int, float)) and v), None)
            if first:
                eq = [None if v is None else (v / first) * prev_end for v in pv]
                entry["timestamps"] = ts
                entry["equity"] = eq
                last = next((v for v in reversed(eq) if v is not None), None)
                if last is not None:
                    prev_end = last
        windows.append(entry)
    return {"variant": variant, "start": 1.0, "windows": windows, "sources": rd.sources}
