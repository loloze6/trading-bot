"""
D-185: key the trial ledger rows written before orchestrator.dsr_same_structure
with their (structure_hash, timeframe), from the config their run saved and the
run's protocol timeframe.

Dry run by default: prints COUNTS only (rows keyed, rows left unkeyed and why).
It reads the ledger, the saved configs and each run's protocol for its
`timeframe` key, and prints nothing of any of them.

    python tools/backfill_structure_hash.py                 # dry run
    python tools/backfill_structure_hash.py --write         # append to the overlay

--write appends to the overlay campaign_record/trial_structure_key_overlay.yaml
(structure_key.py documents its shape). It NEVER edits the ledger: the overlay
is append-only and deterministic, an entry already present and equal is skipped,
an entry already present and different aborts the write, and the file is
replaced atomically (temp file + os.replace). The DSR reads the overlay beside
the ledger rows under orchestrator.dsr_same_structure.

Where a row's config comes from:
  trial_id "run_NNN:<variant>"  -> runs/run_NNN/artifacts/variants/<variant>/strategy_config.json
  trial_id "run_NNN"            -> runs/run_NNN/artifacts/candidate_strategy_config.json
A row with no saved config stays unkeyed. So does a row whose saved config does
not hash (the forecast_hash rule) to the row's own forecast_hash -- the file is
then not what the row tested -- and a row whose run has no readable protocol
timeframe. A legacy row with no forecast_hash cannot be checked that way and is
keyed from its saved config, counted apart ("keyed_unverified").

Why none of this can leak: the key is a function of a saved config and a bar
size, both fixed before any bar of the run was read.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path

import yaml

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import structure_key as sk  # noqa: E402  (tools/ sibling)

ROOT = _HERE.parent  # strategy-research/
LEDGER_REL = Path("campaign_record") / "campaign_state.yaml"
OVERLAY_REL = Path("campaign_record") / "trial_structure_key_overlay.yaml"


def _forecast_hash(text: str) -> str:
    """The _compute_forecast_hash rule (run_phase1_research.py), on the file text."""
    return hashlib.sha256(json.dumps(json.loads(text), sort_keys=True).encode("utf-8")).hexdigest()


def _config_ref(trial_id: str) -> tuple:
    """(run_id, config path relative to the root) of a trial id, or (None, None)
    when it is not run_NNN or run_NNN:<variant>."""
    if not isinstance(trial_id, str) or not trial_id:
        return None, None
    run_id, _, variant = trial_id.partition(":")
    if not run_id or "/" in run_id or "\\" in run_id or ".." in run_id:
        return None, None
    if variant:
        if "/" in variant or "\\" in variant or ".." in variant:
            return None, None
        return run_id, Path("runs") / run_id / "artifacts" / "variants" / variant / "strategy_config.json"
    return run_id, Path("runs") / run_id / "artifacts" / "candidate_strategy_config.json"


def plan(root: Path, rows: list, existing: dict) -> dict:
    """What a write would do. Returns {"entries": [new overlay entries, sorted],
    "counts": {...}}; counts: rows, already_keyed (a native key), already_in_overlay,
    keyed (entries to add), keyed_unverified (the part of keyed with no forecast_hash to
    check), and unkeyed_<reason> for each reason a row stays unkeyed."""
    counts = {"rows": 0, "already_keyed": 0, "already_in_overlay": 0, "keyed": 0,
              "keyed_unverified": 0}
    new_entries = {}

    def _unkeyed(reason):
        counts[f"unkeyed_{reason}"] = counts.get(f"unkeyed_{reason}", 0) + 1

    tf_cache: dict = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        counts["rows"] += 1
        if row.get("structure_hash") is not None and row.get("timeframe") is not None:
            counts["already_keyed"] += 1
            continue
        key = (row.get("trial_id"), row.get("source"))
        if key in existing:
            counts["already_in_overlay"] += 1
            continue
        run_id, rel = _config_ref(row.get("trial_id"))
        if rel is None or not (isinstance(row.get("source"), str) and row["source"]):
            _unkeyed("no_run_for_trial_id" if rel is None else "no_source")
            continue
        cfg_path = root / rel
        if not cfg_path.is_file():
            _unkeyed("no_saved_config")
            continue
        try:
            text = cfg_path.read_text(encoding="utf-8")
            structure_hash = sk.compute_structure_hash(json.loads(text))
            fhash = _forecast_hash(text)
        except Exception:  # noqa: BLE001 -- an unparseable config leaves the row unkeyed
            _unkeyed("config_unreadable")
            continue
        recorded = row.get("forecast_hash")
        if recorded is not None and recorded != fhash:
            _unkeyed("config_does_not_match_forecast_hash")
            continue
        if run_id not in tf_cache:
            tf_cache[run_id] = sk.run_protocol_timeframe(root, run_id)
        timeframe = tf_cache[run_id]
        if timeframe is None:
            _unkeyed("no_protocol_timeframe")
            continue
        new_entries[key] = {
            "trial_id": row["trial_id"], "source": row["source"],
            "structure_hash": structure_hash, "timeframe": timeframe,
            "config_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
            "config_ref": rel.as_posix(),
        }
        counts["keyed"] += 1
        if recorded is None:
            counts["keyed_unverified"] += 1
    return {"entries": [new_entries[k] for k in sorted(new_entries, key=lambda k: (str(k[0]), str(k[1])))],
            "counts": counts}


def _atomic_write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def run(root: Path, write: bool = False) -> dict:
    """Plan the backfill under `root` (the strategy-research directory); with
    write=True append the new entries to the overlay. Returns the plan."""
    root = Path(root)
    ledger_path, overlay_path = root / LEDGER_REL, root / OVERLAY_REL
    state = yaml.safe_load(ledger_path.read_text(encoding="utf-8")) or {}
    rows = state.get("trial_sharpes") or []
    existing_doc = (yaml.safe_load(overlay_path.read_text(encoding="utf-8"))
                    if overlay_path.exists() else None)
    existing = sk.validate_structure_overlay(existing_doc)  # a malformed overlay aborts here
    result = plan(root, rows, existing)
    if write and result["entries"]:
        merged = list((existing_doc or {}).get("entries") or []) + result["entries"]
        sk.validate_structure_overlay({"entries": merged})  # the whole file must stay valid
        _atomic_write(overlay_path, {"entries": merged})
    result["written"] = bool(write and result["entries"])
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--write", action="store_true",
                    help="append the keyed rows to the overlay (default: dry run, counts only)")
    ap.add_argument("--root", default=str(ROOT),
                    help="the strategy-research directory (default: this tool's)")
    args = ap.parse_args(argv)
    result = run(Path(args.root), write=args.write)
    counts = result["counts"]
    print(f"backfill_structure_hash ({'WRITE' if args.write else 'dry run'}): "
          + ", ".join(f"{k}={v}" for k, v in counts.items()))
    if args.write:
        print(f"overlay: {len(result['entries'])} entr{'y' if len(result['entries']) == 1 else 'ies'} "
              f"appended to {OVERLAY_REL.as_posix()}")
    else:
        print(f"dry run: nothing written; {counts['keyed']} row(s) would be keyed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
