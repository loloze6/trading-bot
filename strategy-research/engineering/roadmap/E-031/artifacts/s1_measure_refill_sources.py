"""E-031 S1 measurement script.

Read-only. Recomputes every count quoted in s1_refill_sources.md directly
from the primary YAML/config files, so the numbers in the report are
reproducible rather than hand-copied from a one-off grep.

Usage (from repo root):
    python strategy-research/engineering/roadmap/E-031/artifacts/s1_measure_refill_sources.py

Touches no files. Does not open local_data/holdout_sealed/ (not referenced
at all). Does not invoke run_campaign.py or any campaign/backtest code.
"""

import re
import sys
from pathlib import Path

import yaml

SR = Path(__file__).resolve().parents[4]  # .../trading-bot/strategy-research
ROOT = SR.parent  # .../trading-bot


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def section(title: str):
    print(f"\n=== {title} ===")


def main() -> int:
    # ------------------------------------------------------------------
    # 1. campaign_state.yaml
    # ------------------------------------------------------------------
    cs_path = SR / "campaign_record" / "campaign_state.yaml"
    cs = load_yaml(cs_path)

    section(f"campaign_state.yaml ({cs_path.relative_to(ROOT)})")

    failed_families = cs.get("failed_families", [])
    print(f"failed_families: {len(failed_families)} entries (denominator: this list)")

    altitude_history = cs.get("altitude_history", [])
    escalate = [a for a in altitude_history if a.get("outcome") == "escalate"]
    print(
        f"altitude_history: {len(altitude_history)} entries total; "
        f"{len(escalate)} with outcome=escalate (denominator: altitude_history list)"
    )
    for e in escalate:
        print(
            f"    - run={e.get('run')} dimension={e.get('dimension')!r} "
            f"family={e.get('family')!r}"
        )

    rpd = cs.get("recent_parameter_dimensions_by_family", {})
    nonempty = {k: v for k, v in rpd.items() if v}
    print(
        f"recent_parameter_dimensions_by_family: {len(rpd)} families tracked, "
        f"{len(nonempty)} with a non-empty dimension list (denominator: this dict)"
    )
    for k, v in rpd.items():
        print(f"    - {k}: {v!r}")

    instruments = cs.get("instruments_tried", [])
    print(f"instruments_tried: {len(instruments)} -> {instruments}")

    timeframes = cs.get("timeframes_tried", [])
    print(f"timeframes_tried: {len(timeframes)} -> {timeframes}")

    # ------------------------------------------------------------------
    # 2. coin_universe.yaml -- cross-check instruments_tried staleness
    # ------------------------------------------------------------------
    cu_path = SR / "config" / "coin_universe.yaml"
    cu_text = cu_path.read_text(encoding="utf-8")
    n_symbols = len(re.findall(r"^\s*- symbol:", cu_text, flags=re.M))
    section(f"coin_universe.yaml ({cu_path.relative_to(ROOT)})")
    print(
        f"symbol entries: {n_symbols} (cross-check only -- instruments_tried above "
        f"is {len(instruments)}, and campaign_queue.yaml's XS_momentum note ratifies "
        f"a 19-pair Kraken universe separately from this field)"
    )

    # ------------------------------------------------------------------
    # 3. feed_wishlist.yaml
    # ------------------------------------------------------------------
    fw_path = SR / "campaign_record" / "feed_wishlist.yaml"
    fw = load_yaml(fw_path)
    wishlist = fw.get("wishlist", [])
    section(f"feed_wishlist.yaml ({fw_path.relative_to(ROOT)})")
    print(
        f"wishlist entries: {len(wishlist)} (denominator: this list; the file's own "
        f"'Example entry (template)' block is a '#' comment, not live YAML, so it is "
        f"correctly excluded by safe_load)"
    )
    for w in wishlist:
        print(
            f"    - feed_name={w.get('feed_name')} "
            f"hypotheses_blocked={len(w.get('hypotheses_blocked', []))}"
        )

    # Cross-check against available_feeds.yaml
    af_path = SR / "config" / "available_feeds.yaml"
    af = load_yaml(af_path)
    unavailable = {u["evidence_type"] for u in af.get("unavailable", [])}
    section(f"available_feeds.yaml ({af_path.relative_to(ROOT)}) cross-check")
    for w in wishlist:
        et = w.get("evidence_type")
        status = (
            "UNAVAILABLE (still routed to feed_wishlist)"
            if et in unavailable
            else "AVAILABLE"
        )
        print(f"    - {w.get('feed_name')} / evidence_type={et}: {status}")

    # ------------------------------------------------------------------
    # 4. campaign_knowledge_base.yaml -- reactivation clauses
    # ------------------------------------------------------------------
    kb_path = SR / "campaign_record" / "campaign_knowledge_base.yaml"
    kb = load_yaml(kb_path)
    findings = kb.get("findings", [])
    meta_findings = kb.get("meta_findings", [])
    section(f"campaign_knowledge_base.yaml ({kb_path.relative_to(ROOT)})")
    print(
        f"findings: {len(findings)} (hypothesis-outcome records -- this is the "
        f"denominator for reactivation_condition below)"
    )
    print(
        f"meta_findings: {len(meta_findings)} (process/methodology records -- "
        f"a distinct category, no reactivation_condition field by design)"
    )
    print(
        f"exhausted_mechanisms index: {len(kb.get('exhausted_mechanisms', []))} "
        f"(cross-reference index into findings above, not additional records)"
    )

    with_reactivation = [f for f in findings if f.get("reactivation_condition")]
    print(
        f"findings carrying a non-null reactivation_condition: {len(with_reactivation)}"
    )
    for f in with_reactivation:
        print(
            f"    - id={f.get('id')} hypothesis_id={f.get('hypothesis_id')} "
            f"exhausted={f.get('exhausted')}"
        )

    # ------------------------------------------------------------------
    # 5. detector_wishlist.yaml
    # ------------------------------------------------------------------
    dw_path = SR / "config" / "detector_wishlist.yaml"
    dw = load_yaml(dw_path)
    candidates = dw.get("candidates", [])
    section(f"detector_wishlist.yaml ({dw_path.relative_to(ROOT)})")
    print(f"candidates: {len(candidates)}")
    for c in candidates:
        tc = c.get("trigger_condition", {})
        print(
            f"    - family={c.get('family')} status={tc.get('status')} "
            f"last_evaluated_at={tc.get('last_evaluated_at')}"
        )

    # Is the KB newer than the last predicate evaluation? (staleness signal)
    kb_mtime = kb_path.stat().st_mtime
    dw_mtime = dw_path.stat().st_mtime
    print(
        f"campaign_knowledge_base.yaml mtime={kb_mtime:.0f}  "
        f"detector_wishlist.yaml mtime={dw_mtime:.0f}  "
        f"(KB modified after wishlist file: {kb_mtime > dw_mtime})"
    )

    # ------------------------------------------------------------------
    # 6. register_hypothesis / evaluate_and_persist_wishlist_predicate callers
    # ------------------------------------------------------------------
    section(
        "call-site grep (register_hypothesis / evaluate_and_persist_wishlist_predicate)"
    )
    self_path = Path(__file__).resolve()
    for fn in ("register_hypothesis(", "evaluate_and_persist_wishlist_predicate("):
        hits = []
        for py in SR.rglob("*.py"):
            if py.resolve() == self_path:
                continue  # exclude this measurement script itself
            try:
                text = py.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            for i, line in enumerate(text.splitlines(), start=1):
                if fn in line:
                    hits.append(f"{py.relative_to(ROOT)}:{i}")
        print(f"{fn} -- {len(hits)} call site(s):")
        for h in hits:
            print(f"    - {h}")

    # ------------------------------------------------------------------
    # 7. refinement_notes.yaml presence across runs/
    # ------------------------------------------------------------------
    runs_dir = SR / "runs"
    run_dirs = [
        p for p in runs_dir.iterdir() if p.is_dir() and p.name.startswith("run_")
    ]
    with_notes = [
        p for p in run_dirs if (p / "artifacts" / "refinement_notes.yaml").exists()
    ]
    section(f"refinement_notes.yaml presence ({runs_dir.relative_to(ROOT)})")
    print(f"run directories: {len(run_dirs)} (denominator)")
    print(
        f"with refinement_notes.yaml: {len(with_notes)} -> "
        f"{[p.name for p in with_notes]}"
    )

    # ------------------------------------------------------------------
    # 8. campaign_queue.yaml -- _select_entry schedulability today
    # ------------------------------------------------------------------
    cq_path = SR / "config" / "campaign_queue.yaml"
    cq = load_yaml(cq_path)
    entries = cq.get("queue", [])
    section(f"campaign_queue.yaml ({cq_path.relative_to(ROOT)})")
    print(f"entries: {len(entries)} (denominator: this queue)")
    from collections import Counter

    statuses = Counter(e.get("status") for e in entries)
    print(f"status breakdown: {dict(statuses)}")
    schedulable = [e for e in entries if e.get("status") in ("ready", "in_progress")]
    print(
        f"schedulable today (_select_entry semantics: status in "
        f"{{'ready','in_progress'}}): {len(schedulable)}"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
