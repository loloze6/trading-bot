"""
replay_repeat_gate -- E-036 S2b (delivery_plan_v26.md slice 8): a READ-ONLY
replay of the 5a exact-match repeat gate (tools/novelty.py via
tools/anti_adjacency_gate.py) over the real past corpus runs/run_*, next to
what the retired family-grain layer 2 (build_exclusion_digest.
legacy_family_lookup) said for the same run. Findings:
engineering/roadmap/E-036/S2B_REPLAY.md.

Nothing here decides anything or writes under the corpus: no backtest, no
market data, no API call, no orchestrator import. The only file written is
the result YAML (CLI --out), and the CLI refuses an --out under --runs-dir.

WHAT IS REPLAYED
Runs are taken in run-number order, as chronological (run_9 before
run_010). Each run plays two roles:

  1. CANDIDATE at 5a -- the config its backtest ran,
     artifacts/candidate_strategy_config.json (the file the legacy
     backtest_specification flow writes, F4d's significance_methodology
     injection included, and the file its trial row is hashed from), on the
     protocol it ran. Its key is built exactly as
     run_phase1_research._repeat_gate_context/_check_variant_repeat build it:
     novelty.forecast_hash_of_config(config) (_compute_forecast_hash's
     canonicalisation), the protocol file's `symbols` (read strictly),
     anti_adjacency_gate.candidate_key, and anti_adjacency_gate.
     layer2_digest_check against novelty.match_index over the memory of
     EARLIER runs only, with this run excluded (exclude_run_id), as live.
     Protocol source: protocol_result.yaml's `protocol_file` (what the engine
     ran); for a prescreen-killed run (no protocol_file: the retired prescreen
     stopped it before a backtest) prescreen_result.yaml's `protocol_version`,
     the protocol the run had resolved -- the 5a gate sits before both, so the
     candidate existed either way. The source is recorded per run.

  2. MEMORY ENTRY -- what campaign_memory.yaml would have held for the run
     had regroup_record been on (it was off for this whole corpus, so there
     is no campaign_memory.yaml to read). build_memory_entry itself cannot run
     here: every run lacks artifacts/idea_status.yaml and grid_evaluation.yaml
     (the grid is later machinery). So the entry is assembled from the SAME
     helpers build_memory_entry uses for the parts the key reads:
       * variants -- campaign_memory._variants_block (single-column shape:
         no artifacts/variants/index.yaml in this corpus, so the one variant
         is named after the run), which measures `symbols` from
         protocol_result.yaml's results (_protocol_shape) and copies
         `forecast_hash` from the trial ledger's "backtest" row
         (_trial_rows/_tested_trial);
       * protocol_ref -- campaign_memory.protocol_ref_of(protocol_file, root);
       * timeframe -- the card's (only the unresolved-protocol fallback).
     Declared deviation (measured): the ledger's backtest rows predate
     E-025's mandatory forecast_hash, so no row in this corpus carries one.
     When a run's backtest row is missing or has no hash, the row is
     BACKFILLED with novelty.forecast_hash_of_config of the run's
     candidate_strategy_config.json -- the function and file
     _record_backtest_trial would have hashed -- and the source is recorded
     (`forecast_hash_source`). A row that DOES carry a hash is used as is.
     A run gets no memory entry (it can never be matched, the safe
     direction, as live) when: no hypothesis_card.yaml / hypothesis_id
     (build_memory_entry requires one), no protocol_result.yaml, no backtest
     results (a prescreen stub), no config to hash, or any helper raises.
     A result row with component_errors.count > 0 makes it a fault entry
     (never matches), mirroring regroup_record.

OLD SIDE (information only)
The retired family-grain layer 2 as its last 5a caller used it
(_route_post_variant_selection before E-036 S2a): the hypothesis card,
backtest_spec.yaml's `config` for the composition fingerprint, every
(instrument, timeframe) the card names (extract_instruments /
extract_timeframes; none named -> None, as evaluate_candidate defaulted),
and the precedence repeat > neighbour > novel across them (the old
multi-instrument rule). The digest is build_exclusion_digest.
scan_run_triples over the corpus, restricted to EARLIER runs (each triple's
run_ids filtered; a triple left empty dropped -- the grouping key is per
run, so this equals a scan of the earlier runs alone). The outcome is
build_exclusion_digest.legacy_family_lookup's. Counted as "old refuse":
`repeat` only -- the one outcome that REFUSEd. `neighbour` ADMITted with a
flag and is reported separately. Layer 1 (KB) is not replayed on either
side: it is advisory in the new gate, and the KB is today's, not the one
each run saw.

CLI:
  python strategy-research/tools/replay_repeat_gate.py [--runs-dir ...] [--root ...]
      [--campaign-state ...] [--out ...]
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

import anti_adjacency_gate as _aag  # tools/ sibling: candidate_key, layer2_digest_check
import build_exclusion_digest as _bed  # tools/ sibling: the retired family digest
import campaign_memory as _cm  # tools/ sibling: the memory entry helpers
import novelty as _nov  # tools/ sibling: THE exact-match key

_HERE = Path(__file__).resolve().parent
_SR = _HERE.parent

DEFAULT_RUNS_DIR = _SR / "runs"
DEFAULT_CAMPAIGN_STATE_PATH = _SR / "campaign_record" / "campaign_state.yaml"
DEFAULT_OUT_PATH = _SR / "engineering" / "roadmap" / "E-036" / "s2b_replay_result.yaml"

SCHEMA_VERSION = 1
_RUN_RE = re.compile(r"^run_(\d+)$")
_OLD_RANK = {"repeat": 2, "neighbour": 1, "novel": 0}

# Candidate-side unkeyable reasons (exhaustive; each run gets exactly one or none).
CAND_NO_CONFIG = "no_candidate_config"
CAND_CONFIG_UNREADABLE = "candidate_config_unreadable"
CAND_NO_PROTOCOL = "no_protocol_recorded"
CAND_PROTOCOL_UNREADABLE = "protocol_unreadable"
CAND_PROTOCOL_NO_SYMBOLS = "protocol_has_no_symbols"


class ReplayError(ValueError):
    """The replay was asked to do something unsafe (e.g. write under the corpus)."""


def _run_sort_key(path: Path):
    m = _RUN_RE.match(path.name)
    return (int(m.group(1)), path.name) if m else (10 ** 9, path.name)


def run_dirs_in_order(runs_dir: Path) -> list:
    """Every runs_dir/run_<digits> directory, in run-number order."""
    return sorted((p for p in Path(runs_dir).iterdir() if p.is_dir() and _RUN_RE.match(p.name)),
                  key=_run_sort_key)


def _read_yaml(path: Path):
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def _read_mapping(path: Path):
    """The parsed mapping, or None when absent / unparseable / not a mapping."""
    if not Path(path).exists():
        return None
    try:
        doc = _read_yaml(path)
    except (OSError, yaml.YAMLError):
        return None
    return doc if isinstance(doc, dict) else None


def _read_card(arts: Path):
    """(card, reason): the parsed hypothesis_card.yaml mapping, else None and
    no_hypothesis_card / hypothesis_card_unreadable (the old digest scan
    skipped such a card too, scan_run_triples' skipped_runs)."""
    path = Path(arts) / "hypothesis_card.yaml"
    if not path.exists():
        return None, "no_hypothesis_card"
    try:
        card = _read_yaml(path)
    except (OSError, yaml.YAMLError) as exc:
        return None, f"hypothesis_card_unreadable: {type(exc).__name__}"
    if not isinstance(card, dict):
        return None, "hypothesis_card_unreadable: not a mapping"
    return card, None


def _read_config(path: Path):
    """(config, reason): the parsed JSON config, else None and a reason."""
    if not path.exists():
        return None, CAND_NO_CONFIG
    try:
        cfg = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return None, f"{CAND_CONFIG_UNREADABLE}: {exc}"
    if not isinstance(cfg, dict):
        return None, f"{CAND_CONFIG_UNREADABLE}: not a JSON object"
    return cfg, None


def _executed_protocol(arts: Path):
    """(protocol_file as recorded, source) -- protocol_result.yaml's
    `protocol_file` (the backtest ran it), else prescreen_result.yaml's
    `protocol_version` (a prescreen-killed run), else (None, None)."""
    pr = _read_mapping(arts / "protocol_result.yaml") or {}
    if pr.get("protocol_file"):
        return str(pr["protocol_file"]), "protocol_result.protocol_file"
    ps = _read_mapping(arts / "prescreen_result.yaml") or {}
    if ps.get("protocol_version"):
        return str(ps["protocol_version"]), "prescreen_result.protocol_version"
    return None, None


def _protocol_ref(protocol_file, root: Path):
    """campaign_memory.protocol_ref_of, with a RELATIVE recorded path (the
    corpus records e.g. 'protocols\\\\baseline_v1.json', written by the
    engine running in strategy-research/) anchored at `root` first, so the
    result never depends on this process's working directory. Absolute
    paths pass through unchanged."""
    if not protocol_file:
        return None
    p = Path(str(protocol_file).replace("\\", "/"))
    return _cm.protocol_ref_of(str(p if p.is_absolute() else Path(root) / p), root)


def _key_dict(key: tuple) -> dict:
    return {"forecast_hash": key[0], "symbols": list(key[1]), "timeframe": key[2],
            "window_set": key[3]}


# ---------------------------------------------------------------------------
# Memory side
# ---------------------------------------------------------------------------

def _has_component_errors(pr: dict) -> bool:
    for r in pr.get("results") or []:
        ce = r.get("component_errors") if isinstance(r, dict) else None
        if isinstance(ce, dict) and isinstance(ce.get("count"), int) and ce["count"] > 0:
            return True
    return False


def memory_entry_for_run(run_dir: Path, run_id: str, *, trial_sharpes, root: Path):
    """(entry, reason, forecast_hash_source): the campaign_memory-shaped entry
    the key reads (run_id, hypothesis_id, legacy, engineering_fault,
    protocol_ref, timeframe, variants), built in memory only, never written.
    entry None + reason when the run cannot have a (matchable) entry."""
    arts = Path(run_dir) / "artifacts"
    card, card_reason = _read_card(arts)
    if card is None:
        return None, card_reason, None
    hyp_id = card.get("hypothesis_id")
    if not isinstance(hyp_id, str) or not hyp_id.strip():
        return None, "no_hypothesis_id", None
    timeframe = card.get("timeframe") if isinstance(card.get("timeframe"), str) else None
    pr = _read_mapping(arts / "protocol_result.yaml")
    if pr is None:
        return None, "no_protocol_result", None
    if not (pr.get("results") or []):
        return None, f"not_backtested ({pr.get('source') or 'no results'})", None
    if _has_component_errors(pr):
        return ({"run_id": run_id, "hypothesis_id": hyp_id, "legacy": False,
                 "engineering_fault": _cm.ENGINEERING_FAULT_COMPONENT_ERROR},
                "engineering_fault", None)

    trials = _cm._trial_rows(run_id, trial_sharpes)
    row = (trials.get(run_id) or {}).get("backtest")
    if row is not None and isinstance(row.get("forecast_hash"), str) and row["forecast_hash"]:
        fh_source = "trial_ledger"
    else:
        cfg, reason = _read_config(arts / "candidate_strategy_config.json")
        if cfg is None:
            return None, f"no_forecast_hash ({reason})", None
        fh_source = ("config_file_backfill (ledger row without forecast_hash)" if row is not None
                     else "config_file_backfill (no ledger row)")
        row = {**(row or {"trial_id": run_id, "source": "backtest"}),
               "forecast_hash": _nov.forecast_hash_of_config(cfg)}
        trials = {**trials, run_id: {**(trials.get(run_id) or {}), "backtest": row}}
    try:
        variants = _cm._variants_block(Path(run_dir), run_id, [run_id], trials)
    except _cm.CampaignMemoryError as exc:
        return None, f"memory_helper_raised: {exc}", None
    entry = {
        "run_id": run_id, "hypothesis_id": hyp_id, "legacy": False, "engineering_fault": None,
        "protocol_ref": _protocol_ref(pr.get("protocol_file"), root),
        "timeframe": timeframe, "variants": variants,
    }
    return entry, None, fh_source


# ---------------------------------------------------------------------------
# Candidate side
# ---------------------------------------------------------------------------

def candidate_for_run(run_dir: Path, *, root: Path):
    """(context, reason): what the 5a gate would read for this run -- the
    config's forecast hash, the protocol ref/symbols/strict spec -- or None
    and the unkeyable reason."""
    arts = Path(run_dir) / "artifacts"
    cfg, reason = _read_config(arts / "candidate_strategy_config.json")
    if cfg is None:
        return None, reason
    protocol_file, source = _executed_protocol(arts)
    if protocol_file is None:
        return None, CAND_NO_PROTOCOL
    protocol_ref = _protocol_ref(protocol_file, root)
    try:
        proto = _nov.load_protocol(root, protocol_ref)
        spec = _nov.protocol_spec(root, protocol_ref, strict=True)
    except _nov.NoveltyError as exc:
        return None, f"{CAND_PROTOCOL_UNREADABLE}: {exc}"
    symbols = proto.get("symbols")
    if not (isinstance(symbols, list) and symbols and all(isinstance(s, str) and s for s in symbols)):
        return None, f"{CAND_PROTOCOL_NO_SYMBOLS}: {protocol_ref}"
    card = _read_mapping(arts / "hypothesis_card.yaml") or {}
    return {"forecast_hash": _nov.forecast_hash_of_config(cfg),
            "protocol_ref": protocol_ref, "protocol_source": source,
            "symbols": sorted(set(symbols)), "spec": spec,
            "card_timeframe": card.get("timeframe")}, None


# ---------------------------------------------------------------------------
# Old side
# ---------------------------------------------------------------------------

def _digest_before(scan: dict, earlier: set) -> dict:
    """The family digest restricted to runs in `earlier` (a triple's run_ids
    filtered, an emptied triple dropped)."""
    fams = {}
    for fam, bucket in (scan.get("families") or {}).items():
        triples = []
        for t in bucket.get("triples") or []:
            rids = [r for r in t.get("run_ids") or [] if r in earlier]
            if rids:
                triples.append({**t, "run_ids": rids})
        if triples:
            fams[fam] = {"confidence": bucket.get("confidence"), "triples": triples}
    return {"families": fams}


def old_outcome_for_run(run_dir: Path, digest: dict) -> dict:
    """The retired layer 2's outcome for this run: legacy_family_lookup over
    every (instrument, timeframe) the card names, repeat > neighbour > novel."""
    arts = Path(run_dir) / "artifacts"
    card, card_reason = _read_card(arts)
    if card is None:
        return {"outcome": "not_evaluable", "reason": card_reason}
    spec = _read_mapping(arts / "backtest_spec.yaml") or {}
    cfg = spec.get("config") if isinstance(spec.get("config"), dict) else None
    instruments = _bed.extract_instruments(card) or [None]
    timeframes = _bed.extract_timeframes(card) or [None]
    best = None
    for instrument in instruments:
        for tf in timeframes:
            res = _bed.legacy_family_lookup(card, instrument, tf, digest, candidate_config=cfg)
            res = {**res, "instrument": instrument, "timeframe": tf}
            if best is None or _OLD_RANK[res["outcome"]] > _OLD_RANK[best["outcome"]]:
                best = res
    best["fingerprint_config"] = "backtest_spec.config" if cfg is not None else None
    return best


# ---------------------------------------------------------------------------
# Replay
# ---------------------------------------------------------------------------

def replay(runs_dir: Path = DEFAULT_RUNS_DIR, *, root: Path = _SR,
           campaign_state_path: Path | None = DEFAULT_CAMPAIGN_STATE_PATH) -> dict:
    """The full replay, returned as a dict (nothing written)."""
    runs_dir, root = Path(runs_dir), Path(root)
    state = _read_mapping(campaign_state_path) if campaign_state_path else None
    trial_sharpes = (state or {}).get("trial_sharpes") or []
    dirs = run_dirs_in_order(runs_dir)
    scan = _bed.scan_run_triples(runs_dir)

    memory = {"runs": {}}  # campaign_memory-shaped, EARLIER runs only at each step
    protocol_warnings: list = []
    rows = []
    earlier: set = set()
    for run_dir in dirs:
        run_id = run_dir.name
        row = {"run_id": run_id}

        # --- new gate: this run as a 5a candidate against earlier memory
        cand, cand_reason = candidate_for_run(run_dir, root=root)
        key = None
        if cand is None:
            row["new"] = {"outcome": "UNKEYED", "reason": cand_reason}
        else:
            specs = _nov.protocol_specs(root, memory, warnings=protocol_warnings)
            specs[_nov.normalize_ref(cand["protocol_ref"])] = cand["spec"]
            key = _aag.candidate_key(cand["forecast_hash"], cand["symbols"], cand["protocol_ref"],
                                     specs, card_timeframe=cand["card_timeframe"])
            index = _nov.match_index(memory, specs, exclude_run_id=run_id)
            res = _aag.layer2_digest_check(key, index)
            row["new"] = {"outcome": "REPEAT" if res["outcome"] == "repeat" else "NOVEL",
                          "matched": [f"{m['run_id']}:{m['variant_id']}" for m in res["matched"]],
                          "key": _key_dict(key), "protocol_ref": cand["protocol_ref"],
                          "protocol_source": cand["protocol_source"]}

        # --- old gate: the family digest of earlier runs
        row["old"] = old_outcome_for_run(run_dir, _digest_before(scan, earlier))

        # --- this run's own memory entry, added AFTER its own check
        entry, mem_reason, fh_source = memory_entry_for_run(run_dir, run_id,
                                                            trial_sharpes=trial_sharpes, root=root)
        mem = {"entry": entry is not None and not entry.get("engineering_fault"),
               "reason": mem_reason, "forecast_hash_source": fh_source}
        if entry is not None:
            memory["runs"][run_id] = entry
            if not entry.get("engineering_fault"):
                own_specs = _nov.protocol_specs(root, {"runs": {run_id: entry}},
                                                warnings=protocol_warnings)
                v = entry["variants"][run_id]
                own_key = _nov.novelty_key(v["forecast_hash"], v.get("symbols"), entry, own_specs)
                mem["key"] = _key_dict(own_key)
                if key is not None:
                    # Self-consistency: the key this run would be FOUND by
                    # later equals the key it was CHECKED with. A difference
                    # is a blind spot of the gate (a true repeat it misses).
                    mem["self_consistent"] = own_key == key
        row["memory"] = mem
        rows.append(row)
        earlier.add(run_id)

    return {"schema_version": SCHEMA_VERSION, "runs": rows,
            "totals": _totals(rows),
            "protocol_warnings": _dedupe(protocol_warnings),
            "corpus": {"runs_dir": _display_path(runs_dir, root), "n_run_dirs": len(dirs),
                       "order": "run number (run_<digits>)"}}


def _display_path(path: Path, root: Path) -> str:
    """`path` relative to root's parent (e.g. strategy-research/runs) when it
    lies under it, else as given -- no machine-specific absolute path in the
    committed result."""
    try:
        return Path(path).resolve().relative_to(Path(root).resolve().parent).as_posix()
    except ValueError:
        return Path(path).as_posix()


def _dedupe(items: list) -> list:
    seen, out = set(), []
    for it in items:
        k = json.dumps(it, sort_keys=True)
        if k not in seen:
            seen.add(k)
            out.append(it)
    return out


def _bucket(reason: str | None) -> str:
    return (reason or "").split(":")[0].split(" (")[0]


def _totals(rows: list) -> dict:
    new_counts = {"REPEAT": 0, "NOVEL": 0, "UNKEYED": 0}
    unkeyed: dict = {}
    old_counts = {"repeat": 0, "neighbour": 0, "novel": 0, "not_evaluable": 0}
    matrix: dict = {}
    mem_reasons: dict = {}
    old_unevaluable: dict = {}
    for r in rows:
        n, o = r["new"]["outcome"], r["old"]["outcome"]
        new_counts[n] += 1
        old_counts[o] += 1
        if n == "UNKEYED":
            b = _bucket(r["new"]["reason"])
            unkeyed[b] = unkeyed.get(b, 0) + 1
        if o == "not_evaluable":
            b = _bucket(r["old"]["reason"])
            old_unevaluable[b] = old_unevaluable.get(b, 0) + 1
        matrix.setdefault(o, {"REPEAT": 0, "NOVEL": 0, "UNKEYED": 0})[n] += 1
        if not r["memory"]["entry"]:
            b = _bucket(r["memory"]["reason"])
            mem_reasons[b] = mem_reasons.get(b, 0) + 1
    self_incons = [r["run_id"] for r in rows if r["memory"].get("self_consistent") is False]
    # Every group of keyed candidates sharing a config hash, whatever their
    # protocol or memory status: the upper bound on what ANY protocol/memory
    # convention could turn into a REPEAT (an exact match needs the same hash).
    by_hash: dict = {}
    for r in rows:
        if r["new"]["outcome"] != "UNKEYED":
            by_hash.setdefault(r["new"]["key"]["forecast_hash"], []).append(
                {"run_id": r["run_id"], "timeframe": r["new"]["key"]["timeframe"],
                 "window_set": r["new"]["key"]["window_set"], "new": r["new"]["outcome"]})
    collisions = [{"forecast_hash": h, "runs": v} for h, v in by_hash.items() if len(v) > 1]
    return {
        "runs": len(rows),
        "variants": len(rows),  # one variant per run in this corpus (no variants/index.yaml)
        "new": {**new_counts, "keyed": new_counts["REPEAT"] + new_counts["NOVEL"],
                "unkeyed_by_reason": dict(sorted(unkeyed.items()))},
        "old": {**old_counts, "refuse (repeat)": old_counts["repeat"],
                "admit (neighbour + novel)": old_counts["neighbour"] + old_counts["novel"],
                "not_evaluable_by_reason": dict(sorted(old_unevaluable.items()))},
        "agreement_old_x_new": {k: matrix[k] for k in ("repeat", "neighbour", "novel",
                                                       "not_evaluable") if k in matrix},
        "memory_entries": sum(1 for r in rows if r["memory"]["entry"]),
        "no_memory_entry_by_reason": dict(sorted(mem_reasons.items())),
        "self_inconsistent_runs": self_incons,
        "distinct_config_hashes": len(by_hash),
        "config_hash_collisions": collisions,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    parser.add_argument("--root", type=Path, default=_SR,
                        help="strategy-research/ (protocol refs are relative to it)")
    parser.add_argument("--campaign-state", type=Path, default=DEFAULT_CAMPAIGN_STATE_PATH)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT_PATH)
    args = parser.parse_args(argv)
    out = args.out.resolve()
    runs = args.runs_dir.resolve()
    if out == runs or runs in out.parents:
        raise ReplayError(f"--out {args.out} is under --runs-dir {args.runs_dir}: the replay "
                          f"never writes into the corpus")
    result = replay(args.runs_dir, root=args.root, campaign_state_path=args.campaign_state)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        yaml.safe_dump(result, f, sort_keys=False, allow_unicode=True)
    t = result["totals"]
    print(f"replay written to {out}")
    print(f"  runs={t['runs']} new: REPEAT={t['new']['REPEAT']} NOVEL={t['new']['NOVEL']} "
          f"UNKEYED={t['new']['UNKEYED']} | old: repeat={t['old']['repeat']} "
          f"neighbour={t['old']['neighbour']} novel={t['old']['novel']} "
          f"not_evaluable={t['old']['not_evaluable']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
