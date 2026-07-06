# Improvement 05 — Campaign Knowledge Base (Cross-Run Findings)

## Gap

`findings_carryover.yaml` already exists but is **linear, run-to-run memory**: it tells the *next* run what not to repeat, via `what_failed`, `diagnostic_snapshot`, `what_not_to_try`. It does not support cross-run inference. Two separate runs each independently discovering "trending-regime signals derived from public flow data don't work on majors at 1h" remain two disconnected facts in two YAML files — nothing combines them into a generalizable conclusion the way a human researcher would after ten experiments.

This improvement adds a queryable, dimensioned knowledge store that `campaign-review` (and future hypothesis generation) can reason over, so profitability is pursued as a **combination of accumulated findings**, not as a sequence of isolated promote-or-reject attempts.

## New artifact: `campaign_knowledge_base.yaml`

Root-level, one per campaign, updated after every run (not just at campaign_review time).

```yaml
campaign_id: string
last_updated: timestamp

# The core structure: a fact table indexed by dimension, not by run.
findings:
  - mechanism: enum[...]              # from Improvement 01's edge_source.category / mechanism_failure taxonomy
    regime: string
    symbol: string
    timeframe: string
    indicator_category: string        # from Improvement 04's indicator_library
    outcome: enum[confirmed_no_edge, confirmed_edge_found, inconclusive, edge_but_wrong_regime, edge_but_execution_gap]
    confidence: enum[high, medium, low]
    supporting_run_ids: list[string]
    last_confirmed: timestamp
    notes: string

# Derived views, recomputed on write (not separately maintained)
coverage_matrix:
  # mechanism x regime x symbol/timeframe cells and whether they've been tested
  tested_cells: list[object]
  untested_cells: list[object]        # explicitly surfaced — this is what tells campaign_review where the unexplored space is

exhausted_mechanisms:
  # mechanisms with high-confidence confirmed_no_edge across multiple regimes/symbols
  - mechanism: string
    confirmed_no_edge_in: list[string]   # regime/symbol/timeframe combos
    still_untested_in: list[string]
```

## How it's populated

After every run's `verdict_interpreter` stage completes (not only at `campaign_review`), a lightweight orchestrator hook writes a new `findings` entry using:
- `edge_source.category` and `mechanism_failure` from Improvement 01
- `regime_attribution.conclusion` from Improvement 02 (so `edge_but_wrong_regime` is a distinct, correctly-labeled outcome, not conflated with `confirmed_no_edge`)
- `trade_attribution.primary_weakness` from Improvement 03 (so `edge_but_execution_gap` is distinct too)
- `indicator_id`/`category` from Improvement 04

This means Improvement 05 has a hard dependency on 01–03 producing structured, taggable outputs — it is the aggregation layer sitting on top of them, not a replacement for them.

## Skill constraint changes — `campaign-review`

Currently decides `continue / reframe / escalate / terminate` using run history in `campaign_state.yaml` (list of runs + verdicts). Change its required input to include `campaign_knowledge_base.yaml`, and require it to explicitly answer, before deciding:

1. Which `coverage_matrix` cells are `untested_cells` and worth trying next (this should directly inform a `reframe` decision's new research_brief).
2. Which mechanisms are in `exhausted_mechanisms` and must not be retried in the same regime/symbol/timeframe without new evidence.
3. Whether the pattern across `findings` suggests a *combination* worth testing that no single run proposed — e.g., "mechanism X failed alone in regime A, but was never tried combined with mechanism Y" — and if so, this becomes the seed of the next `research_brief.existing_context`.

This directly operationalizes "profitability will come from a combination of acquired knowledge from various backtesting" — the knowledge base is what makes combination-seeking possible, since combinations can only be proposed once individual results are stored in a form that supports cross-referencing.

## Skill constraint changes — `hypothesis-design`

When starting a new run, the handoff must include the relevant slice of `campaign_knowledge_base.yaml` (filtered to the current symbol/timeframe), not just the previous run's `proposed_brief.existing_context`. The skill must check `exhausted_mechanisms` before proposing a hypothesis in an already-exhausted cell.

## Relationship to `findings_carryover.yaml`

Keep `findings_carryover.yaml` as-is for its current purpose (immediate next-run handoff, human-readable single-run summary). `campaign_knowledge_base.yaml` is the aggregated, structured superset — every `findings_carryover.yaml` should be absorbed into it as a `findings` entry on write, not maintained as a competing memory system.

## Schema/orchestrator changes

- `schemas/campaign_knowledge_base.schema.json` — new.
- `workflow/run_phase1_research.py` — add a post-`verdict_interpreter` hook that writes a `findings` entry and recomputes `coverage_matrix`/`exhausted_mechanisms`.
- `campaign-review` handoff template — add `campaign_knowledge_base.yaml` as a required input.

## Acceptance criteria

1. `campaign_knowledge_base.yaml` gains a new `findings` entry after every completed run, not only at `campaign_review` checkpoints.
2. `coverage_matrix.untested_cells` is non-empty and specific enough to directly seed a `reframe` decision's new research brief.
3. `campaign-review`'s decision rationale, when `reframe` or `continue` is chosen, references specific `findings` or `coverage_matrix` entries rather than only the immediately preceding run.
4. A retrospective check: given the current campaign's run history, the knowledge base can correctly reconstruct at least one `exhausted_mechanisms` entry that the current linear `findings_carryover` chain does not surface (demonstrating the aggregation adds information the linear version didn't have).
