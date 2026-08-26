"""
E-033 S1 measurement script — pre-backtest stage characterization.

Reads the 59-run corpus under strategy-research/runs/ plus
campaign_record/campaign_state.yaml and prints MEASURED counts used in
s1_stage_characterization.md. Every count states its denominator. No
network, no LLM, no writes to the run corpus. Read-only.

Run from strategy-research/:
    python engineering/roadmap/E-033/artifacts/s1_measure_pre_backtest_stages.py
"""
import json
from pathlib import Path
from collections import Counter

import yaml

ROOT = Path(__file__).resolve().parents[4]  # .../strategy-research
RUNS = ROOT / "runs"
CAMPAIGN_STATE = ROOT / "campaign_record" / "campaign_state.yaml"


def load_yaml(p: Path):
    if not p.exists():
        return None
    try:
        with open(p, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        return {"__error__": str(e)}


def main():
    run_dirs = sorted([d for d in RUNS.iterdir() if d.is_dir() and d.name.startswith("run_")])
    n_runs = len(run_dirs)
    print(f"=== Corpus size: {n_runs} run directories under runs/ ===\n")

    # ---- Stage 1: hypothesis_generation ----
    n_hyp_card = sum(1 for d in run_dirs if (d / "artifacts" / "hypothesis_card.yaml").exists())
    print(f"[hypothesis_generation] hypothesis_card.yaml present: {n_hyp_card}/{n_runs}")

    # ---- Stage 2: innovation_expansion ----
    variant_counts = []
    diversity_axes = Counter()
    for d in run_dirs:
        card = load_yaml(d / "artifacts" / "expanded_hypothesis_card.yaml")
        if not card or "__error__" in card:
            continue
        variants = card.get("expanded_variants")
        if variants is None:
            continue
        variant_counts.append((d.name, len(variants)))
        for v in variants:
            axis = v.get("diversity_axis") if isinstance(v, dict) else None
            if axis:
                diversity_axes[axis] += 1

    n_expansion_cards = len(variant_counts)
    total_variants = sum(c for _, c in variant_counts)
    print(f"\n[innovation_expansion] expanded_hypothesis_card.yaml with expanded_variants: "
          f"{n_expansion_cards}/{n_runs}")
    print(f"  total variants across those {n_expansion_cards} runs: {total_variants}")
    if variant_counts:
        max_run, max_n = max(variant_counts, key=lambda t: t[1])
        print(f"  max variants in one run: {max_n} ({max_run})")
        print(f"  min variants in one run: {min(c for _, c in variant_counts)}")
        print(f"  mean variants per card: {total_variants / n_expansion_cards:.2f}")
    print(f"  diversity_axis tag distribution (of {sum(diversity_axes.values())} tagged variants): "
          f"{dict(diversity_axes)}")

    # ---- Stage 3: validation ----
    val_statuses = Counter()
    val_runs_with_variants_and_status = []
    for d in run_dirs:
        dec = load_yaml(d / "artifacts" / "validation_decision.yaml")
        if not dec or "__error__" in dec:
            continue
        status = dec.get("status") or dec.get("family_status")
        if status is None:
            status = "<missing-status-key>"
        status = str(status).strip().lower()
        val_statuses[status] += 1

    n_val_decisions = sum(val_statuses.values())
    print(f"\n[validation] validation_decision.yaml with a readable status: {n_val_decisions}/{n_runs}")
    for status, n in val_statuses.most_common():
        print(f"  {status}: {n}")

    # ---- refinement_planner invocations ----
    n_refinement_notes = sum(1 for d in run_dirs if (d / "artifacts" / "refinement_notes.yaml").exists())
    print(f"\n[refinement_planner] refinement_notes.yaml present: {n_refinement_notes}/{n_runs}")
    for d in run_dirs:
        rn = d / "artifacts" / "refinement_notes.yaml"
        if rn.exists():
            notes = load_yaml(rn)
            impl_allowed = None
            if notes and "__error__" not in notes:
                impl_allowed = notes.get("decision", {}).get("implementation_allowed")
            print(f"  {d.name}: implementation_allowed={impl_allowed}")

    # counters.refinements_used from pipeline_state.yaml, where present
    refinements_used_hist = Counter()
    for d in run_dirs:
        st = load_yaml(d / "pipeline_state.yaml")
        if st and "__error__" not in st:
            ru = st.get("counters", {}).get("refinements_used")
            if ru is not None:
                refinements_used_hist[ru] += 1
    n_pipeline_states = sum(refinements_used_hist.values())
    print(f"\n  pipeline_state.yaml with a counters.refinements_used field: {n_pipeline_states}/{n_runs}")
    print(f"  distribution of final refinements_used: {dict(sorted(refinements_used_hist.items()))}")

    # ---- Stage 4: backtest_specification ----
    spec_statuses = Counter()
    for d in run_dirs:
        dec = load_yaml(d / "artifacts" / "decision.yaml")
        if not dec or "__error__" in dec:
            continue
        status = str(dec.get("status", "<missing>")).strip().lower()
        spec_statuses[status] += 1
    n_spec_decisions = sum(spec_statuses.values())
    print(f"\n[backtest_specification] decision.yaml with a status: {n_spec_decisions}/{n_runs}")
    for status, n in spec_statuses.most_common():
        print(f"  {status}: {n}")

    n_candidate_configs = sum(1 for d in run_dirs
                               if (d / "artifacts" / "candidate_strategy_config.json").exists())
    print(f"  candidate_strategy_config.json emitted: {n_candidate_configs}/{n_runs}")

    # ---- E-034 artifacts: variant_selection.yaml / variants_not_pursued.yaml ----
    n_var_sel = sum(1 for d in run_dirs if (d / "artifacts" / "variant_selection.yaml").exists())
    n_var_not_pursued = sum(1 for d in run_dirs if (d / "artifacts" / "variants_not_pursued.yaml").exists())
    print(f"\n[E-034 artifacts, off-by-default] variant_selection.yaml present: "
          f"{n_var_sel}/{n_runs}")
    print(f"[E-034 artifacts, off-by-default] variants_not_pursued.yaml present: "
          f"{n_var_not_pursued}/{n_runs}")

    # Grep-equivalent: does ANY artifact in ANY run record an unpursued variant
    # (the "1 file out of 59" claim in EPIC.md) -- re-derive independently by
    # scanning innovation_notes.yaml / verdict_interpretation.yaml for the phrase.
    hits = []
    for d in run_dirs:
        for fname in ("innovation_notes.yaml", "verdict_interpretation.yaml", "validation_decision.yaml"):
            p = d / "artifacts" / fname
            if not p.exists():
                continue
            try:
                text = p.read_text(encoding="utf-8", errors="replace").lower()
            except Exception:
                continue
            if "not_pursued" in text or "unpursued" in text or "not pursued" in text:
                hits.append(f"{d.name}/{fname}")
    print(f"\n[grep-equivalent] runs whose artifacts mention an unpursued/not_pursued variant: "
          f"{len(hits)}/{n_runs} -> {hits}")

    # ---- verdict_interpreter outcomes (proxy for "what backtest_specification's
    # one chosen config actually achieved") ----
    verdict_labels = Counter()
    for d in run_dirs:
        vi = load_yaml(d / "artifacts" / "verdict_interpretation.yaml")
        if not vi or "__error__" in vi:
            continue
        label = vi.get("verdict_label") or vi.get("disposition") or vi.get("status")
        verdict_labels[str(label)] += 1
    n_verdicts = sum(verdict_labels.values())
    print(f"\n[verdict_interpreter] verdict_interpretation.yaml with a label: {n_verdicts}/{n_runs}")
    for label, n in verdict_labels.most_common():
        print(f"  {label}: {n}")

    # ---- campaign_state.yaml altitude_history (the "38 graded verdicts" source) ----
    cs = load_yaml(CAMPAIGN_STATE)
    if cs and "__error__" not in cs:
        ah = cs.get("altitude_history", [])
        print(f"\n[campaign_state.yaml] altitude_history entries: {len(ah)}")
        outcome_counts = Counter(row.get("outcome") for row in ah)
        for outcome, n in outcome_counts.most_common():
            print(f"  outcome={outcome}: {n}")
        altitude_counts = Counter(row.get("altitude") for row in ah)
        print(f"  altitude distribution: {dict(altitude_counts)}")
        promote_rows = [row for row in ah if row.get("outcome") == "promote"]
        print(f"  rows with outcome == 'promote': {len(promote_rows)}")
    else:
        print(f"\n[campaign_state.yaml] could not load: {cs}")

    # ---- correlation check: variant count vs eventual verdict label, per run ----
    print("\n[correlation] variant_count vs verdict_label, per run (where both known):")
    variant_count_by_run = dict(variant_counts)
    rows = []
    for d in run_dirs:
        vc = variant_count_by_run.get(d.name)
        vi = load_yaml(d / "artifacts" / "verdict_interpretation.yaml")
        label = None
        if vi and "__error__" not in vi:
            label = vi.get("verdict_label") or vi.get("disposition") or vi.get("status")
        if vc is not None and label is not None:
            rows.append((d.name, vc, label))
    for run_name, vc, label in rows:
        print(f"  {run_name}: variants={vc} verdict={label}")
    print(f"  n rows with both variant_count and verdict_label: {len(rows)}/{n_runs}")
    by_label = {}
    for _, vc, label in rows:
        by_label.setdefault(label, []).append(vc)
    print("  mean variant_count by verdict_label:")
    for label, vcs in sorted(by_label.items()):
        print(f"    {label}: n={len(vcs)} mean_variants={sum(vcs)/len(vcs):.2f}")


if __name__ == "__main__":
    main()
