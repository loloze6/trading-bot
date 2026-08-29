"""E-034 S1 measurement script.

Scans the run corpus for expanded_hypothesis_card.yaml files and characterizes:
  - how many runs/files carry the artifact, and under what paths
  - total variant count and per-run max
  - variant item shapes (bare string vs dict, and which keys dicts carry)
  - which runs' chosen variant (if any) is identifiable from backtest_spec.yaml /
    validation_decision.yaml / decision.yaml
  - occurrences of `variants_not_pursued` anywhere in the run corpus

Run from strategy-research/:
    ../venv/Scripts/python engineering/roadmap/E-034/artifacts/s1_measure_variants.py

Read-only. Does not touch local_data/holdout_sealed/ (never globbed).
"""

from __future__ import annotations

import glob
import json
import re
import sys
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[4]  # strategy-research/
RUNS = ROOT / "runs"


def load_yaml(path: Path):
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        return {"__PARSE_ERROR__": str(e)}


def main():
    # --- 1. locate expanded_hypothesis_card.yaml under artifacts/ only
    #        (attempt_1_blocked/ copies are a separate, superseded attempt of
    #        the same run and are reported but not double-counted).
    artifact_files = sorted((RUNS).glob("*/artifacts/expanded_hypothesis_card.yaml"))
    blocked_files = sorted((RUNS).glob("*/attempt_*_blocked/expanded_hypothesis_card.yaml"))

    print(
        f"expanded_hypothesis_card.yaml under */artifacts/: {len(artifact_files)} files "
        f"(denominator: {len(list(RUNS.glob('run_*')))} run dirs under runs/)"
    )
    print(
        f"expanded_hypothesis_card.yaml under */attempt_*_blocked/ (superseded attempts, "
        f"not counted in the total below): {len(blocked_files)} files -> "
        f"{[str(p.relative_to(RUNS)) for p in blocked_files]}"
    )

    total_variants = 0
    max_in_one_run = 0
    max_run = None
    shapes = {}
    dict_keys_seen = set()
    per_run_rows = []
    parse_errors = []
    no_key = []

    for f in artifact_files:
        run_dir = f.parents[1]
        run_id = run_dir.name
        d = load_yaml(f)
        if not d or "__PARSE_ERROR__" in d:
            parse_errors.append((run_id, d.get("__PARSE_ERROR__") if d else "empty file"))
            continue
        variants = d.get("expanded_variants")
        if variants is None:
            no_key.append(run_id)
            continue
        n = len(variants)
        total_variants += n
        if n > max_in_one_run:
            max_in_one_run = n
            max_run = run_id
        for v in variants:
            t = type(v).__name__
            shapes[t] = shapes.get(t, 0) + 1
            if isinstance(v, dict):
                dict_keys_seen.update(v.keys())
        per_run_rows.append((run_id, n))

    print()
    print(
        f"MEASURED: total expanded_variants across {len(per_run_rows)} successfully-parsed "
        f"runs (denominator: {len(artifact_files)} artifact files, "
        f"{len(parse_errors)} parse errors, {len(no_key)} missing the key): {total_variants}"
    )
    print(f"MEASURED: max variants in a single run: {max_in_one_run} ({max_run})")
    print(
        f"MEASURED: variant item shapes (type name -> count of items, "
        f"denominator {total_variants} total items): {shapes}"
    )
    print(f"MEASURED: keys seen across all dict-shaped variants (union, informational): {sorted(dict_keys_seen)}")
    if parse_errors:
        print(f"PARSE ERRORS: {parse_errors}")
    if no_key:
        print(f"MISSING expanded_variants KEY: {no_key}")

    # --- 2. variants_not_pursued grep across the whole runs/ corpus
    hits = []
    for p in RUNS.rglob("*"):
        if p.is_file() and p.suffix in (".yaml", ".yml", ".json", ".md"):
            try:
                text = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if "variants_not_pursued" in text:
                hits.append(str(p.relative_to(RUNS)))
    print()
    print(
        f"MEASURED: files under runs/ containing the literal string "
        f"'variants_not_pursued' (denominator: all .yaml/.yml/.json/.md files under runs/): "
        f"{len(hits)} -> {hits}"
    )

    # --- 3. run_019 spot check: is the chosen variant named anywhere?
    print()
    print("=== run_019 spot check ===")
    r19 = RUNS / "run_019" / "artifacts"
    ehc = load_yaml(r19 / "expanded_hypothesis_card.yaml")
    print(f"run_019 expanded_variants ({len(ehc.get('expanded_variants', []))} items):")
    for v in ehc.get("expanded_variants", []):
        print(f"  - {v!r}")
    vd = load_yaml(r19 / "validation_decision.yaml")
    print(f"run_019 validation_decision.yaml keys: {sorted(vd.keys()) if isinstance(vd, dict) else vd}")
    bs_path = r19 / "backtest_spec.yaml"
    if not bs_path.exists():
        bs_path = r19 / "backtest_spec.yaml"
    bs = load_yaml(r19 / "backtest_spec.yaml") if (r19 / "backtest_spec.yaml").exists() else None
    print(f"run_019 backtest_spec.yaml present: {bs is not None}")
    if bs:
        print(f"run_019 backtest_spec.yaml keys: {sorted(bs.keys())}")
        print(f"run_019 backtest_spec.yaml config_rationale: {bs.get('config_rationale')}")

    # --- 4. cross-run: which runs have BOTH >1 variant AND a backtest_spec.yaml,
    #        and whether hypothesis_claim/config_choice text in config_rationale
    #        names a specific variant value (heuristic substring match only,
    #        reported for manual eyeballing, not asserted as proof).
    print()
    print("=== cross-run: multi-variant runs with a produced backtest_spec.yaml ===")
    for run_id, n in per_run_rows:
        if n <= 1:
            continue
        spec_path = RUNS / run_id / "artifacts" / "backtest_spec.yaml"
        if not spec_path.exists():
            continue
        print(
            f"{run_id}: {n} variants, backtest_spec.yaml exists -> inspect manually "
            f"(listed for S1 report, not auto-verdicted)"
        )


if __name__ == "__main__":
    main()
