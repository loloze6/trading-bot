"""
The "current composite" forecast series that a candidate block's residual IC
is measured against (E-060 S2, delivery_plan_v26.md slice 7 item 7.1; spec:
engineering/roadmap/E-060/S1_FINDINGS.md §2, guesses 4 and 5, and operator
decision 3). Used only under orchestrator.composition_runs.

Which composite (guess 4, per exact timeframe -- operator decision 3: until the
engine supports mixed bar sizes, only blocks with the SAME exact bar size are
ever combined, so a candidate is compared with the forecast blocks registered
on its own bar size):
  * no forecast block on this timeframe  -> kind `none`: no composite, the
    residual IC is the candidate's own IC;
  * one                                  -> kind `block`: that block's own
    tested base config (its registry `source_config_ref`);
  * two or more                          -> kind `composition`: the base
    (equal-weight) variant config of the composition run recorded for exactly
    this set of blocks in campaign_record/compositions.yaml; none recorded ->
    kind `stale` and the residual-IC cell is INCONCLUSIVE ("composite is
    stale").
Regime blocks are not forecasts and never enter the composite (7.4 is later).
A forecast block registered without a `timeframe` (the registry keeps no
timeframe with the flag off -- adding one there would change the flag-off
registry bytes) cannot be placed: it is EXCLUDED with a loud line and listed
in `excluded_blocks`, never allowed to break composition on any timeframe.
The registry is append-only; nothing here edits it.

The set of blocks is identified by `registry_hash` (composite_registry_hash):
sha256 over the sorted (block_id, source_config_sha256) pairs of exactly those
blocks, so a block registered on ANOTHER timeframe does not make this
timeframe's composite stale. S3's composition writer must record the same hash
(`registry_hash`), its base variant's config (`base_config_ref`) and that
config's canonical sha256 (`base_config_sha256`, required) in each
compositions.yaml entry: that is this module's read contract.

Where it is measured (guess 5): on the candidate's own coins and windows --
the composite config is run through tools/run_protocol.py with the
CANDIDATE's protocol file. Cached under
campaign_record/composite/<registry_hash>/<config8>_<protocol8>_<engine8>_<data8>/
where engine8 is the git sha the candidate's windows were run with and data8
hashes the candidate windows' OHLCV data_sha256 values (their manifest.json):
a change of engine or of market data is a different cache entry. After a run
the composite's own window manifests must show that same git sha and the same
data_sha256 per (symbol, window) -- else CompositeError (the two series would
not be comparable). Cache writes hold a lock (campaign_memory's primitive), so
two misses never race on one directory; a hit whose results/ bars files are
gone is recomputed.

What it is not:
  * not a trial -- tools/run_protocol.py writes no trial row (only
    run_phase1_research._record_backtest_trial does), and nothing here calls
    that; the cache directory is outside runs/;
  * not graded -- no pass rule, no profit bars, no grid; its protocol run is
    started without --validation-protocol;
  * never the holdout -- --holdout is never passed, every protocol window must
    carry real ISO test dates that lie wholly outside the sealed range (the
    caller passes run_phase1_research._load_holdout_range() and its
    HoldoutBoundaryBreach), failing closed, and a path under
    local_data/holdout_sealed is refused.

No lookahead: the composite forecast at bar t is the engine's output for bar
t, computed from data up to t's close exactly as for any backtest; this
module only runs it and reads its bars.csv. The residual that uses it is
past-only by construction (tools/residual_ic.py).
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

import residual_ic as _ric  # tools/ sibling (also puts trading-bot/ on sys.path)
import timeframe as _tf  # tools/ sibling: the one timeframe parser
import holdout_policy as _holdout_policy  # tools/ sibling: the one holdout_range / day parser (CUL-339)

SCHEMA_VERSION = 1
COMPOSITE_META_FILENAME = "composite.yaml"
COMPOSITE_LOCK_FILENAME = ".composite.lock"
# A composite protocol run is a full backtest; a second miss waits this long for it.
COMPOSITE_LOCK_WAIT_SECONDS = 3600.0
KIND_NONE, KIND_BLOCK, KIND_COMPOSITION, KIND_STALE = "none", "block", "composition", "stale"
_RUN_PROTOCOL = Path(__file__).resolve().parent / "run_protocol.py"
_SEALED_DIR_NAME = "holdout_sealed"

# Operator decision 3, by bar length in seconds.
TIMEFRAME_CATEGORIES = ("high", "medium", "low", "daily")


class CompositeError(ValueError):
    """A registry block, a compositions entry, a config or a protocol cannot
    be used to build the composite. Never caught here."""


def timeframe_category(timeframe) -> str:
    """high: bar <= 15 min; medium: 15 min < bar < 1 h; low: 1 h <= bar < 1 day;
    daily: bar >= 1 day. Unparseable timeframes raise (tools/timeframe.py)."""
    secs = _tf.timeframe_seconds(timeframe)
    if secs <= 15 * 60:
        return "high"
    if secs < 3600:
        return "medium"
    if secs < 86400:
        return "low"
    return "daily"


def forecast_blocks_on_timeframe(registry_doc: dict, timeframe) -> tuple:
    """(blocks, excluded): registry forecast blocks whose exact bar size
    equals `timeframe` (compared in seconds, so "60m" == "1h"), and
    [{block_id, reason}] for forecast blocks that cannot be placed because
    they carry no timeframe (printed loudly, never raised)."""
    want = _tf.timeframe_seconds(timeframe)
    out, excluded = [], []
    for block in registry_doc.get("blocks") or []:
        if block.get("kind") != "forecast":
            continue
        tf = block.get("timeframe")
        if tf is None:
            reason = ("no timeframe recorded (registered with orchestrator.composition_runs off) "
                      "-- excluded from every per-timeframe composite")
            print(f"WARNING [E-060] composite: registry block {block.get('block_id')!r} {reason}")
            excluded.append({"block_id": block.get("block_id"), "reason": reason})
            continue
        if _tf.timeframe_seconds(tf) == want:
            out.append(block)
    return out, excluded


def composite_registry_hash(blocks: list) -> str:
    """First 16 hex chars of sha256 over the sorted [block_id,
    source_config_sha256] pairs -- the identity of one composite's block set."""
    pairs = sorted([b["block_id"], b["source_config_sha256"]] for b in blocks)
    return hashlib.sha256(json.dumps(pairs).encode("utf-8")).hexdigest()[:16]


def load_compositions(path: Path) -> list:
    """campaign_record/compositions.yaml's `compositions` list ([] when the
    file is absent; S3 writes it). Malformed raises."""
    path = Path(path)
    if not path.exists():
        return []
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise CompositeError(f"{path}: unparseable YAML ({exc})") from exc
    if not isinstance(doc, dict) or not isinstance(doc.get("compositions"), list):
        raise CompositeError(f"{path}: expected a mapping with a `compositions` list")
    return doc["compositions"]


def resolve_current_composite(registry_doc: dict, compositions: list, timeframe) -> dict:
    """Guess 4 for one timeframe. Returns {kind, timeframe, registry_hash,
    block_ids, excluded_blocks, config_ref, expected_config_sha256, reason}."""
    blocks, excluded = forecast_blocks_on_timeframe(registry_doc, timeframe)
    out = {"kind": KIND_NONE, "timeframe": timeframe, "registry_hash": None,
           "block_ids": [b["block_id"] for b in blocks], "excluded_blocks": excluded,
           "config_ref": None, "expected_config_sha256": None, "reason": None}
    if not blocks:
        out["reason"] = f"no forecast block registered on timeframe {timeframe!r}"
        return out
    out["registry_hash"] = composite_registry_hash(blocks)
    if len(blocks) == 1:
        out.update(kind=KIND_BLOCK, config_ref=blocks[0]["source_config_ref"],
                   expected_config_sha256=blocks[0]["source_config_sha256"])
        return out
    matches = [c for c in compositions if isinstance(c, dict)
               and c.get("registry_hash") == out["registry_hash"] and c.get("base_config_ref")]
    if not matches:
        out.update(kind=KIND_STALE,
                   reason=(f"composite is stale: no composition run is recorded for the "
                           f"{len(blocks)} forecast blocks on {timeframe!r} (registry_hash "
                           f"{out['registry_hash']})"))
        return out
    refs = {(c["base_config_ref"], c.get("base_config_sha256")) for c in matches}
    if len(refs) > 1:
        raise CompositeError(f"compositions.yaml records {len(refs)} different base configs for "
                             f"registry_hash {out['registry_hash']}: {sorted(map(str, refs))}")
    ref, sha = refs.pop()
    if not sha:
        raise CompositeError(f"compositions.yaml entry for registry_hash {out['registry_hash']} "
                             f"has no base_config_sha256 -- the composite's config cannot be "
                             f"checked against what was tested (same rule as a single block)")
    out.update(kind=KIND_COMPOSITION, config_ref=ref, expected_config_sha256=sha)
    return out


def _canonical_config_sha256(path: Path) -> str:
    """Same canonical form as run_phase1_research._compute_forecast_hash."""
    try:
        cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    except ValueError as exc:
        raise CompositeError(f"{path}: unparseable JSON ({exc})") from exc
    return hashlib.sha256(json.dumps(cfg, sort_keys=True).encode("utf-8")).hexdigest()


def _refuse_sealed(path: Path) -> None:
    if _SEALED_DIR_NAME in Path(path).resolve().parts:
        raise CompositeError(f"{path} is under {_SEALED_DIR_NAME}/ -- the composite never "
                             f"reads the sealed holdout store")


def _iso(value, what: str, breach_cls) -> date:
    """A strict YYYY-MM-DD day via tools/holdout_policy.py (CUL-339: the ONE
    parser). Stricter than before: a timestamp, padding or trailing text used
    to be cut to its first 10 characters and accepted; it is now refused."""
    day = _holdout_policy.iso_day(value)
    if day is None:
        raise breach_cls(f"{what}={value!r} is not a YYYY-MM-DD day -- refusing (fail closed)")
    return date.fromisoformat(day)


def check_protocol_outside_holdout(protocol: dict, holdout_range: tuple, *,
                                   breach_cls=CompositeError) -> None:
    """Every test window must carry real ISO start/end dates and lie wholly
    before or wholly after the sealed range (both ends inclusive -- the engine
    reads the whole end DAY). Anything missing or unparseable fails closed.
    The range itself must be a closed strict-day pair (holdout_policy)."""
    try:
        lo_s, hi_s = _holdout_policy.parse_holdout_range(holdout_range, "holdout range")
    except _holdout_policy.HoldoutPolicyError as exc:
        raise breach_cls(f"{exc} -- refusing (fail closed)") from exc
    lo, hi = date.fromisoformat(lo_s), date.fromisoformat(hi_s)
    windows = protocol.get("windows")
    if not isinstance(windows, list) or not windows:
        raise breach_cls("protocol has no windows -- nothing to check, refusing (fail closed)")
    for w in windows:
        test = (w or {}).get("test") if isinstance(w, dict) else None
        if not isinstance(test, dict):
            raise breach_cls(f"protocol window {w!r} has no test dates -- refusing (fail closed)")
        label = w.get("label")
        start = _iso(test.get("start"), f"window {label!r} test.start", breach_cls)
        end = _iso(test.get("end"), f"window {label!r} test.end", breach_cls)
        if end < start:
            raise breach_cls(f"window {label!r} ends before it starts -- refusing")
        if not (end < lo or start > hi):
            raise breach_cls(
                f"protocol window {label!r} ({start}..{end}) touches the sealed holdout range "
                f"-- the composite never reaches the holdout")


def subprocess_runner(python_exe) -> callable:
    """The default runner: tools/run_protocol.py in NORMAL mode (never
    --holdout, no --validation-protocol) into `out_dir`."""
    def _run(config_path: Path, protocol_path: Path, out_dir: Path) -> None:
        cmd = [str(python_exe), str(_RUN_PROTOCOL), str(config_path), str(protocol_path),
               "--out-dir", str(out_dir)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise CompositeError(f"composite protocol run failed (exit {result.returncode}):\n"
                                 f"{(result.stderr or '')[-4000:]}")
    return _run


def run_fingerprint(protocol_result: dict, results_dir) -> dict:
    """{git_sha, data: {"<symbol>|<window>": data_sha256}} from each window's
    manifest.json (reporting/run_artifact.write_manifest). Missing manifest,
    missing hash or two different git shas raise."""
    data, shas = {}, set()
    for e in protocol_result.get("results") or []:
        if not (isinstance(e, dict) and e.get("run_id")):
            continue
        path = Path(results_dir) / e["run_id"] / "manifest.json"
        if not path.exists():
            raise CompositeError(f"{path} is missing -- the market data a window read cannot be "
                                 f"fingerprinted")
        m = json.loads(path.read_text(encoding="utf-8"))
        dsha = (m.get("data") or {}).get("data_sha256")
        if not dsha or not m.get("git_sha"):
            raise CompositeError(f"{path}: no data.data_sha256 / git_sha")
        data[f"{e.get('symbol')}|{e.get('window')}"] = dsha
        shas.add(m["git_sha"])
    if not data:
        raise CompositeError("protocol result has no window to fingerprint")
    if len(shas) != 1:
        raise CompositeError(f"windows were run with different engine versions: {sorted(shas)}")
    return {"git_sha": shas.pop(), "data": data}


def _fp_hash(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()


def composite_series(resolved: dict, *, root: Path, protocol_path: Path, holdout_range: tuple,
                     candidate_fingerprint: dict, breach_cls=CompositeError,
                     runner=None, python_exe=None) -> tuple:
    """({symbol: records}, {symbol: step}, cache_dir) for a `block` or
    `composition` composite on the candidate's protocol; computed once and
    cached (see the module docstring for the key). Raises for any other kind."""
    if resolved["kind"] not in (KIND_BLOCK, KIND_COMPOSITION):
        raise CompositeError(f"composite kind {resolved['kind']!r} has no series to compute")
    import campaign_memory as _cm  # tools/ sibling: the lock primitive
    root = Path(root)
    config_path = root / resolved["config_ref"]
    protocol_path = Path(protocol_path)
    for p in (config_path, protocol_path):
        _refuse_sealed(p)
        if not p.exists():
            raise CompositeError(f"{p} is missing")
    config_sha = _canonical_config_sha256(config_path)
    expected = resolved.get("expected_config_sha256")
    if not expected:
        raise CompositeError(f"{config_path}: no recorded config sha256 to check against")
    if config_sha != expected:
        raise CompositeError(f"{config_path}: sha256 {config_sha} differs from the recorded "
                             f"{expected} -- the composite's config changed after it was tested")
    protocol_bytes = protocol_path.read_bytes()
    protocol_sha = hashlib.sha256(protocol_bytes).hexdigest()
    protocol = json.loads(protocol_bytes.decode("utf-8"))
    check_protocol_outside_holdout(protocol, holdout_range, breach_cls=breach_cls)

    engine_sha = candidate_fingerprint["git_sha"]
    data_hash = _fp_hash(candidate_fingerprint["data"])
    parent = root / "campaign_record" / "composite" / resolved["registry_hash"]
    cache_dir = parent / (f"{config_sha[:8]}_{protocol_sha[:8]}_"
                          f"{_fp_hash(engine_sha)[:8]}_{data_hash[:8]}")
    meta_path = cache_dir / COMPOSITE_META_FILENAME
    summary_path = cache_dir / "protocol_summary.json"
    parent.mkdir(parents=True, exist_ok=True)
    with _cm._file_lock(parent / COMPOSITE_LOCK_FILENAME, "the composite cache",
                        error_cls=CompositeError, wait_seconds=COMPOSITE_LOCK_WAIT_SECONDS):
        meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else None
        hit = (isinstance(meta, dict) and summary_path.exists()
               and meta.get("config_sha256") == config_sha
               and meta.get("protocol_sha256") == protocol_sha
               and meta.get("registry_hash") == resolved["registry_hash"]
               and meta.get("engine_git_sha") == engine_sha
               and meta.get("data_fingerprint_sha256") == data_hash)
        if hit:
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            if not all(p.exists() for p in _ric.window_bars_paths(summary, cache_dir / "results")):
                print(f"WARNING [E-060] composite cache {cache_dir}: bars files missing -- recomputing")
                hit = False
        if not hit:
            cache_dir.mkdir(parents=True, exist_ok=True)
            if meta_path.exists():
                meta_path.unlink()  # composite.yaml is the commit marker: written last
            run = runner or subprocess_runner(python_exe or sys.executable)
            run(config_path, protocol_path, cache_dir)
            if not summary_path.exists():
                raise CompositeError(f"composite protocol run wrote no {summary_path}")
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            got = run_fingerprint(summary, cache_dir / "results")
            if got["git_sha"] != engine_sha:
                raise CompositeError(f"composite ran on engine {got['git_sha']}, the candidate on "
                                     f"{engine_sha} -- not comparable")
            if got["data"] != candidate_fingerprint["data"]:
                raise CompositeError("the composite read different market data from the "
                                     "candidate (data_sha256 per symbol|window differ) -- not "
                                     "comparable")
            meta = {
                "schema_version": SCHEMA_VERSION,
                "kind": resolved["kind"],
                "timeframe": resolved["timeframe"],
                "registry_hash": resolved["registry_hash"],
                "block_ids": list(resolved["block_ids"]),
                "config_ref": resolved["config_ref"],
                "config_sha256": config_sha,
                "protocol_ref": protocol_path.as_posix(),
                "protocol_sha256": protocol_sha,
                "engine_git_sha": engine_sha,
                "data_fingerprint_sha256": data_hash,
                "computed_at": datetime.now(timezone.utc).isoformat(),
                "note": "not a trial, not graded, never the holdout (E-060 S2, guess 5)",
            }
            meta_path.write_text(yaml.safe_dump(meta, sort_keys=False), encoding="utf-8")
    records, steps = _ric.symbol_records_from_protocol_result(summary, cache_dir / "results")
    return records, steps, cache_dir


def residual_ic_by_variant(variant_summaries: dict, variant_results_dirs: dict, *,
                           root: Path, protocol_path: Path, registry_path: Path,
                           compositions_path: Path, holdout_range: tuple,
                           breach_cls=CompositeError, exempt_reason: str | None = None,
                           runner=None, python_exe=None) -> dict:
    """The residual-IC diagnostic for every tested variant of one run. Returns
    {timeframe, timeframe_category, composite: {...}, variants: {variant_id:
    diagnostic}} -- or, for an exempt idea (a regime block or a composition
    run), {timeframe, timeframe_category, skipped: reason, variants: {}}
    without resolving or running anything.
    `variant_results_dirs`: {variant_id: <variant out-dir>/results}."""
    import block_registry as _br  # tools/ sibling
    protocol = json.loads(Path(protocol_path).read_text(encoding="utf-8"))
    timeframe = protocol.get("timeframe", "1h")  # run_protocol's own default
    head = {"timeframe": timeframe, "timeframe_category": timeframe_category(timeframe)}
    if exempt_reason:
        return {**head, "skipped": exempt_reason, "composite": None, "variants": {}}
    block_size = _tf.bars_per_day(timeframe)
    resolved = resolve_current_composite(_br.load_registry(registry_path),
                                         load_compositions(compositions_path), timeframe)
    comp_records = comp_note = None
    if resolved["kind"] in (KIND_BLOCK, KIND_COMPOSITION):
        fps = {vid: run_fingerprint(variant_summaries[vid], variant_results_dirs[vid])
               for vid in sorted(variant_summaries)}
        first = next(iter(fps.values()))
        if any(fp != first for fp in fps.values()):
            raise CompositeError("the variants of this run read different market data or ran on "
                                 "different engine versions -- one composite cannot serve them")
        comp_records, _steps, cache_dir = composite_series(
            resolved, root=root, protocol_path=protocol_path, holdout_range=holdout_range,
            candidate_fingerprint=first, breach_cls=breach_cls, runner=runner,
            python_exe=python_exe)
        comp_note = cache_dir.relative_to(Path(root)).as_posix()
    variants = {}
    for vid in sorted(variant_summaries):
        if resolved["kind"] == KIND_STALE:
            diag = _ric.stale_residual_ic(resolved["reason"])
        else:
            records, steps = _ric.symbol_records_from_protocol_result(
                variant_summaries[vid], variant_results_dirs[vid])
            label = _ric.COMPOSITE_NONE if resolved["kind"] == KIND_NONE else resolved["kind"]
            diag = _ric.compute_residual_ic(records, comp_records, block_size=block_size,
                                            expected_step_by_symbol=steps, composite_label=label)
        diag["composite_registry_hash"] = resolved["registry_hash"]
        variants[vid] = diag
    return {
        **head,
        "skipped": None,
        "composite": {"kind": resolved["kind"], "registry_hash": resolved["registry_hash"],
                      "block_ids": resolved["block_ids"],
                      "excluded_blocks": resolved["excluded_blocks"],
                      "config_ref": resolved["config_ref"],
                      "cache_dir": comp_note, "reason": resolved["reason"]},
        "variants": variants,
    }
