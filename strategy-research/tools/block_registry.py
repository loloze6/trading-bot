"""
campaign_record/block_registry.yaml -- validated blocks, append-only
(E-058 S2b, delivery_plan_v26.md slice 6a; spec:
engineering/roadmap/E-058/S1_FINDINGS.md §4, guesses 1/6/7 and the operator
decision of 2026-09-23).

Written ONLY by the orchestrator's `regroup_record` tool stage
(orchestrator.regroup_record.enabled, off by default), from the run's memory
entry (tools/campaign_memory.py) plus two run files:
  * artifacts/block_manifest.yaml -- which part of the config IS the block
    (STRATEGY_DESIGN_GUIDE.md §7c: {block: {kind, config_paths}, scaffolding,
    rationale}), checked by tools/block_manifest.py -- the same code the
    orchestrator's 5a stage checks it with (one contract, two readers);
  * the tested base config the manifest's JSON pointers are read from.

A block is registered only when ALL hold:
  * the grid's idea_status is `validated` (the status comes only from
    idea_status.yaml, copied into the memory entry -- nothing here decides);
  * the run has no engineering fault (a component-error run is never
    registered -- its memory entry is the fault-only form);
  * the run's block_manifest.yaml exists. Without it the memory entry says
    `registry: {skipped: no_manifest}` and a loud line is printed; that is not
    a failure here (guess 1). Stage 1b writes it under
    orchestrator.config_direct_authoring, where 5a already fails loud when it is
    missing; a run from another flow simply has none.

Append-only. An entry is never edited or removed by code. A re-run of a run
that already registered a block must produce exactly the same block (then it
is a no-op); anything else -- a different block, or no block at all -- raises
BlockRegistryError and a person decides (guess 7).

E-060 S2 (slice 7 item 7.1), under orchestrator.composition_runs.enabled
only (record_run(..., composition_runs=True)): the entry also carries the
block's exact `timeframe` and its `timeframe_category` (operator decision 3:
high <= 15min < medium < 1h <= low < 1d <= daily), and `residual_ic` /
`correlation_to_composite` become mappings read from the run's
artifacts/residual_ic.yaml (the numbers the grid's residual_ic cell was
evaluated on) for the base variant. Flag off: the entry is exactly the E-058
shape (both null, no timeframe keys).

Deliberately NOT here:
  * a coin restriction: a block validated anywhere is usable on any coin
    (target decision, card F). `symbols_tested` is informational only.
  * reader proposal scores, refine/pivot/escalate, hypothesis_family,
    altitude, continuation fields (retired in slice 6c).

Importable without the orchestrator: every path is passed in by the caller.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

import block_manifest as _bm  # tools/ sibling: THE manifest contract (shared with 5a)
import campaign_memory as _cm  # tools/ sibling: atomic write + lock primitive
import json_pointer as _jp  # tools/ sibling: the orchestrator's pointer + base-variant rules
from workflow_artifact_validation import validate_workflow_artifact

SCHEMA_VERSION = 1
REGISTRY_LOCK_FILENAME = ".block_registry.lock"
MANIFEST_FILENAME = _bm.MANIFEST_FILENAME
MANIFEST_KINDS = _bm.MANIFEST_KINDS
_NUMBER_KEYS = ("value", "threshold", "n_windows", "n_trades")
# Fields that may differ between two registrations of the same block without
# the block itself having changed.
_VOLATILE_FIELDS = frozenset({"registered_at"})

BLOCK_FIELDS = (
    "block_id", "hypothesis_id", "kind", "config_fragment", "regime_assignment",
    "criteria_passed", "variants_passed", "numbers", "symbols_tested",
    "correlation_to_composite", "residual_ic", "source_config_ref",
    "source_config_sha256", "validated_by_run", "registered_at",
)
# E-060 S2: written together, only under orchestrator.composition_runs.
TIMEFRAME_FIELDS = ("timeframe", "timeframe_category")
RESIDUAL_IC_ARTIFACT = "residual_ic.yaml"


class BlockRegistryError(ValueError):
    """The registry file, a manifest or a registration input is malformed, or
    a re-run would change an append-only entry. Never caught here."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _fresh_doc() -> dict:
    return {"schema_version": SCHEMA_VERSION, "revision": 0, "updated_at": None, "blocks": []}


def load_registry(path: Path) -> dict:
    """The registry document. Absent -> a fresh one (not written until a
    block is registered). Anything else malformed raises; a malformed file is
    never replaced with a fresh one."""
    path = Path(path)
    if not path.exists():
        return _fresh_doc()
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise BlockRegistryError(f"{path}: unparseable YAML ({exc})") from exc
    if not isinstance(doc, dict):
        raise BlockRegistryError(f"{path}: expected a mapping, got {type(doc).__name__}")
    if doc.get("schema_version") != SCHEMA_VERSION:
        raise BlockRegistryError(f"{path}: schema_version={doc.get('schema_version')!r}, "
                                 f"expected {SCHEMA_VERSION}")
    revision = doc.get("revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 0:
        raise BlockRegistryError(f"{path}: revision={revision!r} is not a non-negative integer")
    blocks = doc.get("blocks")
    if not isinstance(blocks, list):
        raise BlockRegistryError(f"{path}: blocks is not a list")
    seen = set()
    for i, block in enumerate(blocks):
        if not isinstance(block, dict):
            raise BlockRegistryError(f"{path}: blocks[{i}] is not a mapping")
        missing = [f for f in BLOCK_FIELDS if f not in block]
        extra = sorted(set(block) - set(BLOCK_FIELDS) - set(TIMEFRAME_FIELDS))
        if missing or extra:
            raise BlockRegistryError(f"{path}: blocks[{i}] missing {missing} / unknown {extra}")
        tf_present = [f for f in TIMEFRAME_FIELDS if f in block]
        if tf_present and len(tf_present) != len(TIMEFRAME_FIELDS):
            raise BlockRegistryError(f"{path}: blocks[{i}] carries {tf_present} but not all of "
                                     f"{list(TIMEFRAME_FIELDS)} -- they are written together")
        bid = block["block_id"]
        if not isinstance(bid, str) or not bid or bid in seen:
            raise BlockRegistryError(f"{path}: blocks[{i}].block_id={bid!r} is empty or duplicated")
        seen.add(bid)
        if not isinstance(block["validated_by_run"], str) or not block["validated_by_run"]:
            raise BlockRegistryError(f"{path}: blocks[{i}].validated_by_run is not a run id")
    if revision < len(blocks):
        raise BlockRegistryError(f"{path}: revision={revision} is below the block count "
                                 f"{len(blocks)} -- every append bumps it")
    return doc


def load_manifest(run_dir: Path):
    """artifacts/block_manifest.yaml, shape-validated by tools/block_manifest.py
    (the orchestrator's own check); None when absent."""
    return _bm.load_manifest_file(Path(run_dir) / "artifacts" / MANIFEST_FILENAME,
                                  error_cls=BlockRegistryError)


def _base_variant(entry: dict) -> tuple:
    """The tested base config, chosen exactly as protocol_execution chooses
    its base variant (tools/json_pointer.base_variant_id: `base`, else the
    first index-validated variant in sorted order). Index-validated variants
    are the memory's `tested` and `failed` ones; the single run_id column
    (variant loop off) is its own base. The base must have been backtested --
    a block is never read from a config the grid did not test."""
    variants = entry.get("variants") or {}
    run_id = entry["run_id"]
    validated = [vid for vid, v in variants.items() if v.get("status") in ("tested", "failed")]
    vid = _jp.base_variant_id(validated) if validated else None
    info = variants.get(vid) if vid else None
    if not info or info.get("status") != "tested" or not info.get("config_ref") \
            or not info.get("forecast_hash"):
        raise BlockRegistryError(
            f"{run_id}: base variant {vid!r} is not a tested variant with a config_ref and "
            f"forecast_hash in the memory entry (variants: {sorted(variants)}) -- a block's config "
            f"piece must come from the base config the grid actually tested")
    return vid, info


def _composition_fields(run_dir: Path, run_id: str, vid: str, kind: str) -> dict:
    """E-060 S2: timeframe, timeframe_category, residual_ic and
    correlation_to_composite from artifacts/residual_ic.yaml (written by
    protocol_execution under composition_runs) for the base variant `vid`.
    A file that is ABSENT is absent by design -- the run's protocol_execution
    happened with the flag off -- so the block keeps the E-058 shape (no
    timeframe keys, both null; composite_cache then excludes it loudly). A
    file marked `skipped` (an exempt idea) gives the timeframe with null
    residual-IC fields; so does a regime block (it is not a forecast). A
    present, non-skipped file without the base variant raises."""
    path = Path(run_dir) / "artifacts" / RESIDUAL_IC_ARTIFACT
    if not path.exists():
        print(f"WARNING [E-060] block registry: {run_id} has no artifacts/{RESIDUAL_IC_ARTIFACT} "
              f"(protocol_execution ran with orchestrator.composition_runs off) -- block "
              f"registered without timeframe / residual IC")
        return {}
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise BlockRegistryError(f"{path}: unparseable YAML ({exc})") from exc
    doc = doc if isinstance(doc, dict) else {}
    if not isinstance(doc.get("timeframe"), str) \
            or doc.get("timeframe_category") not in ("high", "medium", "low", "daily"):
        raise BlockRegistryError(f"{path}: no valid timeframe / timeframe_category")
    out = {"timeframe": doc["timeframe"], "timeframe_category": doc["timeframe_category"],
           "residual_ic": None, "correlation_to_composite": None}
    if doc.get("skipped"):
        return out
    diag = (doc.get("variants") or {}).get(vid)
    if not isinstance(diag, dict):
        raise BlockRegistryError(f"{path}: no residual-IC record for base variant {vid!r}")
    if kind == "forecast":
        basis = {"composite": diag.get("composite"),
                 "composite_registry_hash": diag.get("composite_registry_hash")}
        out["residual_ic"] = {"value": diag.get("value"), "n_eff": diag.get("n_eff"),
                              "p_value": diag.get("p_value"),
                              "p_value_one_sided": diag.get("p_value_one_sided"),
                              "fully_explained": diag.get("fully_explained"), **basis}
        out["correlation_to_composite"] = {"value": diag.get("correlation_to_composite"), **basis}
    return out


def build_block(run_dir: Path, entry: dict, manifest: dict, *, root: Path,
                registered_at: str | None = None, composition_runs: bool = False) -> dict:
    """One registry entry (pure apart from reading the base config, and under
    composition_runs artifacts/residual_ic.yaml)."""
    run_id = entry["run_id"]
    vid, info = _base_variant(entry)
    cfg_path = Path(root) / info["config_ref"]
    if not cfg_path.exists():
        raise BlockRegistryError(f"{run_id}: base config {cfg_path} is missing")
    try:
        config = json.loads(cfg_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise BlockRegistryError(f"{cfg_path}: unparseable JSON ({exc})") from exc
    # Same canonical form as run_phase1_research._compute_forecast_hash, so the
    # hash equals the trial row's forecast_hash when the file is unchanged.
    sha = hashlib.sha256(json.dumps(config, sort_keys=True).encode("utf-8")).hexdigest()
    if sha != info["forecast_hash"]:
        raise BlockRegistryError(
            f"{cfg_path}: sha256 {sha} differs from the tested variant's forecast_hash "
            f"{info['forecast_hash']} -- the config changed after the backtest; refusing to "
            f"register a block the grid did not test")
    paths = manifest["block"]["config_paths"]
    where = str(Path(run_dir) / "artifacts" / MANIFEST_FILENAME)
    # The one resolution check (block AND scaffolding) -- the same 5a ran on 1b's base config.
    _bm.check_manifest(manifest, config, where=f"{where} (tested base config {cfg_path})",
                       error_cls=BlockRegistryError)
    grid = entry["grid"]
    numbers = {}
    for crit, row in grid["cells"].items():
        numbers[crit] = {}
        for variant, cell in row.items():
            if cell.get("result") != "PASS":
                raise BlockRegistryError(f"{run_id}: grid.{crit}.{variant} is {cell.get('result')!r} "
                                         f"but the idea is validated -- inconsistent memory entry")
            num = {k: cell[k] for k in _NUMBER_KEYS if k in cell}
            if "per_symbol" in cell:
                num["per_symbol"] = {s: {k: c[k] for k in _NUMBER_KEYS if k in c}
                                     for s, c in cell["per_symbol"].items()}
            numbers[crit][variant] = num
    symbols = sorted({s for v in (entry.get("variants") or {}).values()
                      if v.get("status") == "tested" for s in (v.get("symbols") or [])})
    block = {
        "block_id": f"{entry['hypothesis_id']}:{run_id}",
        "hypothesis_id": entry["hypothesis_id"],
        "kind": manifest["block"]["kind"],
        "config_fragment": {p: _jp.resolve_json_pointer(config, p) for p in paths},
        "regime_assignment": _bm.regime_assignment(paths),
        "criteria_passed": list(grid["criteria"]),
        "variants_passed": list(grid["variants"]),
        "numbers": numbers,
        "symbols_tested": symbols,  # informational: any-coin eligibility (card F)
        "correlation_to_composite": None,  # filled under composition_runs (E-060 S2)
        "residual_ic": None,  # filled under composition_runs (E-060 S2)
        "source_config_ref": info["config_ref"],
        "source_config_sha256": sha,
        "validated_by_run": run_id,
        "registered_at": registered_at or _now(),
    }
    if composition_runs:
        block.update(_composition_fields(run_dir, run_id, vid, block["kind"]))
    return block


def _stable(block: dict) -> dict:
    return {k: v for k, v in block.items() if k not in _VOLATILE_FIELDS}


def _append(path: Path, run_id: str, new_blocks: list) -> None:
    """Under the lock: refuse any change to what `run_id` already registered;
    append otherwise. Writes nothing when there is nothing new."""
    path = Path(path)
    if not new_blocks and not path.exists():
        return  # nothing registered yet, nothing to register: no file, no lock
    with _cm._file_lock(path.parent / REGISTRY_LOCK_FILENAME, "the block registry",
                        error_cls=BlockRegistryError):
        doc = load_registry(path)
        existing = [b for b in doc["blocks"] if b["validated_by_run"] == run_id]
        if existing:
            if [_stable(b) for b in existing] == [_stable(b) for b in new_blocks]:
                return  # the same re-run: nothing to append
            raise BlockRegistryError(
                f"{path}: {run_id} already registered {[b['block_id'] for b in existing]}; this "
                f"re-run would register {[b['block_id'] for b in new_blocks] or 'nothing'} "
                f"with different content. The registry is append-only -- a person decides "
                f"(remove or keep the old entry by hand), code never edits it.")
        if not new_blocks:
            return
        taken = {b["block_id"] for b in doc["blocks"]}
        clash = [b["block_id"] for b in new_blocks if b["block_id"] in taken]
        if clash:
            raise BlockRegistryError(f"{path}: block_id(s) {clash} already registered by another run")
        doc["blocks"].extend(new_blocks)
        doc["revision"] += len(new_blocks)
        doc["updated_at"] = _now()
        validate_workflow_artifact(path, doc)
        _cm._atomic_write(path, doc)


def blocks_for_run(path: Path, run_id: str) -> list:
    """block_ids `run_id` already registered (read only; [] when the file is
    absent). A malformed registry raises."""
    if not Path(path).exists():
        return []
    return [b["block_id"] for b in load_registry(path)["blocks"] if b["validated_by_run"] == run_id]


def record_run(path: Path, run_dir: Path, entry: dict, *, root: Path,
               composition_runs: bool = False, composition_run: bool = False) -> dict | None:
    """The regroup_record hook. Returns the memory entry's `registry` value
    ({"block_ids": [...]} or {"skipped": reason}); None for a fault-only
    entry, which carries no registry field. Raises BlockRegistryError on a
    malformed file/manifest or an append-only conflict.
    `composition_run` (E-060 S3b, guess 11; the caller passes it only under
    orchestrator.composition_runs): the run is a composition -- a composite
    NEVER registers as a block (registering would change the registry and
    re-trigger R1 forever), whatever its idea_status: {"skipped":
    "composition"}, no block_manifest.yaml read, no warning."""
    run_id = entry["run_id"]
    if entry.get("engineering_fault") is not None:
        _append(path, run_id, [])  # never registers; only refuses to hide an old block
        return None
    if composition_run:
        _append(path, run_id, [])  # never registers; only refuses to hide an old block
        return {"skipped": _cm.REGISTRY_SKIPPED_COMPOSITION}
    if entry.get("legacy") is not False or entry.get("idea_status") != "validated":
        _append(path, run_id, [])
        return {"skipped": _cm.REGISTRY_SKIPPED_NOT_VALIDATED}
    manifest = load_manifest(run_dir)
    if manifest is None:
        _append(path, run_id, [])
        print(f"WARNING [E-058] block registry: {run_id} is VALIDATED but has no "
              f"artifacts/{MANIFEST_FILENAME} -- nothing says which part of its config is the "
              f"block, so NO block is registered (memory: registry.skipped=no_manifest). "
              f"Only strategy_config_authoring (orchestrator.config_direct_authoring) writes it.")
        return {"skipped": _cm.REGISTRY_SKIPPED_NO_MANIFEST}
    block = build_block(run_dir, entry, manifest, root=root, composition_runs=composition_runs)
    _append(path, run_id, [block])
    print(f"[E-058] block registry: registered {block['block_id']} ({block['kind']}) -> {path}")
    return {"block_ids": [block["block_id"]]}
