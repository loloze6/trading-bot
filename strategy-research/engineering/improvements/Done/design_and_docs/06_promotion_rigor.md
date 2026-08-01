# Improvement 06 — Promotion Rigor (Multiple-Testing Correction & Holdout Enforcement)

## Gap

This is the defensive counterpart to Improvements 01–05: it does not help *find* profitable strategies, it stops the pipeline from *wrongly declaring* a strategy profitable. Implement last, once the generative improvements are producing more candidates worth protecting — but implement it before any strategy is actually sent to live deployment, since this is the last line of defense against false positives.

Two distinct gaps:

1. **No multiple-comparisons control.** `campaign_state.yaml` tracks runs and failed families but nothing adjusts the promotion bar for how many hypotheses have been tested in this campaign. With enough attempts, a strategy will eventually clear a fixed `median_sharpe` threshold by chance alone.
2. **Holdout is defined but not enforced.** `pipeline_state.flags.holdout_reserved` and the glossary describe a holdout concept, but the stage map goes directly from walk-forward `protocol_execution` to `verdict_interpreter` to `promote` — there is no distinct, enforced, single-use holdout evaluation gate before terminal promotion.

## Part A — Multiple-testing correction

### New artifact: `promotion_audit.yaml`

Produced whenever a hypothesis reaches candidate-for-promotion status (i.e., `verdict_interpreter` would otherwise output `promote`).

```yaml
hypothesis_id: string
raw_median_sharpe: float
total_hypotheses_tested_this_campaign: int      # pulled from campaign_state.runs count
total_variants_tested_this_campaign: int         # finer-grained: includes innovation_expansion variants, not just top-level runs
deflated_sharpe_ratio: float                     # corrected for number of trials (standard deflated Sharpe methodology)
correction_method: string                        # document which method/formula was applied
promotion_threshold_raw: float
promotion_threshold_deflated: float
passes_deflated_threshold: boolean
```

### Implementation

- Add a deterministic post-processing step (in `tools/run_protocol.py` or a new `tools/deflate_sharpe.py`) that computes a deflated Sharpe ratio using the campaign's total trial count (both full runs and innovation_expansion variants — variants tested and discarded within a run still count as trials). Use an established deflated/probabilistic Sharpe ratio formula; do not invent a novel correction.
- `campaign_state.yaml` must already be tracking a running trial count (it tracks `runs` — extend to also track cumulative variant count across `innovation_expansion` stages, since that's the true number of implicit comparisons, not just top-level runs).
- The `promote` verdict from `verdict_interpreter` becomes provisional; final promotion requires `promotion_audit.passes_deflated_threshold = true`.

## Part B — Holdout enforcement

### New pipeline stage: `holdout_evaluation`

Inserted between a provisional `promote` verdict and terminal `research_decision`:

```
[Claude] verdict_interpreter → promote (provisional)
            │
            ▼
[Tool]   holdout_evaluation   ← NEW, single-use, deterministic
            │
     ┌──────┴──────┐
  pass            fail
     │              │
     ▼              ▼
research_decision   kill (route back through verdict_interpreter
(promoted)           with a documented holdout-failure root_cause)
```

### Enforcement rules (must be mechanically guaranteed, not just prompted)

1. The holdout date range is fixed at campaign start (in `protocol_definitions`/`baseline_v1.json` or a campaign-level config) and **never used in any walk-forward window** for any run in the campaign. Add a validation check in `tools/check_data.py` or `run_protocol.py` that raises an error if a protocol's walk-forward windows overlap the configured holdout range.
2. The holdout evaluation runs **exactly once** per hypothesis. `pipeline_state.flags.holdout_reserved` must be checked before running — if already consumed for this hypothesis_id, refuse to re-run it (prevents implicitly tuning against holdout via repeated attempts).
3. If a hypothesis fails holdout, it cannot be resubmitted for holdout evaluation after further "refinement" — a holdout failure is terminal for that specific hypothesis instance (refinements based on holdout results would defeat the purpose of holdout). Refinements are permitted only if they're driven by walk-forward diagnostics from a *different, not-yet-holdout-tested* variant.

### New artifact: `holdout_result.yaml`

```yaml
hypothesis_id: string
holdout_window: [start, end]
holdout_sharpe: float
holdout_max_drawdown: float
walk_forward_sharpe_for_comparison: float
degradation_pct: float          # how much performance dropped from walk-forward to holdout
status: enum[pass, fail]
consumed_at: timestamp          # enforces single-use
```

## Orchestrator/schema changes

- `workflow/stages.yaml` — register `holdout_evaluation` as a new stage, `assigned_engine: tool`.
- `schemas/promotion_audit.schema.json`, `schemas/holdout_result.schema.json` — new.
- `workflow/run_phase1_research.py` — insert `holdout_evaluation` into routing between provisional `promote` and `research_decision`; enforce single-use via `pipeline_state.flags.holdout_reserved`.
- `quant-validation` skill — reference the fixed campaign holdout range in `sample_split_design` so it's declared upfront, not discovered ad hoc at promotion time.

## Acceptance criteria

1. `promotion_audit.yaml` is produced for every provisional `promote` verdict; no hypothesis reaches `research_decision` (promoted) without a passing `passes_deflated_threshold`.
2. The deflated Sharpe correction visibly tightens as `total_variants_tested_this_campaign` grows — verify with a synthetic test: same raw Sharpe, higher trial count, lower deflated Sharpe.
3. Walk-forward windows never overlap the configured holdout range — verified by an automated check that fails the pipeline setup if they do.
4. A hypothesis cannot pass through `holdout_evaluation` more than once — verified by attempting a second call and confirming it is rejected via `pipeline_state.flags.holdout_reserved`.
5. At least one existing/past promoted strategy (if any) can be retroactively run through this gate as a regression test, to confirm the new gate doesn't trivially reject genuinely good strategies (i.e., check for excessive conservatism, not just correctness of the block).
