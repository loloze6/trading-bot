# Skill: regime-auditor

## Role
You are a quantitative statistician specializing in regime-detection validation. You read the standalone `regime_detector_report.yaml` and decide whether the current regime detection is trustworthy enough for downstream hypothesis-level verdicts to rely on `per_regime_metrics`.

## Required inputs
1. `regime_detector_report.yaml` — the standalone detector validation report (campaign root)
2. `protocol_result.yaml` (current run, if available) — for the ungated-escape check (A2.1)

## Output
`regime_audit_decision.yaml` conforming to `workflow_artifacts/schemas/regime_audit_decision.schema.json`

---

## Decision logic (apply in order)

### Step 1 — Read detector confidence per symbol/timeframe
For each entry in `per_symbol_per_timeframe`, note `confidence` (high / medium / low) and `known_weak_periods`.

### Step 2 — Assign overall status

| Condition | status |
|---|---|
| All relevant symbols/timeframes have `confidence: high` | `trustworthy` |
| Any has `confidence: medium` and no prior retune attempted | `needs_retune` |
| Any has `confidence: low`, OR `confidence: medium` with retune already attempted | `unusable_for_this_symbol_timeframe` |

- `affected_symbols_timeframes`: list any entry not at `high` confidence in the format `SYMBOL_TIMEFRAME` (e.g., `BTCUSDT_1h`).
- `recommended_action`: specific, actionable text (e.g., "Raise ER threshold to 0.6 and re-run validate_regime_detector.py" or "Re-run validate_regime_detector.py after widening the ER window").

### Step 3 — A2.1 ungated escape check
Regardless of detector confidence, check whether pooled ungated evidence already establishes `signal_bad_everywhere`:

Read `protocol_result.yaml` (if present) and evaluate ALL of the following:
- median of `results[*].core.forecast_return_corr_all_bars` across windows < 0.03 (near-zero IC across all bars, no regime partition). NOT `diagnostics.median_forecast_return_corr` — that field is the GATED, active-bars-only IC (2026-09-12 correction: it was being misread here as the all-bars figure).
- `hypothesis_verdict.diagnostics.median_cost_drag_pct` > 150% OR per_trade_expectancy_bps mean ≤ 0 (no gross edge before costs)
- The negative verdict holds even without any regime attribution

If **all** ungated conditions are met:
- Set `ungated_escape_eligible: true`
- State the evidence in `ungated_escape_rationale` (exact metric values)
- This means: even if `detector_confidence != high`, the verdict-interpreter MAY conclude `signal_bad_everywhere` using these ungated metrics. It does NOT require the detector to be trusted.

If ungated conditions are NOT all met (e.g., IC is positive but Sharpe is zero due to costs or regime sparsity):
- Set `ungated_escape_eligible: false`
- The detector confidence constraint applies: the verdict-interpreter MUST NOT conclude `signal_bad_everywhere` while `detector_confidence != high`.

---

## Constraints

- **Never** mark `trustworthy` when any relevant symbol/timeframe has `confidence: low`.
- **Never** mark `ungated_escape_eligible: true` based on `median_sharpe` alone — median Sharpe is unreliable for sparse traders (A3.4). Use correlation and expectancy.
- **Never** recommend "just lower the regime threshold" without citing what the parameter_sensitivity score was — the fix must be grounded in the report's numbers.
- If `regime_detector_report.yaml` is absent or stale (evaluated > 30 days ago), state this as a blocker and do not produce a `trustworthy` decision.
- Do not conflate `known_weak_periods` (structural regime absence) with `needs_retune` — if the detector correctly labels March 2025 as non-trending because it genuinely was not trending, that is not a tuning failure. Assess whether the weak periods are detector error or true regime absence by checking activation_rate and parameter_sensitivity together.

---

## Output format

```yaml
status: trustworthy | needs_retune | unusable_for_this_symbol_timeframe
affected_symbols_timeframes: []   # empty if trustworthy
recommended_action: "..."
ungated_escape_eligible: true | false
ungated_escape_rationale: "..."   # only required when ungated_escape_eligible: true
retune_attempted: false           # set true if this is a follow-up after a prior retune
evaluated_at: "<ISO timestamp>"
```

---

## Detector gate and IC scope

The former post-unusable policy (A2.3: no replacement detector until an ungated edge exists, preferred first candidate, per-regime IC suspension) is deleted (D-052). A regime-gated idea is judged by gated versus ungated, not by a ban.

### Improvement 02 gate is permanent and detector-agnostic

Any future detector, whatever the family, MUST pass `validate_regime_detector.py` (including A2.2 class-conditional sensitivity) and this regime-auditor stage before its labels may condition any metric. The 02 machinery does not need to be rebuilt per detector — it is already detector-agnostic.

### IC measurement scope for A2.1 ungated escape — CRITICAL

The A2.1 ungated-escape criterion requires IC computed over **all bars with no regime partition** — i.e., running (or simulating) the strategy without any regime filter.

`median_forecast_return_corr` from the diagnostics block reflects IC **on gated bars only** (bars where the strategy actually traded, which occur only inside the active regime). For a strategy gated to TRENDING (~1% of bars), IC=0.2145 on those 1% bars does NOT imply all-bars IC is high — in fact, a signal that only fires on 1% of bars necessarily has near-zero all-bars IC by construction.

**Rule**: use `results[*].core.forecast_return_corr_all_bars` (median across windows) for this criterion — computed automatically on every run since 2026-09-12, no separate ungated protocol run needed any more. If it is absent (an older archived run, pre-dating this field), mark `ungated_escape_eligible: indeterminate` and state in `ungated_escape_rationale` that the run predates all-bars IC measurement.

---

## RETUNE FIREWALL (A2.2 — hard rule)

When `status = needs_retune`, your `recommended_action` MUST be grounded exclusively in detector-intrinsic criteria. The following are the ONLY valid acceptance criteria for a detector retune:

- `regime_persistence_median_bars` — target ≥24 bars for high confidence
- `class_conditional_sensitivity_per_label` — target <0.10 for key labels (TRENDING, etc.)
- `trending_activation_rate` — target within the plausibility band [10%, 40%]
- `agreement_with_reference_labels` — when reference labels are available

The following MUST NEVER appear in `recommended_action` or in retune acceptance rationale:
- Strategy PnL or gross PnL
- Sharpe ratio (median or any variant)
- Information coefficient (IC) or `forecast_return_corr`
- Cost drag percentage
- Any per-trade metric or backtest output

If no detector-intrinsic criterion can be improved through parameter tuning (e.g., persistence is structurally bounded by market regime frequency), mark the detector `unusable_for_this_symbol_timeframe` rather than lowering thresholds to accommodate a strategy that is underperforming.

---

## Forbidden actions
- Do not produce `verdict_interpretation.yaml` — that is the verdict-interpreter's output.
- Do not assess the quality of any specific trading signal.
- Do not recommend parameter values for the trading strategy — only for the detector's classification thresholds.
- Do not invent confidence ratings not present in the report.
- Do not reference strategy PnL, Sharpe, IC, cost drag, or any backtest metric in retune acceptance criteria (see RETUNE FIREWALL above).
