# Improvement 02 — Regime Attribution & Detector Validation

## Gap

The system allocates strategies to regimes (`TRENDING`, `RANGING`, `HIGH_VOL`, etc.) and reports `per_regime_metrics`, but a `kill` or `pivot` verdict currently conflates three independently falsifiable claims:

1. The signal itself has no edge.
2. The signal has edge, but it is gated to the wrong regime.
3. The regime detector is misclassifying periods, so *any* regime-conditioned metric is unreliable.

Without separating these, `regime_uninformative` and `weak_signal` verdicts may be killing signals that were actually fine but mis-gated, or drawing conclusions from a regime partition that is itself wrong. This is the highest-leverage fix in the plan because every other diagnostic (Improvement 01, 03) that reads `per_regime_metrics` inherits this risk.

## Part A — Standalone regime detector validation

The regime detector must be validated **independently of any specific hypothesis**, on a recurring basis (not re-litigated per run), and its validity must be a precondition other stages can check.

### New artifact: `regime_detector_report.yaml`

Root-level (campaign-scoped, refreshed periodically, not per-run):

```yaml
detector_version: string
evaluated_at: timestamp
per_symbol_per_timeframe:
  - symbol: string
    timeframe: string
    metrics:
      regime_persistence_median_bars: number       # how long regimes last once detected
      transition_frequency_per_window: number       # flip-flopping indicates noisy detection
      parameter_sensitivity: number                  # % of periods that change label under small parameter perturbation (stability check)
      agreement_with_reference_labels: number | null # if any hand-labeled or external reference period exists
    confidence: enum[high, medium, low]
    known_weak_periods: list[string]  # date ranges where confidence is low, e.g. transition zones
```

### New tool: `tools/validate_regime_detector.py`

Deterministic (no LLM), analogous to `run_protocol.py`:
1. Runs the regime detector standalone across historical data per symbol/timeframe.
2. Computes `regime_persistence_median_bars` and `transition_frequency_per_window` directly from the label sequence.
3. Computes `parameter_sensitivity` by re-running the detector with small perturbations (e.g., ±10% on its threshold parameters) and measuring the fraction of bars whose label changes.
4. If a reference/hand-labeled period is configured, computes agreement.
5. Assigns `confidence` (high/medium/low) via a simple rule (e.g., high persistence + low sensitivity = high confidence) — codify explicit thresholds in the tool, don't leave this to an LLM to eyeball.
6. Writes `regime_detector_report.yaml`.

### New skill: `regime-auditor`

**Goal:** Read `regime_detector_report.yaml` and decide whether current regime detection is trustworthy enough for hypothesis-level conclusions to be drawn from `per_regime_metrics`, and if not, prescribe a fix (parameter re-tuning, alternative detection method, or flagging that this symbol/timeframe cannot support regime-gated strategies yet).

**Trigger:** Run automatically (a) at campaign start, (b) whenever `verdict-interpreter` resolves `mechanism_failure = regime_misattribution` (see Improvement 01), (c) periodically (e.g., every N runs) as a standing health check.

**Output:** `regime_audit_decision.yaml`:
```yaml
status: enum[trustworthy, needs_retune, unusable_for_this_symbol_timeframe]
affected_symbols_timeframes: list
recommended_action: string
```

If `status = needs_retune`, orchestrator pauses regime-gated hypothesis generation for the affected symbol/timeframe until re-validated. If `status = unusable_for_this_symbol_timeframe`, this is recorded in `campaign_knowledge_base.yaml` (Improvement 05) so future hypothesis generation avoids regime-gating there entirely.

## Part B — Per-hypothesis regime attribution

For every backtested hypothesis, `verdict-interpreter` must be able to answer three separate questions before issuing a verdict:

```yaml
regime_attribution:
  detector_confidence: enum[high, medium, low]   # pulled directly from regime_detector_report.yaml for this symbol/timeframe
  signal_performs_in_intended_regime: boolean     # per_regime_metrics for the gated regime only
  signal_performs_in_other_regimes: boolean       # would it have worked ungated / in a different regime?
  conclusion: enum[
    signal_bad_everywhere,
    signal_good_wrong_regime_gate,
    signal_good_regime_gate_correct,
    inconclusive_low_detector_confidence
  ]
```

Logic the skill must apply, in order:
1. If `detector_confidence != high` → `conclusion = inconclusive_low_detector_confidence`, and the verdict must be `refine`-at-detector-level (route to regime-auditor), not a hypothesis-level `kill` or `pivot`.
2. Else if the signal performs well in a *different* regime than the one it was gated to → `signal_good_wrong_regime_gate` → prescribed action is re-gate and re-test at altitude 1 (parameter change: which regime it's active in), not discard the family.
3. Else if it performs poorly in all regimes → `signal_bad_everywhere` → genuine pivot/kill candidate.
4. Else → `signal_good_regime_gate_correct` → normal promotion path.

This directly answers the concern: "nothing tells us if the strategy is bad, mis-allocated to a regime, or if the regime is badly identified" — each is now a distinct, checked branch.

## Schema/orchestrator changes

- `schemas/regime_detector_report.schema.json`, `schemas/regime_audit_decision.schema.json` — new.
- `schemas/verdict_interpretation.schema.json` — add `regime_attribution` block (required whenever the hypothesis under test is regime-gated).
- `workflow/stages.yaml` — register `regime_auditor` as a stage with `assigned_engine: tool` for `validate_regime_detector.py` and `assigned_engine: claude` for the `regime-auditor` skill decision step.
- `workflow/run_phase1_research.py` — before any `verdict_interpreter` run reads `per_regime_metrics`, check `regime_detector_report.yaml` freshness/confidence for that symbol/timeframe; if stale or missing, trigger regime validation first.

## Acceptance criteria

1. `regime_detector_report.yaml` exists and is refreshed on a defined cadence, independent of any specific hypothesis run.
2. No `verdict_interpretation.yaml` for a regime-gated hypothesis is finalized with `conclusion = signal_bad_everywhere` (i.e., a real kill/pivot) while `detector_confidence != high` for that symbol/timeframe — this must be mechanically blocked, not just discouraged in the prompt.
3. At least one historical run where a signal was killed can be shown, retroactively, to have had `detector_confidence: low` at the time — used as a regression test that the new gate would have prevented that false kill.
4. `campaign_knowledge_base.yaml` (Improvement 05) receives an entry whenever `regime_audit_decision.status = unusable_for_this_symbol_timeframe`.
