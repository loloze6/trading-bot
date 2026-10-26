"""Read-only: run the campaign's launch flag pre-flight (run_campaign._flag_preflight, the check
that halts a launch with `flag_misconfiguration`) on this checkout's config/campaign_config.yaml,
and print every flag value the daily-breadth loop depends on.

Usage, from strategy-research/:  ../venv/Scripts/python.exe engineering/flagset_daily_breadth/preflight_check.py
Writes nothing (the dry run is a separate command).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "workflow"))
sys.path.insert(0, str(ROOT / "tools"))

import run_campaign as rc  # noqa: E402

WANT = {
    "variant_loop": True, "config_direct_authoring": True, "profit_bars_file": True,
    "profit_bars_every_backtest": True, "profit_bars_v2": True, "decide_next": True,
    "operator_approval": True, "folds": True, "brief_criteria": True, "analyst": True,
    "claim_tests": True,
    "regroup_record": True, "grid_evaluation": True,
    "verdict_routing_retired": True, "nearest_build": True, "deviation_gate": False,
    "config_replay_gate": True, "exact_config_1b": True, "composition_runs": True,
}


def main() -> None:
    values, refusal = rc._flag_preflight()
    print(f"flag pre-flight refusal: {refusal!r}  ({'ACCEPTED' if refusal is None else 'REFUSED'})")
    bad = 0
    for name, want in WANT.items():
        got = values.get(name)
        ok = got is want
        bad += not ok
        print(f"  {name:28s} {got!s:6s} expected {want!s:6s} {'ok' if ok else 'MISMATCH'}")
    print(f"mismatches: {bad}")
    if refusal is not None or bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
