"""
campaign_record/campaign_memory.yaml -- the per-run campaign memory
(E-058 S2a, delivery_plan_v26.md slice 6a; spec:
engineering/roadmap/E-058/S1_FINDINGS.md §3 and its operator decision).

Written ONLY by the orchestrator's `regroup_record` tool stage
(orchestrator.regroup_record.enabled, off by default), one entry per run keyed
by `run_id` and REPLACED on a re-run. Old runs are never backfilled: the
legacy record is campaign_knowledge_base.yaml.

What this module deliberately does NOT do:
  * decide anything. An entry's `idea_status` is copied from the grid's
    idea_status.yaml; nothing here computes or overrides a status.
  * read reader proposals for meaning. Proposal files are REFERENCED (path,
    proposal ids, count) and validated only so a malformed file fails loud.
    Their scores are never copied -- they rank the next candidate in the
    later decide-next step (slice 6b), and a copy here would invite a second
    reader to route on them.
  * write trial rows. campaign_state.trial_sharpes is written by
    protocol_execution; the ids here are a read-only cross-link.
  * carry retired machinery (slice 6c): no hypothesis_family, altitude,
    lineage routing, continuation or verdict-routing field. build_memory_entry
    refuses to return an entry that contains one (RETIRED_FIELDS).
  * the block registry, the KB mirror and the scoreboard (E-058 S2b). Their
    fields are present with an explicit "not built" / null value.

Importable without the orchestrator (same convention as reader_proposals.py):
every path is passed in by the caller, so tests' ROOT sandbox covers it.
"""
from __future__ import annotations

import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import yaml

SCHEMA_VERSION = 1

LEGACY_NOTE = (
    "Runs before the regroup_record stage (orchestrator.regroup_record.enabled) are not "
    "listed here and are never backfilled; their history is "
    "campaign_record/campaign_knowledge_base.yaml, where every entry without "
    "`legacy_schema: false` is legacy. Trial counts live in "
    "campaign_record/campaign_state.yaml -> trial_sharpes, not here."
)

ENGINEERING_FAULT_COMPONENT_ERROR = "component_execution_error"
PROFIT_BARS_NOT_EVALUATED = "not evaluated before regroup"

# Retired in slice 6c (roadmap v26 card G): no memory entry may carry them.
RETIRED_FIELDS = frozenset({
    "hypothesis_family", "altitude", "altitude_history", "next_altitude",
    "altitude_justification", "lineage_routing", "hypothesis_verdict",
    "continuation_child", "continuation_parent", "failed_families",
    "findings_carryover", "circuit_breaker",
})

_CELL_KEYS = ("result", "value", "threshold", "n_windows", "n_trades", "reason")
_CELL_RESULTS = ("PASS", "FAIL", "INCONCLUSIVE")
_TRIAL_SOURCES = ("backtest", "backtest_failed")
_IDEA_STATUSES = ("validated", "refuted", "inconclusive")


class CampaignMemoryError(ValueError):
    """A memory input or the memory file itself is malformed. Never caught
    here: the record must stop loudly, never silently drop or guess a field."""


def _load_strict(path: Path):
    """Plain safe_load, no LLM-output repair (a malformed machine-written file
    must not be silently 'repaired')."""
    try:
        return yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise CampaignMemoryError(f"{path}: unparseable YAML ({exc})") from exc


def _load_mapping(path: Path, what: str) -> dict:
    if not Path(path).exists():
        raise CampaignMemoryError(f"{path} is missing -- {what}")
    doc = _load_strict(path)
    if not isinstance(doc, dict):
        raise CampaignMemoryError(f"{path}: expected a mapping, got {type(doc).__name__}")
    return doc


def _ref(run_id: str, rel: str) -> str:
    return f"runs/{run_id}/{rel}"


def _compact_cell(cell, where: str) -> dict:
    if not isinstance(cell, dict) or cell.get("result") not in _CELL_RESULTS:
        raise CampaignMemoryError(f"{where}: cell result must be one of {_CELL_RESULTS}, "
                                  f"got {cell!r}")
    out = {k: cell[k] for k in _CELL_KEYS if k in cell}
    per_symbol = cell.get("per_symbol")
    if per_symbol is not None:
        if not isinstance(per_symbol, dict):
            raise CampaignMemoryError(f"{where}: per_symbol is not a mapping")
        out["per_symbol"] = {sym: {k: c[k] for k in _CELL_KEYS if isinstance(c, dict) and k in c}
                             for sym, c in per_symbol.items()}
    return out


def _grid_block(run_id: str, grid_doc: dict, path: Path) -> dict:
    criteria, variants, grid = grid_doc.get("criteria"), grid_doc.get("variants"), grid_doc.get("grid")
    if grid_doc.get("result") != "GRID_EVALUATED":
        raise CampaignMemoryError(f"{path}: result={grid_doc.get('result')!r}, expected "
                                  f"GRID_EVALUATED (idea_status.yaml exists only for an evaluated grid)")
    if not isinstance(criteria, list) or not criteria or not isinstance(variants, list) or not variants:
        raise CampaignMemoryError(f"{path}: criteria/variants must be non-empty lists")
    if not isinstance(grid, dict):
        raise CampaignMemoryError(f"{path}: grid is not a mapping")
    cells, counts = {}, {r: 0 for r in _CELL_RESULTS}
    for crit in criteria:
        row = grid.get(crit)
        if not isinstance(row, dict):
            raise CampaignMemoryError(f"{path}: grid.{crit} is missing or not a mapping")
        cells[crit] = {}
        for variant in variants:
            if variant not in row:
                raise CampaignMemoryError(f"{path}: grid.{crit}.{variant} is missing")
            cell = _compact_cell(row[variant], f"{path}: grid.{crit}.{variant}")
            cells[crit][variant] = cell
            counts[cell["result"]] += 1
    return {"ref": _ref(run_id, "artifacts/grid_evaluation.yaml"), "criteria": list(criteria),
            "variants": list(variants), "cells": cells, "counts": counts}


def _protocol_shape(pr: dict | None) -> dict:
    results = (pr or {}).get("results") or []
    if not isinstance(results, list):
        raise CampaignMemoryError("protocol_result.results is not a list")
    symbols = sorted({r.get("symbol") for r in results if isinstance(r, dict) and r.get("symbol")})
    return {"symbols": symbols, "n_windows": len(results)}


def _trial_ids_by_key(run_id: str, trial_sharpes) -> dict:
    """{trial_id: [sources]} for this run's backtest rows. Read-only."""
    if trial_sharpes is None:
        trial_sharpes = []
    if not isinstance(trial_sharpes, list):
        raise CampaignMemoryError("campaign_state.trial_sharpes is not a list")
    out: dict = {}
    for row in trial_sharpes:
        if not isinstance(row, dict) or row.get("source") not in _TRIAL_SOURCES:
            continue
        tid = row.get("trial_id")
        if isinstance(tid, str) and (tid == run_id or tid.startswith(f"{run_id}:")):
            out.setdefault(tid, []).append(row["source"])
    return out


def _variants_block(run_dir: Path, run_id: str, grid_variants: list, trials: dict,
                    forecast_hash_fn) -> dict:
    """Two grid-column shapes, told apart by the grid's own columns:
      * variant loop (columns are index.yaml variant ids): every index entry
        -- tested (a grid column), failed (validated but no column: its
        backtest failed), or not_tested (index status).
      * single column named after run_id (variant loop off -- including
        config-direct authoring, which writes index.yaml but backtests only
        the base config): from artifacts/protocol_result.yaml."""
    arts = run_dir / "artifacts"
    index_path = arts / "variants" / "index.yaml"
    out = {}
    index = None
    if index_path.exists():
        index = _load_mapping(index_path, "variant index").get("variants")
        if not isinstance(index, dict):
            raise CampaignMemoryError(f"{index_path}: variants is not a mapping")
    if index is not None and not (grid_variants == [run_id] and run_id not in index):
        unknown = [v for v in grid_variants if v not in index]
        if unknown:
            raise CampaignMemoryError(f"{index_path}: grid variant(s) {unknown} not in the index")
        for vid in sorted(index):
            info = index[vid] if isinstance(index[vid], dict) else {}
            if vid in grid_variants:
                status, reason = "tested", None
            elif info.get("status") == "validated":
                status, reason = "failed", "validated but produced no grid column (backtest failed)"
            else:
                status, reason = "not_tested", info.get("reason") or info.get("status")
            cfg_rel = info.get("config_path")
            cfg_rel = Path(cfg_rel).as_posix() if cfg_rel else None
            vpr_path = arts / "variants" / vid / "protocol_result.yaml"
            shape = _protocol_shape(_load_strict(vpr_path)) if (status == "tested" and vpr_path.exists()) \
                else {"symbols": [], "n_windows": 0}
            tid = f"{run_id}:{vid}"
            out[vid] = {
                "status": status, "reason": reason,
                "config_ref": _ref(run_id, cfg_rel) if cfg_rel else None,
                "forecast_hash": forecast_hash_fn(run_dir / cfg_rel) if cfg_rel else None,
                "symbols": shape["symbols"], "n_windows": shape["n_windows"],
                "trial_id": tid if tid in trials else None,
            }
        return out
    if grid_variants != [run_id]:
        raise CampaignMemoryError(
            f"{run_dir}: no artifacts/variants/index.yaml, so the grid must have the single "
            f"column {run_id!r}; got {grid_variants}")
    pr_path = arts / "protocol_result.yaml"
    shape = _protocol_shape(_load_mapping(pr_path, "protocol_execution output"))
    cfg = arts / "candidate_strategy_config.json"
    out[run_id] = {
        "status": "tested", "reason": None,
        "config_ref": _ref(run_id, "artifacts/candidate_strategy_config.json") if cfg.exists() else None,
        "forecast_hash": forecast_hash_fn(cfg) if cfg.exists() else None,
        "symbols": shape["symbols"], "n_windows": shape["n_windows"],
        "trial_id": run_id if run_id in trials else None,
    }
    return out


def _proposals_block(run_dir: Path, run_id: str, categories) -> list:
    """References only. Validated fail-loud by reader_proposals.load_proposals
    (the same check the readers stage applies); only ids and counts are kept."""
    import reader_proposals  # tools/ sibling; imported lazily for the caller's sys.path
    pdir = run_dir / "artifacts" / "proposals"
    loaded = reader_proposals.load_proposals(pdir, list(categories))
    return [{
        "category": cat,
        "ref": _ref(run_id, f"artifacts/proposals/{cat}.yaml") if (pdir / f"{cat}.yaml").exists() else None,
        "proposal_ids": [p["proposal_id"] for p in loaded[cat]],
        "count": len(loaded[cat]),
    } for cat in categories]


def _find_retired(obj, path="") -> list:
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in RETIRED_FIELDS:
                found.append(f"{path}{k}")
            found += _find_retired(v, f"{path}{k}.")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            found += _find_retired(v, f"{path}{i}.")
    return found


def build_memory_entry(run_dir: Path, run_id: str, *, component_errors: list,
                       trial_sharpes, categories, forecast_hash_fn,
                       protocol_root: Path | None = None, recorded_at: str | None = None) -> dict:
    """One run's memory entry, from artifacts that exist under the flag.
    Pure apart from reads: `component_errors` (the orchestrator's
    _protocol_component_errors), `trial_sharpes` (campaign_state, read only),
    `categories` (the reader categories) and `forecast_hash_fn` (a path -> hash
    callable: the orchestrator's _compute_forecast_hash, so a variant's
    `forecast_hash` equals its trial row's) are passed in. Raises CampaignMemoryError on any malformed or
    inconsistent input."""
    run_dir = Path(run_dir)
    arts = run_dir / "artifacts"
    card = _load_mapping(arts / "hypothesis_card.yaml", "the idea's identity (hypothesis_id)")
    hyp_id = card.get("hypothesis_id")
    if not isinstance(hyp_id, str) or not hyp_id.strip():
        raise CampaignMemoryError(f"{arts / 'hypothesis_card.yaml'} has no hypothesis_id")
    timeframe = card.get("timeframe")

    fault = ENGINEERING_FAULT_COMPONENT_ERROR if component_errors else None
    trials = _trial_ids_by_key(run_id, trial_sharpes)

    pr = _load_strict(arts / "protocol_result.yaml") if (arts / "protocol_result.yaml").exists() else {}
    protocol_file = (pr or {}).get("protocol_file")
    protocol_ref = None
    if protocol_file:
        p = Path(protocol_file)
        if protocol_root is not None:
            try:
                p = p.resolve().relative_to(Path(protocol_root).resolve())
            except (ValueError, OSError):
                pass
        protocol_ref = p.as_posix()

    if fault:
        # The grid is meaningless on a run with component errors: no status and
        # no grid numbers are recorded, only the fact of the fault and the
        # trials it spent.
        idea_status = None
        idea_status_reason = "not recorded: component_execution_error (the grid is meaningless on this run)"
        idea_status_ref = None
        grid = None
        grid_variants = None
    else:
        is_path = arts / "idea_status.yaml"
        idea = _load_mapping(is_path, "the grid's idea status")
        idea_status = idea.get("idea_status")
        if idea_status not in _IDEA_STATUSES:
            raise CampaignMemoryError(f"{is_path}: idea_status={idea_status!r} not one of {_IDEA_STATUSES}")
        if idea.get("run_id") != run_id:
            raise CampaignMemoryError(f"{is_path}: run_id={idea.get('run_id')!r} is not {run_id!r}")
        idea_status_reason = idea.get("reason")
        idea_status_ref = _ref(run_id, "artifacts/idea_status.yaml")
        grid_path = arts / "grid_evaluation.yaml"
        grid_doc = _load_mapping(grid_path, "the grid")
        if grid_doc.get("idea_status") != idea_status:
            raise CampaignMemoryError(f"{grid_path}: idea_status={grid_doc.get('idea_status')!r} "
                                      f"disagrees with idea_status.yaml ({idea_status!r})")
        grid = _grid_block(run_id, grid_doc, grid_path)
        grid_variants = grid["variants"]

    if grid_variants is None:
        # engineering fault: only the grid's column NAMES (which variants ran)
        # are used, never its cells; without a grid, what actually ran on disk.
        grid_path = arts / "grid_evaluation.yaml"
        cols = _load_mapping(grid_path, "the grid").get("variants") if grid_path.exists() else None
        if isinstance(cols, list) and cols:
            grid_variants = list(cols)
        else:
            index_path = arts / "variants" / "index.yaml"
            idx = (_load_mapping(index_path, "variant index").get("variants") or {}) \
                if index_path.exists() else {}
            grid_variants = [v for v in sorted(idx)
                             if (arts / "variants" / v / "protocol_result.yaml").exists()] or [run_id]
    variants = _variants_block(run_dir, run_id, grid_variants, trials, forecast_hash_fn)

    if fault:
        registry = {"skipped": "engineering_fault"}
    elif idea_status != "validated":
        registry = {"skipped": "not_validated"}
    else:
        registry = {"skipped": "not_built"}  # the block registry is E-058 S2b

    entry = {
        "run_id": run_id,
        "hypothesis_id": hyp_id,
        "legacy": False,
        "recorded_at": recorded_at or datetime.now(timezone.utc).isoformat(),
        "idea_status": idea_status,
        "idea_status_reason": idea_status_reason,
        "idea_status_ref": idea_status_ref,
        "engineering_fault": fault,
        "engineering_fault_detail": list(component_errors[:10]) if fault else [],
        "grid": grid,
        "variants": variants,
        "trial_ids": list(trials),
        "protocol_ref": protocol_ref,
        "timeframe": timeframe,
        "proposals": _proposals_block(run_dir, run_id, categories),
        "registry": registry,
        "profit_bars": None,
        "profit_bars_reason": PROFIT_BARS_NOT_EVALUATED,
        "kb_entry_id": None,
    }
    retired = _find_retired(entry)
    if retired:
        raise CampaignMemoryError(f"memory entry for {run_id} carries retired field(s) {retired}")
    return entry


def _fresh_doc() -> dict:
    return {"schema_version": SCHEMA_VERSION, "legacy_note": LEGACY_NOTE, "runs": {}}


def load_memory(path: Path) -> dict:
    """The memory document. Absent -> a fresh one. Anything that is not
    exactly this module's shape raises -- a malformed file is never
    overwritten with a fresh one (that would silently erase the record)."""
    path = Path(path)
    if not path.exists():
        return _fresh_doc()
    doc = _load_strict(path)
    if not isinstance(doc, dict):
        raise CampaignMemoryError(f"{path}: expected a mapping, got {type(doc).__name__}")
    if doc.get("schema_version") != SCHEMA_VERSION:
        raise CampaignMemoryError(f"{path}: schema_version={doc.get('schema_version')!r}, "
                                  f"expected {SCHEMA_VERSION}")
    runs = doc.get("runs")
    if not isinstance(runs, dict):
        raise CampaignMemoryError(f"{path}: runs is not a mapping")
    for key, entry in runs.items():
        if not isinstance(entry, dict) or entry.get("run_id") != key:
            raise CampaignMemoryError(f"{path}: runs.{key} is not an entry keyed by its own run_id")
    return doc


def _atomic_write(path: Path, doc: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            yaml.safe_dump(doc, f, sort_keys=False, allow_unicode=True)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def upsert_memory(path: Path, entry: dict) -> dict:
    """Insert or REPLACE (same run_id) one entry; atomic write (temp file +
    os.replace in the same directory). Returns the written document."""
    run_id = entry.get("run_id") if isinstance(entry, dict) else None
    if not isinstance(run_id, str) or not run_id:
        raise CampaignMemoryError(f"memory entry has no run_id: {entry!r}")
    retired = _find_retired(entry)
    if retired:
        raise CampaignMemoryError(f"memory entry for {run_id} carries retired field(s) {retired}")
    path = Path(path)
    doc = load_memory(path)
    doc["legacy_note"] = LEGACY_NOTE
    doc["runs"][run_id] = entry
    _atomic_write(path, doc)
    return doc
