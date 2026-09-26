"""
The "current composite" forecast series that a candidate block's residual IC
is measured against (E-060 S2, delivery_plan_v26.md slice 7 item 7.1; spec:
engineering/roadmap/E-060/S1_FINDINGS.md §2, guesses 4 and 5, and operator
decision 3 of 2026-09-26). Used only under orchestrator.composition_runs.

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

The set of blocks is identified by `registry_hash` (composite_registry_hash):
sha256 over the sorted (block_id, source_config_sha256) pairs of exactly those
blocks, so a block registered on ANOTHER timeframe does not make this
timeframe's composite stale. S3's composition writer must record the same hash
(`registry_hash`) and its base variant's config (`base_config_ref`) in each
compositions.yaml entry: that is this module's read contract (S3 builds the
writer).

Where it is measured (guess 5): on the candidate's own coins and windows --
the composite config is run through tools/run_protocol.py with the
CANDIDATE's protocol file, which the data policy already admitted. Cached
under campaign_record/composite/<registry_hash>/<config_sha8>_<protocol_sha8>/
(the run_protocol out-dir plus composite.yaml), so a second candidate on the
same protocol reuses it.

What it is not:
  * not a trial -- tools/run_protocol.py writes no trial row (only
    run_phase1_research._record_backtest_trial does), and nothing here calls
    that; the cache directory is outside runs/;
  * not graded -- no pass rule, no profit bars, no grid; its protocol run is
    started without --validation-protocol;
  * never the holdout -- --holdout is never passed, every protocol window is
    checked against config/campaign_data_policy.yaml's holdout_range before
    anything runs, and a path under local_data/holdout_sealed is refused.

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
from datetime import datetime, timezone
from pathlib import Path

import yaml

import residual_ic as _ric  # tools/ sibling (also puts trading-bot/ on sys.path)
import timeframe as _tf  # tools/ sibling: the one timeframe parser

SCHEMA_VERSION = 1
COMPOSITE_META_FILENAME = "composite.yaml"
KIND_NONE, KIND_BLOCK, KIND_COMPOSITION, KIND_STALE = "none", "block", "composition", "stale"
_RUN_PROTOCOL = Path(__file__).resolve().parent / "run_protocol.py"
_SEALED_DIR_NAME = "holdout_sealed"

# Operator decision 3 (2026-09-26), by bar length in seconds.
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


def forecast_blocks_on_timeframe(registry_doc: dict, timeframe) -> list:
    """Registry forecast blocks whose exact bar size equals `timeframe`
    (compared in seconds, so "60m" == "1h"). A forecast block without a
    `timeframe` (registered before this slice) cannot be placed: raises."""
    want = _tf.timeframe_seconds(timeframe)
    out = []
    for block in registry_doc.get("blocks") or []:
        if block.get("kind") != "forecast":
            continue
        tf = block.get("timeframe")
        if tf is None:
            raise CompositeError(
                f"registry block {block.get('block_id')!r} has no timeframe (registered before "
                f"E-060 S2) -- it cannot be placed in a per-timeframe composite; a person "
                f"decides how to record it (the registry is append-only)")
        if _tf.timeframe_seconds(tf) == want:
            out.append(block)
    return out


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
    block_ids, config_ref, expected_config_sha256, reason}."""
    blocks = forecast_blocks_on_timeframe(registry_doc, timeframe)
    out = {"kind": KIND_NONE, "timeframe": timeframe, "registry_hash": None,
           "block_ids": [b["block_id"] for b in blocks], "config_ref": None,
           "expected_config_sha256": None, "reason": None}
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
    refs = {c["base_config_ref"] for c in matches}
    if len(refs) > 1:
        raise CompositeError(f"compositions.yaml records {len(refs)} different base configs for "
                             f"registry_hash {out['registry_hash']}: {sorted(refs)}")
    out.update(kind=KIND_COMPOSITION, config_ref=refs.pop(),
               expected_config_sha256=matches[-1].get("base_config_sha256"))
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


def check_protocol_outside_holdout(protocol: dict, policy_path: Path) -> None:
    """Every test window must end before the holdout_range starts and start
    after it ends. The policy file is required (fail loud without it)."""
    policy_path = Path(policy_path)
    if not policy_path.exists():
        raise CompositeError(f"{policy_path} is missing -- refusing to run a composite without "
                             f"the holdout range to check its windows against")
    policy = yaml.safe_load(policy_path.read_text(encoding="utf-8")) or {}
    rng = policy.get("holdout_range")
    if not (isinstance(rng, list) and len(rng) == 2 and all(isinstance(x, str) for x in rng)):
        raise CompositeError(f"{policy_path}: holdout_range={rng!r} is not [start, end]")
    lo, hi = rng
    windows = protocol.get("windows")
    if not isinstance(windows, list) or not windows:
        raise CompositeError("protocol has no windows -- nothing to run the composite on")
    for w in windows:
        test = (w or {}).get("test") or {}
        start, end = str(test.get("start")), str(test.get("end"))
        if not (end < lo or start > hi):
            raise CompositeError(
                f"protocol window {w.get('label')!r} ({start}..{end}) touches the holdout "
                f"range {lo}..{hi} -- the composite never reaches the holdout")


def subprocess_runner(python_exe) -> callable:
    """The default runner: tools/run_protocol.py in NORMAL mode (never
    --holdout, no --validation-protocol) into `out_dir`."""
    def _run(config_path: Path, protocol_path: Path, out_dir: Path) -> None:
        cmd = [str(python_exe), str(_RUN_PROTOCOL), str(config_path), str(protocol_path),
               "--out-dir", str(out_dir)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise CompositeError(f"composite protocol run failed (exit {result.returncode}):\n"
                                 f"{result.stderr[-4000:]}")
    return _run


def composite_series(resolved: dict, *, root: Path, protocol_path: Path, policy_path: Path,
                     runner=None, python_exe=None) -> tuple:
    """({symbol: records}, {symbol: step}, cache_dir) for a `block` or
    `composition` composite on the candidate's protocol; computed once and
    cached. Raises for any other kind."""
    if resolved["kind"] not in (KIND_BLOCK, KIND_COMPOSITION):
        raise CompositeError(f"composite kind {resolved['kind']!r} has no series to compute")
    root = Path(root)
    config_path = root / resolved["config_ref"]
    protocol_path = Path(protocol_path)
    for p in (config_path, protocol_path):
        _refuse_sealed(p)
        if not p.exists():
            raise CompositeError(f"{p} is missing")
    config_sha = _canonical_config_sha256(config_path)
    expected = resolved.get("expected_config_sha256")
    if expected and config_sha != expected:
        raise CompositeError(f"{config_path}: sha256 {config_sha} differs from the recorded "
                             f"{expected} -- the composite's config changed after it was tested")
    protocol_bytes = protocol_path.read_bytes()
    protocol_sha = hashlib.sha256(protocol_bytes).hexdigest()
    protocol = json.loads(protocol_bytes.decode("utf-8"))
    check_protocol_outside_holdout(protocol, policy_path)

    cache_dir = (root / "campaign_record" / "composite" / resolved["registry_hash"]
                 / f"{config_sha[:8]}_{protocol_sha[:8]}")
    meta_path = cache_dir / COMPOSITE_META_FILENAME
    summary_path = cache_dir / "protocol_summary.json"
    meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) if meta_path.exists() else None
    hit = (isinstance(meta, dict) and summary_path.exists()
           and meta.get("config_sha256") == config_sha
           and meta.get("protocol_sha256") == protocol_sha
           and meta.get("registry_hash") == resolved["registry_hash"])
    if not hit:
        cache_dir.mkdir(parents=True, exist_ok=True)
        if meta_path.exists():
            meta_path.unlink()  # composite.yaml is the commit marker: written last
        run = runner or subprocess_runner(python_exe or sys.executable)
        run(config_path, protocol_path, cache_dir)
        if not summary_path.exists():
            raise CompositeError(f"composite protocol run wrote no {summary_path}")
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
            "computed_at": datetime.now(timezone.utc).isoformat(),
            "note": "not a trial, not graded, never the holdout (E-060 S2, guess 5)",
        }
        meta_path.write_text(yaml.safe_dump(meta, sort_keys=False), encoding="utf-8")
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    records, steps = _ric.symbol_records_from_protocol_result(summary, cache_dir / "results")
    return records, steps, cache_dir


def residual_ic_by_variant(variant_summaries: dict, variant_results_dirs: dict, *,
                           root: Path, protocol_path: Path, registry_path: Path,
                           compositions_path: Path, policy_path: Path,
                           runner=None, python_exe=None) -> dict:
    """The residual-IC diagnostic for every tested variant of one run. Returns
    {timeframe, timeframe_category, composite: {kind, registry_hash,
    block_ids, config_ref, reason}, variants: {variant_id: diagnostic}}.
    `variant_results_dirs`: {variant_id: <variant out-dir>/results}."""
    import block_registry as _br  # tools/ sibling
    protocol = json.loads(Path(protocol_path).read_text(encoding="utf-8"))
    timeframe = protocol.get("timeframe", "1h")  # run_protocol's own default
    block_size = _tf.bars_per_day(timeframe)
    resolved = resolve_current_composite(_br.load_registry(registry_path),
                                         load_compositions(compositions_path), timeframe)
    comp_records = comp_note = None
    if resolved["kind"] in (KIND_BLOCK, KIND_COMPOSITION):
        comp_records, _steps, cache_dir = composite_series(
            resolved, root=root, protocol_path=protocol_path, policy_path=policy_path,
            runner=runner, python_exe=python_exe)
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
        "timeframe": timeframe,
        "timeframe_category": timeframe_category(timeframe),
        "composite": {"kind": resolved["kind"], "registry_hash": resolved["registry_hash"],
                      "block_ids": resolved["block_ids"], "config_ref": resolved["config_ref"],
                      "cache_dir": comp_note, "reason": resolved["reason"]},
        "variants": variants,
    }
