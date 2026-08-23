"""E-032 S1 -- measurements backing s1_idea_generation.md.

Read-only. Never touches local_data/holdout_sealed/. Never runs a campaign,
backtest, or writes run_campaign.py. Re-runnable any time from
strategy-research/ (relative paths assume that cwd, matching every other
E-0xx artifact script in this repo).

Produces, on stdout, the exact counts cited in s1_idea_generation.md:
  1. required_inputs for the three generating stages, read directly from
     workflow/stages.yaml -- proves campaign_state.yaml and the near-miss
     scoreboard are NOT in scope for hypothesis_generation / innovation_expansion.
  2. campaign_state.yaml's exclusion-context fields: failed_families,
     recent_parameter_dimensions_by_family, instruments_tried, timeframes_tried,
     components_built -- with counts and denominators.
  3. The staleness cross-check: for every run directory with a hypothesis_card.yaml
     whose thesis/rationale/signal_concept mentions "funding", what `timeframe`
     value was actually used -- to show whether "4h" ever appears for THIS
     family, independent of the global (family-blind) timeframes_tried list.
  4. Whether run_claude_worker's tool grant (ClaudeAgentOptions) permits any
     network/browse tool today -- read directly from run_phase1_research.py.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]  # strategy-research/
assert ROOT.name == "strategy-research", f"unexpected root: {ROOT}"


def section(title: str) -> None:
    print(f"\n{'=' * 70}\n{title}\n{'=' * 70}")


def measure_stage_inputs() -> None:
    section("1. required_inputs per generating stage (workflow/stages.yaml)")
    stages = yaml.safe_load((ROOT / "workflow" / "stages.yaml").read_text(encoding="utf-8"))
    for name in ("hypothesis_generation", "innovation_expansion", "refinement_planner", "campaign_review"):
        entry = stages["stages"][name]
        req = entry.get("required_inputs", [])
        print(f"  {name}:")
        print(f"    skill: {entry.get('skill')}")
        print(f"    required_inputs ({len(req)}): {req}")
        has_campaign_state = any("campaign_state.yaml" in r for r in req)
        has_scoreboard = any("near_miss_scoreboard" in r for r in req)
        print(f"    includes campaign_state.yaml: {has_campaign_state}")
        print(f"    includes near_miss_scoreboard: {has_scoreboard}")


def measure_campaign_state() -> None:
    section("2. campaign_state.yaml exclusion-context fields")
    cs = yaml.safe_load((ROOT / "campaign_record" / "campaign_state.yaml").read_text(encoding="utf-8"))
    ff = cs.get("failed_families", [])
    rpd = cs.get("recent_parameter_dimensions_by_family", {})
    it = cs.get("instruments_tried", [])
    tt = cs.get("timeframes_tried", [])
    cb = cs.get("components_built", [])
    print(f"  failed_families: {len(ff)} entries (denominator: this list)")
    for f in ff:
        print(f"    - {f if isinstance(f, str) else f.get('name')}")
    print(f"  recent_parameter_dimensions_by_family: {len(rpd)} families tracked, "
          f"{sum(1 for v in rpd.values() if v)} with a non-empty dimension list")
    print(f"  instruments_tried: {len(it)} -> {it}")
    print(f"  timeframes_tried: {len(tt)} -> {tt}")
    print(f"  components_built: {len(cb)} (empty list means zero, denominator: field itself)")


def measure_funding_family_timeframes() -> None:
    section("3. Staleness cross-check: timeframe actually used, PER FAMILY")
    runs_dir = ROOT / "runs"
    run_dirs = sorted(d for d in runs_dir.iterdir() if d.is_dir() and d.name.startswith("run_"))
    print(f"  run directories scanned: {len(run_dirs)}")

    families = {
        "funding": re.compile(r"funding", re.IGNORECASE),
        "keltner": re.compile(r"keltner", re.IGNORECASE),
    }
    by_family_timeframe: dict[str, set[str]] = {k: set() for k in families}
    by_family_runs: dict[str, list[str]] = {k: [] for k in families}

    for d in run_dirs:
        card = d / "artifacts" / "hypothesis_card.yaml"
        if not card.exists():
            continue
        text = card.read_text(encoding="utf-8", errors="replace")
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError:
            data = None
        tf = None
        if isinstance(data, dict):
            tf = data.get("timeframe")
        if tf is None:
            m = re.search(r'^timeframe:\s*"?([^\s"]+)"?', text, re.MULTILINE)
            tf = m.group(1) if m else "unparsed"
        for fam, pattern in families.items():
            if pattern.search(text):
                by_family_timeframe[fam].add(str(tf))
                by_family_runs[fam].append(f"{d.name}:{tf}")

    for fam in families:
        print(f"  family~='{fam}': timeframes actually seen = {sorted(by_family_timeframe[fam])}")
        print(f"    runs: {by_family_runs[fam]}")

    cs = yaml.safe_load((ROOT / "campaign_record" / "campaign_state.yaml").read_text(encoding="utf-8"))
    tt = set(cs.get("timeframes_tried", []))
    print(f"\n  campaign_state.yaml timeframes_tried (family-blind): {sorted(tt)}")
    funding_tf = by_family_timeframe["funding"]
    print(f"  '4h' in global timeframes_tried: {'4h' in tt}")
    print(f"  '4h' ever used by a funding-family run: {'4h' in funding_tf}")
    if "4h" in tt and "4h" not in funding_tf:
        print("  ==> CONFIRMED TRAP: a gate keyed on the global list alone would refuse")
        print("      a funding-family 4h proposal even though this (family, timeframe)")
        print("      pair has zero prior runs -- the '4h' entry in timeframes_tried")
        print("      comes entirely from the unrelated keltner family.")


def measure_tool_grant() -> None:
    section("4. Tool grant for stage agents (workflow/run_phase1_research.py)")
    src = (ROOT / "workflow" / "run_phase1_research.py").read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r"ClaudeAgentOptions\(([^)]*)\)", src):
        print(f"  ClaudeAgentOptions({m.group(1)})")
    if "allowed_tools=[]" in src:
        print("  ==> allowed_tools=[] confirmed: stage agents have ZERO tool access")
        print("      (no WebSearch, no WebFetch, no MCP, no filesystem beyond the")
        print("      hand-assembled context_blocks) -- closed-book completion only.")


if __name__ == "__main__":
    measure_stage_inputs()
    measure_campaign_state()
    measure_funding_family_timeframes()
    measure_tool_grant()
