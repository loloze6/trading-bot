"""
campaign_record/campaign_memory.yaml -- the per-run campaign memory
(E-058 S2a, delivery_plan_v26.md slice 6a; spec:
engineering/roadmap/E-058/S1_FINDINGS.md §3 and its operator decision).

Written ONLY by the orchestrator's `regroup_record` tool stage
(orchestrator.regroup_record.enabled, off by default), one entry per run keyed
by `run_id` and REPLACED on a re-run. Old runs are never backfilled: the
legacy record is campaign_knowledge_base.yaml.

Two entry forms:
  * full (build_memory_entry) -- a run without component errors;
  * fault-only (build_fault_entry) -- a run with component errors: only the
    fact of the fault, nothing parsed from its grid, variants or proposals.

What this module deliberately does NOT do:
  * decide anything. An entry's `idea_status` is copied from the grid's
    idea_status.yaml; nothing here computes or overrides a status.
  * read reader proposals for meaning. Proposal files are REFERENCED (path,
    proposal ids, count) and validated only so a malformed file fails loud.
    Their scores are never copied -- they rank the next candidate in the
    later decide-next step (slice 6b), and a copy here would invite a second
    reader to route on them.
  * write trial rows. campaign_state.trial_sharpes is written by
    protocol_execution; trial ids and forecast hashes are copied from it
    (read only).
  * carry retired machinery (slice 6c): no hypothesis_family, altitude,
    lineage routing, continuation or verdict-routing field. build_memory_entry
    and upsert_memory refuse an entry that contains one (RETIRED_FIELDS).
  * the block registry, the KB entry and the scoreboard (E-058 S2b). They
    live in tools/block_registry.py, tools/grid_kb_writer.py and
    tools/near_miss_scoreboard.py; the regroup_record stage fills this
    entry's `registry` and `kb_entry_id` from their results before the
    entry is written.

Importable without the orchestrator (same convention as reader_proposals.py):
every path is passed in by the caller, so tests' ROOT sandbox covers it.
"""
from __future__ import annotations

import contextlib
import os
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

import campaign_lock  # tools/ sibling: the E-011 O_EXCL lock file (pid/age staleness)
from workflow_artifact_validation import validate_workflow_artifact

SCHEMA_VERSION = 1

LEGACY_NOTE = (
    "Runs before the regroup_record stage (orchestrator.regroup_record.enabled) are not "
    "listed here and are never backfilled; their history is "
    "campaign_record/campaign_knowledge_base.yaml, where every entry without "
    "`legacy_schema: false` is legacy. Trial counts live in "
    "campaign_record/campaign_state.yaml -> trial_sharpes, not here."
)

ENGINEERING_FAULT_COMPONENT_ERROR = "component_execution_error"
# `profit_bars: null` + this reason: the branch-3 per-backtest check is off
# (orchestrator.profit_bars_every_backtest.enabled). When it is on, `profit_bars`
# holds the per-variant results (profit_bars_block) and the reason is null.
PROFIT_BARS_NOT_EVALUATED = "not evaluated before regroup"
# artifacts/profit_bars_evaluation.yaml written by the per-backtest check
# (run_phase1_research._evaluate_profit_bars_every_backtest). The promote-path
# check writes the same file WITHOUT a scope (one candidate, no variants), which
# this module must never mistake for per-variant results. THE one definition:
# the writer reads it from here (run_phase1_research._profit_bars_scope_every_backtest).
PROFIT_BARS_SCOPE_EVERY_BACKTEST = "every_backtest"
_PROFIT_RESULTS = ("PASS", "FAIL")
# INVALIDATED: tested on this attempt, but its trial row is invalidated_artifact
# (conformance violation) -- never graded, never passing.
_PROFIT_VARIANT_RESULTS = ("PASS", "FAIL", "NOT_TESTED", "INVALIDATED")
_PROFIT_TESTED_RESULTS = ("PASS", "FAIL", "INVALIDATED")
_PROFIT_BAR_RESULTS = ("PASS", "FAIL", "NOT_EVALUABLE")
# memory entry `registry: {skipped: ...}` reasons (E-058 S2b; tools/block_registry.py)
REGISTRY_SKIPPED_NOT_VALIDATED = "not_validated"
REGISTRY_SKIPPED_NO_MANIFEST = "no_manifest"
# E-060 S3b (guess 11): a composition run -- a composite never registers as a block.
REGISTRY_SKIPPED_COMPOSITION = "composition"

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
# artifacts/variants/index.yaml: the only statuses and keys its writers produce
# (run_tool_worker's backtest_specification and per-variant data gate).
_INDEX_STATUSES = ("validated", "not_tested")
# failed_attempt (E-061 C2 S2a, D-015): the prefixed reason protocol_execution
# persists for a variant refused / failed on an attempt of this run, carried into
# every later attempt's failed_variants unless that variant is re-run successfully.
# kind / symbol / protocol_path / protocol_sha256 / coverage (E-061 C2 S2b, one
# coin per variant): written by 5a under orchestrator.variant_loop for a
# per-coin variant -- its kind (base | design | asset), its coin_universe.yaml
# coin, its own protocol file and that file's sha256, and, for an asset coin,
# the windows that coin covers (D-042). run_protocol_sha256 (E-062 S2b-3b review
# fix 1): the sha256 of the run protocol 5a froze (artifacts/variants/
# run_protocol.json) for that per-coin variant.
_INDEX_KEYS = frozenset({"status", "reason", "config_path", "report", "failed_attempt",
                         "kind", "symbol", "protocol_path", "protocol_sha256", "coverage",
                         "run_protocol_sha256"})
_INDEX_KINDS = ("base", "design", "asset")  # variant_coin.VARIANT_KINDS

MEMORY_LOCK_FILENAME = ".campaign_memory.lock"
MEMORY_LOCK_WAIT_SECONDS = 30.0
_MEMORY_LOCK_POLL_SECONDS = 0.05


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


def _protocol_shape(pr, where: str) -> dict:
    """Symbols and DISTINCT windows. protocol_result.results has one row per
    (symbol, window), so len(results) would count 30 for 15 windows x 2
    symbols (run_054)."""
    results = (pr or {}).get("results") or []
    if not isinstance(results, list):
        raise CampaignMemoryError(f"{where}: results is not a list")
    symbols, windows = set(), set()
    for i, r in enumerate(results):
        window = r.get("window") if isinstance(r, dict) else None
        if not isinstance(window, str) or not window:
            raise CampaignMemoryError(f"{where}: results[{i}] has no window label ({window!r})")
        windows.add(window)
        if r.get("symbol"):
            symbols.add(r["symbol"])
    return {"symbols": sorted(symbols), "n_windows": len(windows)}


def _trial_rows(run_id: str, trial_sharpes) -> dict:
    """{trial_id: {source: row}} for this run's backtest / backtest_failed
    rows. Read-only: nothing here writes the ledger."""
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
            out.setdefault(tid, {})[row["source"]] = row
    return out


def _tested_trial(trials: dict, tid: str, vid: str) -> tuple:
    """A tested variant spent a look, so its "backtest" row MUST exist (the
    ledger invariant); its forecast_hash is copied from that row, never
    recomputed from a config file that may have changed since."""
    row = (trials.get(tid) or {}).get("backtest")
    if row is None:
        raise CampaignMemoryError(
            f"variant {vid!r} was tested but campaign_state.trial_sharpes has no 'backtest' "
            f"row for trial_id {tid!r} -- the trial ledger is missing a spent look")
    fh = row.get("forecast_hash")
    if not isinstance(fh, str) or not fh:
        raise CampaignMemoryError(f"trial row {tid!r} (backtest) has no forecast_hash ({fh!r})")
    return tid, fh


def _windows_field(row, where: str) -> dict:
    """E-062 S2b-3c (D-047 (5), S2B3_FINDINGS.md G11): {"windows_sha256": ...}
    copied from a variant's trial row when the row carries it (a partial-
    coverage per-coin variant graded under orchestrator.profit_bars_v2), else
    {} -- the memory variant then has exactly its pre-S2b-3c keys. Copied, never
    recomputed (the same rule as forecast_hash): the repeat key
    (novelty.match_index) then reads the fingerprint the DSR dedupe counted.
    A malformed value raises."""
    if not isinstance(row, dict) or "windows_sha256" not in row:
        return {}
    import novelty as _nov  # tools/ sibling: THE fingerprint check
    try:
        return {"windows_sha256": _nov.check_windows_sha256(row["windows_sha256"], where)}
    except _nov.NoveltyError as exc:
        raise CampaignMemoryError(str(exc)) from exc


def _check_index_entry(vid, info, index_path: Path) -> None:
    if not isinstance(info, dict):
        raise CampaignMemoryError(f"{index_path}: variants.{vid} is not a mapping ({info!r})")
    extra = sorted(set(info) - _INDEX_KEYS)
    if extra:
        raise CampaignMemoryError(f"{index_path}: variants.{vid} has unknown key(s) {extra}")
    if info.get("status") not in _INDEX_STATUSES:
        raise CampaignMemoryError(f"{index_path}: variants.{vid}.status={info.get('status')!r} "
                                  f"is not one of {_INDEX_STATUSES}")
    for key in ("config_path", "reason", "failed_attempt", "symbol", "protocol_path",
                "protocol_sha256", "run_protocol_sha256"):
        if info.get(key) is not None and not isinstance(info[key], str):
            raise CampaignMemoryError(f"{index_path}: variants.{vid}.{key} is not a string")
    if "kind" in info and info["kind"] not in _INDEX_KINDS:
        raise CampaignMemoryError(f"{index_path}: variants.{vid}.kind={info['kind']!r} is not one "
                                  f"of {_INDEX_KINDS}")
    if info.get("coverage") is not None and not isinstance(info["coverage"], dict):
        raise CampaignMemoryError(f"{index_path}: variants.{vid}.coverage is not a mapping")
    if info["status"] == "validated" and not info.get("config_path"):
        raise CampaignMemoryError(f"{index_path}: variants.{vid} is validated but has no config_path")


def _grid_failed_variants(grid_doc: dict, path: Path) -> dict:
    """The grid's `failed_variants` (E-061 C2 S2a, D-015) through the evaluator's
    own validator (verdict_criteria_evaluator.grid_failed_variants, shared with
    branch 3): {} when absent; a present but malformed value raises."""
    import verdict_criteria_evaluator as _vce  # tools/ sibling, imported lazily
    try:
        return _vce.grid_failed_variants(grid_doc)
    except ValueError as exc:
        raise CampaignMemoryError(f"{path}: {exc}") from exc


def _variants_block(run_dir: Path, run_id: str, grid_variants: list, trials: dict,
                    failed_variants: dict | None = None) -> dict:
    """Two grid-column shapes, told apart by the grid's own columns:
      * variant loop (columns are index.yaml variant ids): every index entry
        -- tested (a grid column; must be `validated` in the index), failed
        (in the grid's failed_variants with a `backtest_failed:` reason
        (E-061 C2 S2a, D-015), or -- a grid written before S2a -- validated
        with no column: its backtest failed), or not_tested (in
        failed_variants with a `refused:` reason -- refused before any
        backtest, no trial row -- or any other not_tested index entry).
        The grid's columns are graded variants only; a failed variant is
        never a column.
      * single column named after run_id (variant loop off -- including
        config-direct authoring, which writes index.yaml but backtests only
        the base config): from artifacts/protocol_result.yaml.
    Any index status or entry shape outside the known set raises."""
    arts = run_dir / "artifacts"
    index_path = arts / "variants" / "index.yaml"
    failed_variants = failed_variants or {}
    import verdict_criteria_evaluator as _vce  # tools/ sibling, imported lazily
    refused_prefix = _vce.FAILED_VARIANT_REFUSED
    out = {}
    index = None
    if index_path.exists():
        index = _load_mapping(index_path, "variant index").get("variants")
        if not isinstance(index, dict):
            raise CampaignMemoryError(f"{index_path}: variants is not a mapping")
        for vid, info in index.items():
            _check_index_entry(vid, info, index_path)
    if index is not None and not (grid_variants == [run_id] and run_id not in index):
        unknown = [v for v in list(grid_variants) + list(failed_variants) if v not in index]
        if unknown:
            raise CampaignMemoryError(f"{index_path}: grid / failed variant(s) {unknown} not in "
                                      f"the index")
        for vid in sorted(index):
            info = index[vid]
            tid = f"{run_id}:{vid}"
            failed_reason = failed_variants.get(vid)
            refused = failed_reason is not None and failed_reason.startswith(refused_prefix)
            wfield: dict = {}  # E-062 S2b-3c: the trial row's window fingerprint, if any
            if vid in grid_variants:
                if info["status"] != "validated":
                    raise CampaignMemoryError(
                        f"{index_path}: grid column {vid!r} has index status {info['status']!r} "
                        f"-- only a validated variant can have been backtested")
                status, reason = "tested", None
                trial_id, fh = _tested_trial(trials, tid, vid)
                wfield = _windows_field((trials.get(tid) or {}).get("backtest"),
                                        f"trial row {tid!r} (backtest)")
                vpr_path = arts / "variants" / vid / "protocol_result.yaml"
                shape = _protocol_shape(_load_mapping(vpr_path, f"variant {vid}'s backtest result"),
                                        str(vpr_path))
            elif (failed_reason is not None and not refused) or (
                    failed_reason is None and info["status"] == "validated"):
                status = "failed"
                reason = (failed_reason if failed_reason is not None
                          else "validated but produced no grid column (backtest failed)")
                failed_row = (trials.get(tid) or {}).get("backtest_failed")
                trial_id = tid if failed_row is not None else None
                fh = failed_row.get("forecast_hash") if failed_row is not None else None
                wfield = _windows_field(failed_row, f"trial row {tid!r} (backtest_failed)")
                shape = {"symbols": [], "n_windows": 0}
            else:
                status, reason = "not_tested", (failed_reason if refused else info.get("reason"))
                trial_id, fh = None, None
                shape = {"symbols": [], "n_windows": 0}
            cfg_rel = info.get("config_path")
            cfg_rel = Path(cfg_rel).as_posix() if cfg_rel else None
            out[vid] = {
                "status": status, "reason": reason,
                "config_ref": _ref(run_id, cfg_rel) if cfg_rel else None,
                "forecast_hash": fh,
                "symbols": shape["symbols"], "n_windows": shape["n_windows"],
                "trial_id": trial_id,
                **wfield,
            }
        return out
    if failed_variants:
        raise CampaignMemoryError(
            f"{run_dir}: failed_variants {sorted(failed_variants)} on a single-column grid -- "
            f"only the variant loop records failed variants")
    if grid_variants != [run_id]:
        raise CampaignMemoryError(
            f"{run_dir}: no artifacts/variants/index.yaml, so the grid must have the single "
            f"column {run_id!r}; got {grid_variants}")
    pr_path = arts / "protocol_result.yaml"
    shape = _protocol_shape(_load_mapping(pr_path, "protocol_execution output"), str(pr_path))
    trial_id, fh = _tested_trial(trials, run_id, run_id)
    cfg = arts / "candidate_strategy_config.json"
    out[run_id] = {
        "status": "tested", "reason": None,
        "config_ref": _ref(run_id, "artifacts/candidate_strategy_config.json") if cfg.exists() else None,
        "forecast_hash": fh,
        "symbols": shape["symbols"], "n_windows": shape["n_windows"],
        "trial_id": trial_id,
    }
    return out


def _proposals_block(run_dir: Path, run_id: str, categories) -> list:
    """References only. Validated fail-loud by reader_proposals.load_proposals
    (the same check the readers stage applies); only ids and counts are kept."""
    import reader_proposals  # tools/ sibling; imported lazily for the caller's sys.path
    pdir = run_dir / "artifacts" / "proposals"
    loaded = reader_proposals.load_proposals(pdir, list(categories))
    # E-068 slice 5: a reader skipped by a code rule (or refused after its
    # retry) says so -- a count of 0 alone would read as "nothing to propose".
    # Only v3 skipped readings carry the key, so every other entry is unchanged.
    readings = reader_proposals.load_readings(pdir, list(categories))
    return [{
        "category": cat,
        "ref": _ref(run_id, f"artifacts/proposals/{cat}.yaml") if (pdir / f"{cat}.yaml").exists() else None,
        "proposal_ids": [p["proposal_id"] for p in loaded[cat]],
        "count": len(loaded[cat]),
        **({"skipped": dict(readings[cat]["skipped"])}
           if "skipped" in (readings.get(cat) or {}) else {}),
    } for cat in categories]


def profit_bars_block(run_dir: Path, run_id: str, variants: dict) -> dict:
    """The memory's `profit_bars` value from the per-backtest check's
    artifacts/profit_bars_evaluation.yaml: one result per variant, each bar's
    result/actual/threshold and the passing variants (the profit_bars_reached
    stop, if any, is raised after this record). `variants` is this entry's own variants block; the two must
    describe the same variants (a tested variant was graded or invalidated, an
    untested or failed one was not), else this raises -- e.g. a stale
    protocol_result graded for a variant whose backtest failed on this pass.
    Read only; decides nothing (the stop is raised by the route after
    regroup_record, never here)."""
    path = Path(run_dir) / "artifacts" / "profit_bars_evaluation.yaml"
    doc = _load_mapping(path, "the per-backtest profit-bars evaluation "
                              "(orchestrator.profit_bars_every_backtest.enabled is on)")
    if doc.get("scope") != PROFIT_BARS_SCOPE_EVERY_BACKTEST:
        raise CampaignMemoryError(
            f"{path}: scope={doc.get('scope')!r}, expected {PROFIT_BARS_SCOPE_EVERY_BACKTEST!r} "
            f"(a promote-path evaluation has one candidate and no per-variant results)")
    if doc.get("run_id") != run_id:
        raise CampaignMemoryError(f"{path}: run_id={doc.get('run_id')!r} is not {run_id!r}")
    result, passing = doc.get("result"), doc.get("passing")
    if result not in _PROFIT_RESULTS:
        raise CampaignMemoryError(f"{path}: result={result!r} not one of {_PROFIT_RESULTS}")
    graded = doc.get("variants")
    if not isinstance(graded, dict) or not graded:
        raise CampaignMemoryError(f"{path}: variants must be a non-empty mapping")
    out_variants = {}
    for vid in sorted(graded):
        v = graded[vid]
        where = f"{path}: variants.{vid}"
        if not isinstance(v, dict) or v.get("result") not in _PROFIT_VARIANT_RESULTS:
            raise CampaignMemoryError(f"{where}: result must be one of {_PROFIT_VARIANT_RESULTS}")
        bars = v.get("bars")
        if not isinstance(bars, list) or (v["result"] in ("PASS", "FAIL")) != bool(bars):
            raise CampaignMemoryError(f"{where}: bars must be a list, non-empty exactly when "
                                      f"the variant was graded (PASS/FAIL)")
        compact = {}
        for i, b in enumerate(bars):
            if (not isinstance(b, dict) or not isinstance(b.get("name"), str)
                    or b.get("result") not in _PROFIT_BAR_RESULTS or b["name"] in compact):
                raise CampaignMemoryError(f"{where}.bars[{i}]: needs a unique name and a result "
                                          f"in {_PROFIT_BAR_RESULTS} ({b!r})")
            compact[b["name"]] = {"result": b["result"], "actual": b.get("actual"),
                                  "threshold": b.get("threshold")}
        if bars:
            every_pass = all(c["result"] == "PASS" for c in compact.values())
            if every_pass != (v["result"] == "PASS"):
                raise CampaignMemoryError(f"{where}: result={v['result']!r} disagrees with its bars")
        out_variants[vid] = {"result": v["result"], "bars": compact}
    expected_passing = sorted(vid for vid, v in out_variants.items() if v["result"] == "PASS")
    if passing != expected_passing or result != ("PASS" if expected_passing else "FAIL"):
        raise CampaignMemoryError(f"{path}: result={result!r}/passing={passing!r} disagree with "
                                  f"the per-variant results (passing {expected_passing})")
    if set(out_variants) != set(variants):
        raise CampaignMemoryError(f"{path}: graded variants {sorted(out_variants)} are not this "
                                  f"entry's variants {sorted(variants)}")
    for vid, mv in variants.items():
        tested = mv.get("status") == "tested"
        if tested != (out_variants[vid]["result"] in _PROFIT_TESTED_RESULTS):
            raise CampaignMemoryError(
                f"{path}: variant {vid!r} is {mv.get('status')!r} in the memory but "
                f"{out_variants[vid]['result']!r} in the profit-bars evaluation -- the two must "
                f"describe the same backtests (stale protocol_result.yaml?)")
    return {"ref": _ref(run_id, "artifacts/profit_bars_evaluation.yaml"),
            "scope": PROFIT_BARS_SCOPE_EVERY_BACKTEST, "result": result,
            "passing": expected_passing, "variants": out_variants}


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


def _now(recorded_at):
    return recorded_at or datetime.now(timezone.utc).isoformat()


def protocol_component_errors(run_dir: Path, *, load) -> list:
    """Every results[*] entry whose component_errors.count > 0, in
    artifacts/protocol_result.yaml and (variant loop) in each
    artifacts/variants/<id>/protocol_result.yaml -- the grid reads every
    variant, so an error in any of them makes it meaningless. Missing
    protocol_result.yaml, or a present but malformed component_errors block,
    raises: an unreadable error count is not a zero one. An absent/null
    block (component_errors off for that window) counts as none.

    THE one definition (moved verbatim from
    run_phase1_research._protocol_component_errors, E-036 S2b), shared by the
    orchestrator's regroup_record and tools/replay_repeat_gate.py. `load` is
    the caller's YAML reader (the orchestrator passes its load_yaml)."""
    run_dir = Path(run_dir)
    artifacts = run_dir / "artifacts"
    sources = [artifacts / "protocol_result.yaml"]
    if not sources[0].exists():
        raise FileNotFoundError(f"{sources[0]} is missing -- cannot check component errors")
    variants_dir = artifacts / "variants"
    if variants_dir.exists():
        sources += sorted(p / "protocol_result.yaml" for p in variants_dir.iterdir()
                          if p.is_dir() and (p / "protocol_result.yaml").exists())
    errors = []
    for src in sources:
        pr = load(src) or {}
        results = pr.get("results") or []
        if not isinstance(results, list):
            raise ValueError(f"{src}: results is not a list ({type(results).__name__})")
        for i, r in enumerate(results):
            ce = r.get("component_errors") if isinstance(r, dict) else None
            if ce is None:
                continue
            count = ce.get("count") if isinstance(ce, dict) else None
            if isinstance(count, bool) or not isinstance(count, int) or count < 0:
                raise ValueError(f"{src}: results[{i}].component_errors is malformed ({ce!r}) "
                                 f"-- expected {{count: <int >= 0>, samples: [...]}}")
            if count > 0:
                errors.append(f"{src.relative_to(run_dir).as_posix()} results[{i}] "
                              f"({r.get('symbol')}/{r.get('window')}): "
                              f"component_errors.count={count}")
    return errors


def build_fault_entry(run_dir: Path, run_id: str, component_errors: list,
                      recorded_at: str | None = None) -> dict:
    """The minimal, fault-only entry for a run with component errors. Its grid,
    variant results and proposals are meaningless (or absent), so none of
    them is parsed: only the fact of the fault. hypothesis_id is recorded when
    hypothesis_card.yaml is readable, else null -- this entry must be
    buildable on a broken run, because the component_execution_error pause
    that follows it must still fire."""
    if not component_errors:
        raise CampaignMemoryError("build_fault_entry called without component errors")
    hyp_id = None
    with contextlib.suppress(Exception):
        card = yaml.safe_load((Path(run_dir) / "artifacts" / "hypothesis_card.yaml")
                              .read_text(encoding="utf-8"))
        value = card.get("hypothesis_id") if isinstance(card, dict) else None
        if isinstance(value, str) and value.strip():
            hyp_id = value
    return {
        "run_id": run_id,
        "hypothesis_id": hyp_id,
        "legacy": False,
        "recorded_at": _now(recorded_at),
        "engineering_fault": ENGINEERING_FAULT_COMPONENT_ERROR,
        "engineering_fault_detail": [str(e) for e in component_errors[:10]],
    }


def protocol_ref_of(protocol_file, protocol_root: Path | None = None):
    """A memory entry's `protocol_ref`: protocol_result.yaml's `protocol_file`
    (the path tools/run_protocol.py was given), relative to `protocol_root`
    when it lies under it, POSIX separators; None when absent. THE one
    definition -- the 5a exact-match gate (E-036 S2a) derives a candidate's
    protocol_ref with it, so both sides of the key come from one rule."""
    if not protocol_file:
        return None
    p = Path(protocol_file)
    if protocol_root is not None:
        with contextlib.suppress(ValueError, OSError):
            p = p.resolve().relative_to(Path(protocol_root).resolve())
    return p.as_posix()


def per_coin_index(run_dir: Path) -> bool:
    """True when the run's artifacts/variants/index.yaml has a per-coin entry
    (a `protocol_path`, written by 5a under one coin per variant, E-061 C2
    S2b). False when there is no index or no such entry."""
    index_path = Path(run_dir) / "artifacts" / "variants" / "index.yaml"
    if not index_path.exists():
        return False
    variants = _load_mapping(index_path, "variant index").get("variants")
    return isinstance(variants, dict) and any(
        isinstance(v, dict) and v.get("protocol_path") for v in variants.values())


def _check_validated_is_whole(run_dir: Path, run_id: str, grid_doc: dict, grid_path: Path,
                              failed_variants: dict, variants: dict) -> None:
    """CUL-342 item 2 (E-061 C2 S2b), the belt before the block registry: a
    `validated` idea must have had EVERY variant graded in this run (card D,
    D-015). The grid's own rollup already refuses to validate otherwise; this
    re-checks what reaches block_registry.record_run, so a grid written before
    S2a (no failed/untested keys) or edited by hand cannot register a block on
    part of an idea. Raises CampaignMemoryError on any of:
      * a non-empty `failed_variants`, `untested_variants` or (review fix M1)
        `partial_coverage_variants` in the grid;
      * a memory variant that is not `tested`;
      * the single-column path (variant loop off) while
        artifacts/variants/index.yaml lists a variant other than `base`: only
        the base config ran, the idea's other variants never did."""
    problems = []
    if failed_variants:
        problems.append(f"failed_variants {sorted(failed_variants)}")
    untested = grid_doc.get("untested_variants")
    if untested:
        problems.append(f"untested_variants "
                        f"{sorted(untested) if isinstance(untested, dict) else untested!r}")
    # E-061 C2 S2b review fix M1 (TEMPORARY, D-042; lifted by E-062 S2b): a
    # variant graded on partial coverage never validates an idea yet.
    partial = grid_doc.get("partial_coverage_variants")
    if partial:
        problems.append(f"partial_coverage_variants "
                        f"{sorted(partial) if isinstance(partial, dict) else partial!r}")
    not_tested = sorted(vid for vid, v in variants.items() if v.get("status") != "tested")
    if not_tested:
        problems.append(f"variant(s) {not_tested} not tested "
                        f"({ {vid: variants[vid].get('status') for vid in not_tested} })")
    index_path = Path(run_dir) / "artifacts" / "variants" / "index.yaml"
    if list(variants) == [run_id] and index_path.exists():
        index = _load_mapping(index_path, "variant index").get("variants")
        others = sorted(v for v in (index or {}) if v != "base")
        if others:
            problems.append(f"only the base config ran (single column {run_id!r}, variant loop "
                            f"off) while {index_path} lists {others}")
    if problems:
        raise CampaignMemoryError(
            f"{grid_path}: idea_status 'validated' but not every variant of the idea was graded "
            f"in this run -- {'; '.join(problems)}. An idea validates only when all its variants "
            f"are graded (card D, D-015); refusing to record it (the block registry would "
            f"register a block on part of an idea).")


def build_memory_entry(run_dir: Path, run_id: str, *, trial_sharpes, categories,
                       protocol_root: Path | None = None, recorded_at: str | None = None,
                       profit_bars_evaluated: bool = False,
                       run_protocol_file=None) -> dict:
    """One run's full memory entry (a run WITHOUT component errors -- see
    build_fault_entry for those), from artifacts that exist under the flag.
    `trial_sharpes` (campaign_state, read only) and `categories` (the reader
    categories) are passed in. `profit_bars_evaluated` is True when the
    per-backtest profit-bars check is on (the caller reads
    orchestrator.profit_bars_every_backtest.enabled): `profit_bars` is then the
    per-variant block from artifacts/profit_bars_evaluation.yaml (required) and
    its reason null; False keeps `profit_bars: null` + PROFIT_BARS_NOT_EVALUATED.
    `run_protocol_file` (E-061 C2 S2b review fix M3): the RUN protocol, which
    `protocol_ref` names for a per-coin run (artifacts/variants/index.yaml
    carries a `protocol_path`) -- there artifacts/protocol_result.yaml mirrors
    one variant's OWN protocol.json (one coin, possibly partial windows), so its
    protocol_file is not the run's protocol. Required for a per-coin run
    (raises without it); ignored otherwise, where protocol_ref stays
    protocol_result.yaml's protocol_file exactly as before.
    Raises CampaignMemoryError on any malformed or inconsistent input."""
    run_dir = Path(run_dir)
    arts = run_dir / "artifacts"
    card = _load_mapping(arts / "hypothesis_card.yaml", "the idea's identity (hypothesis_id)")
    hyp_id = card.get("hypothesis_id")
    if not isinstance(hyp_id, str) or not hyp_id.strip():
        raise CampaignMemoryError(f"{arts / 'hypothesis_card.yaml'} has no hypothesis_id")
    timeframe = card.get("timeframe")
    if timeframe is not None and not isinstance(timeframe, str):
        raise CampaignMemoryError(f"{arts / 'hypothesis_card.yaml'}: timeframe={timeframe!r} is not "
                                  f"a string (campaign_memory.schema.json: string or null)")

    trials = _trial_rows(run_id, trial_sharpes)

    pr = _load_mapping(arts / "protocol_result.yaml", "protocol_execution output")
    if per_coin_index(run_dir):
        if not run_protocol_file:
            raise CampaignMemoryError(
                f"{run_dir}: a per-coin run (index.yaml protocol_path) records the RUN protocol as "
                f"protocol_ref, and no run_protocol_file was given -- protocol_result.yaml's "
                f"protocol_file is one variant's own protocol.json")
        protocol_ref = protocol_ref_of(str(run_protocol_file), protocol_root)
    else:
        protocol_ref = protocol_ref_of(pr.get("protocol_file"), protocol_root)

    is_path = arts / "idea_status.yaml"
    idea = _load_mapping(is_path, "the grid's idea status")
    idea_status = idea.get("idea_status")
    if idea_status not in _IDEA_STATUSES:
        raise CampaignMemoryError(f"{is_path}: idea_status={idea_status!r} not one of {_IDEA_STATUSES}")
    if idea.get("run_id") != run_id:
        raise CampaignMemoryError(f"{is_path}: run_id={idea.get('run_id')!r} is not {run_id!r}")
    grid_path = arts / "grid_evaluation.yaml"
    grid_doc = _load_mapping(grid_path, "the grid")
    if grid_doc.get("idea_status") != idea_status:
        raise CampaignMemoryError(f"{grid_path}: idea_status={grid_doc.get('idea_status')!r} "
                                  f"disagrees with idea_status.yaml ({idea_status!r})")
    grid = _grid_block(run_id, grid_doc, grid_path)
    failed_variants = _grid_failed_variants(grid_doc, grid_path)
    variants = _variants_block(run_dir, run_id, grid["variants"], trials, failed_variants)
    if idea_status == "validated":
        _check_validated_is_whole(run_dir, run_id, grid_doc, grid_path, failed_variants,
                                  variants)

    entry = {
        "run_id": run_id,
        "hypothesis_id": hyp_id,
        "legacy": False,
        "recorded_at": _now(recorded_at),
        "idea_status": idea_status,
        "idea_status_reason": idea.get("reason"),
        "idea_status_ref": _ref(run_id, "artifacts/idea_status.yaml"),
        "engineering_fault": None,
        "engineering_fault_detail": [],
        "grid": grid,
        "variants": variants,
        "trial_ids": list(trials),
        "protocol_ref": protocol_ref,
        "timeframe": timeframe,
        "proposals": _proposals_block(run_dir, run_id, categories),
        # Filled by the regroup_record stage from tools/block_registry.py
        # (E-058 S2b): {"block_ids": [...]} or {"skipped": <reason>}.
        "registry": ({"skipped": REGISTRY_SKIPPED_NOT_VALIDATED} if idea_status != "validated"
                     else None),
        "profit_bars": (profit_bars_block(run_dir, run_id, variants) if profit_bars_evaluated
                        else None),
        "profit_bars_reason": None if profit_bars_evaluated else PROFIT_BARS_NOT_EVALUATED,
        # Filled by the stage from tools/grid_kb_writer.py (E-058 S2b).
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


# E-036 S2a: the idea-writing stages' "already tried" view (below). Bounds the
# prompt: only the most recently recorded runs are listed, the rest counted.
TRIED_IDEAS_MAX_ROWS = 200
TRIED_IDEAS_NOTE = (
    "What was already tried: one row per run recorded in "
    "campaign_record/campaign_memory.yaml -- the idea (hypothesis_id), the coins its "
    "tested variants ran on, the timeframe of the protocol it ran, and the grid's "
    "idea_status (validated / refuted / inconclusive; null for an engineering fault). "
    "No family grouping: an idea's identity is its hypothesis_id. Derived fresh from "
    "the memory for this stage; never edited by hand."
)


def tried_ideas(memory: dict, *, root: Path, max_rows: int = TRIED_IDEAS_MAX_ROWS) -> dict:
    """E-036 S2a (slice 8.1, operator decision 3): the compact, rebuildable
    view of the memory that the idea-writing stages (hypothesis_generation,
    innovation_expansion) get as an optional prompt input under
    orchestrator.exclusion_digest_input. Read only; decides nothing.

    One row per memory entry, oldest first by recorded_at (run_id breaks
    ties), at most `max_rows` (the most recent; the rest counted in
    `omitted_older_runs`): {run_id, hypothesis_id, symbols (the tested
    variants' measured symbols), timeframe (the protocol file's, else the
    card's -- tools/novelty.py's rule), idea_status, variants_tested} plus
    `engineering_fault` on a fault entry. `root` is strategy-research/ (a
    memory entry's protocol_ref is relative to it). An unreadable protocol
    file is listed under `warnings` (key present only then)."""
    import novelty as _nov  # tools/ sibling, imported lazily for the caller's sys.path
    runs = (memory or {}).get("runs") or {}
    ordered = sorted(runs.values(), key=lambda e: (str(e.get("recorded_at") or ""), str(e.get("run_id"))))
    kept = ordered[-max_rows:] if max_rows and len(ordered) > max_rows else ordered
    warnings: list = []
    # The one protocol-spec loop (novelty.protocol_specs), over the kept rows
    # only; an unreadable protocol never crashes the prompt -- the row falls
    # back to the card timeframe and the problem is listed in `warnings`.
    specs = _nov.protocol_specs(root, {"runs": {e.get("run_id"): e for e in kept}},
                                warnings=warnings)
    rows = []
    for e in kept:
        tested = [v for v in (e.get("variants") or {}).values()
                  if isinstance(v, dict) and v.get("status") == "tested"]
        ref = _nov.normalize_ref(e.get("protocol_ref"))
        spec = specs.get(ref) if ref else None
        row = {
            "run_id": e.get("run_id"),
            "hypothesis_id": e.get("hypothesis_id"),
            "symbols": sorted({s for v in tested for s in (v.get("symbols") or [])}),
            "timeframe": (spec or {}).get("timeframe") or _nov.normalize_timeframe(e.get("timeframe")),
            "idea_status": e.get("idea_status"),
            "variants_tested": len(tested),
        }
        if e.get("engineering_fault"):
            row["engineering_fault"] = e["engineering_fault"]
        rows.append(row)
    view = {"source": "campaign_record/campaign_memory.yaml", "note": TRIED_IDEAS_NOTE,
            "max_rows": max_rows, "runs_in_memory": len(runs),
            "omitted_older_runs": len(ordered) - len(kept), "runs": rows}
    if warnings:
        view["warnings"] = warnings
    return view


def _atomic_write(path: Path, doc: dict) -> None:
    """Temp file + os.replace in the same directory (also used by
    tools/block_registry.py and tools/grid_kb_writer.py, E-058 S2b)."""
    path = Path(path)
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


@contextlib.contextmanager
def _file_lock(lock_path: Path, what: str, error_cls=None, wait_seconds: float | None = None):
    """Exclusive lock around a read-modify-write, so two writers cannot lose
    each other's entry. Reuses the E-011 campaign lock primitive
    (tools/campaign_lock.py: O_CREAT|O_EXCL file, cleared only when its pid
    is confirmed dead on this host or it is older than the stale threshold)
    on its own lock file, with a bounded wait; a lock still held after the
    wait raises `error_cls` instead of writing unlocked. Shared with
    tools/block_registry.py and tools/grid_kb_writer.py (E-058 S2b)."""
    error_cls = error_cls or CampaignMemoryError
    wait = MEMORY_LOCK_WAIT_SECONDS if wait_seconds is None else wait_seconds
    lock_path = Path(lock_path)
    deadline = time.monotonic() + wait
    while True:
        try:
            campaign_lock.acquire(lock_path)
            break
        except campaign_lock.CampaignLockHeld as exc:
            if time.monotonic() >= deadline:
                raise error_cls(
                    f"{lock_path} still held after {wait}s -- another writer "
                    f"is updating {what} (or left a live lock). Not writing unlocked. "
                    f"{exc}") from exc
            time.sleep(_MEMORY_LOCK_POLL_SECONDS)
    try:
        yield
    finally:
        campaign_lock.release(lock_path)


def _memory_lock(path: Path):
    return _file_lock(Path(path).parent / MEMORY_LOCK_FILENAME, "the campaign memory")


def upsert_memory(path: Path, entry: dict) -> dict:
    """Insert or REPLACE (same run_id) one entry, under _memory_lock; atomic
    write (temp file + os.replace in the same directory). The document is
    checked against workflow_artifacts/schemas/campaign_memory.schema.json by
    validate_workflow_artifact (matched by file stem) before it is written:
    warn by default, blocking under WORKFLOW_ARTIFACT_VALIDATION=raise.
    Returns the written document."""
    run_id = entry.get("run_id") if isinstance(entry, dict) else None
    if not isinstance(run_id, str) or not run_id:
        raise CampaignMemoryError(f"memory entry has no run_id: {entry!r}")
    retired = _find_retired(entry)
    if retired:
        raise CampaignMemoryError(f"memory entry for {run_id} carries retired field(s) {retired}")
    path = Path(path)
    with _memory_lock(path):
        doc = load_memory(path)
        doc["legacy_note"] = LEGACY_NOTE
        doc["runs"][run_id] = entry
        validate_workflow_artifact(path, doc)
        _atomic_write(path, doc)
    return doc
