---
name: quant-validation
description: Acts as devil's advocate for a trading hypothesis by defining falsification criteria, identifying bias risks, listing failure modes, and deciding whether the idea should proceed.
---

# Quant Validation

## Mission
Pressure-test the hypothesis before implementation.

## Required inputs
- `expanded_hypothesis_card.yaml`

## Required outputs
- `validation_protocol.yaml`
- `validation_decision.yaml`

## Output requirements
`validation_protocol.yaml` must include:
- hypothesis_id
- falsifiable_statement
- null_expectation
- required_evidence
- bias_risks
- failure_modes
- sample_split_design
- decision_rules
- cost_feasibility   ← **REQUIRED (Improvement 09 Layer 1)**

`validation_decision.yaml` must include:
- hypothesis_id
- status
- rationale
- blocking_issues
- conditions (list of strings, only when status is conditional_approve)

YAML formatting rule — applies to ALL string values in both artifacts:
- Any string value containing a colon (:) MUST use block scalar syntax (| or >) or be
  quoted with single or double quotes.
- List items (- items) that contain colons MUST be quoted: `- "key: value"` not `- key: value`
- This rule applies even inside nested mappings and multi-line values.
- Violation causes a YAML parse error that halts the pipeline.

## Checklist
- Restate the hypothesis in falsifiable form.
- Define null expectation.
- List at least 5 failure modes.
- Identify leakage, look-ahead, and overfitting risks.
- Define sample split logic — **including holdout range declaration (A6.1, see below)**.
- Return approve, conditional_approve, refine, or reject. Use conditional_approve when the hypothesis is sound but one specific, resolvable condition must be honored in the config — include a conditions list in the output.
- Check whether the idea can be tested through a minimal change to the existing bot architecture.
- **Complete the `cost_feasibility` block** (Improvement 09 Layer 1 — see section below).

## IMPROVEMENT 06 — Holdout Range Declaration (required in every validation_protocol.yaml)

Before finalizing `validation_protocol.yaml`, read `../../config/campaign_data_policy.yaml`
and record the campaign holdout range in `sample_split_design`. The holdout is single-use and
must be declared at validation time — not discovered at promotion.

```yaml
sample_split_design:
  walk_forward_range: "<from walk_forward_extension in campaign_data_policy.yaml>"
  holdout_range: "<from holdout_range in campaign_data_policy.yaml — FROZEN, do not use in any backtest>"
  holdout_note: "Single-use per A6.1. Evaluated only at holdout_evaluation stage after deflated Sharpe gate passes."
  windows: <integer — number of walk-forward windows planned>
  window_size_bars: <integer>
  step_size_bars: <integer>
```

**Hard rule:** `validation_protocol.yaml.sample_split_design` must contain `holdout_range`.
Any protocol that omits this field is missing a required output and will fail the deliverable check.

## Permitted decision criteria
decision_rules in validation_protocol.yaml MUST use only these measurable criteria.
Do not invent metrics not in this list — they cannot be evaluated by the backtest pipeline.

Available (directly in metrics.json):
- sharpe: annualized Sharpe ratio across walk-forward windows (median)
- win_rate: fraction of profitable trades
- max_drawdown_pct: maximum drawdown percentage
- trade_count: total trades across all windows
- min_trade_count: minimum trades in any single window
- forecast_return_corr (field name: median_forecast_return_corr): pooled forecast-vs-forward-return
  correlation across walk-forward windows. **UNIT CONVENTION — ALWAYS a raw decimal in [-1, 1]
  (e.g. 0.02), NEVER a percentage.** `run_protocol.py`'s criterion parser does no unit conversion
  (compares the raw value directly against whatever number you write), so a criterion phrased with
  a "%" suffix (e.g. "IC >= 1.5-2.0%") is silently comparing 0.02 against the literal number 1.5 —
  a threshold no correlation coefficient can ever clear, since |corr| <= 1 always. Write thresholds
  as bare decimals: "forecast_return_corr >= 0.015" not "IC >= 1.5%". (2026-07-09, P4_ts_trend:
  this exact ambiguity appeared in a validation_protocol.yaml before this rule existed — see this
  skill's changelog and campaign_knowledge_base.yaml's p4_sma_trend_longonly_daily_auto entry.)
  For a long-only (or otherwise single-constant-magnitude-when-active) signal, this is computed via
  a pre-registered block-bootstrap fallback, not a naive per-bar correlation — see
  `trading-bot/performance/signal_statistics.py` and `run_protocol.py::_pooled_ic_with_bootstrap_fallback`.

Computable (derived from metrics.json per_regime):
- regime_frequency: mean_reversion bars / total bars (use field: per_regime)

UNTESTED (record as aspirational but do not gate approval on these):
- buy_hold_sharpe_delta: signal Sharpe minus passive hold Sharpe
- regime_conditional_sharpe: Sharpe computed only on in-regime bars
- parameter_drift: walk-forward parameter stability

Forbidden (never emit these — undefined or unmeasurable in current pipeline):
- Walk-forward PE (undefined metric)
- Regime detection lag (no ground-truth regime timestamp recorded)
- Any metric requiring a second backtest run (e.g. V5 reverse control)

## IMPROVEMENT 09 — Layer 1 Cost Feasibility (required in every validation_protocol.yaml)

Populate this block from `config/cost_model.yaml` (round_trip_cost_bps per symbol):

```yaml
cost_feasibility:
  assumed_round_trip_cost_bps: <from cost_model.yaml for primary symbol, e.g. 17.0 for BTCUSDT>
  expected_holding_bars:
    min: <minimum holding period from signal class and timeframe>
    max: <maximum holding period from signal class and timeframe>
  expected_trades_per_window: <implied count given holding period and any regime gating>
  required_gross_edge_bps_per_trade: <= 2 × assumed_round_trip_cost_bps>
  plausibility: <plausible | marginal | implausible>
  plausibility_rationale: "<must cite the signal class and timeframe. Example: '1h mean-reversion with 6–12 bar holds must clear 34 bps/trade gross; established mean-reversion signals on 1h crypto typically achieve 10–30 bps — marginal to implausible'>"
```

### Hard rule (mirrors "no falsifiable statement → no approval"):

**`plausibility: implausible` → validation status CANNOT be `approve` or `conditional_approve`.**

The blocking issue must be "turnover/cost mismatch". Typical fixes for an implausible verdict:
- Longer timeframe (reduces round-trip cost per holding period)
- Tighter regime gating (fewer, higher-conviction trades)
- Wider holding period assumption (more bars per trade to amortise costs)

If implausible AND no fix is viable within the current architecture: status = `reject`.

### Plausibility rubric:

| Plausibility | Condition |
|---|---|
| `plausible` | Established signal class on this timeframe demonstrably earns ≥ 2× round-trip cost (e.g. strong trend-following on 4h+, daily mean-reversion). |
| `marginal` | Signal class can earn the required edge under favourable conditions but the evidence base is thin or the timeframe is borderline (e.g. moderate-IC mean-reversion on 1h). |
| `implausible` | Signal class cannot plausibly earn 2× round-trip cost at this timeframe with this holding period (e.g. high-frequency entries on 1h with 2–3 bar holds, or a regime-gated strategy that fires on ~1% of bars requiring ~34 bps/trade to break even at 17 bps round-trip). |

Note: `config/cost_model.yaml` is the single source of truth for cost numbers. Do not hardcode fees.

## Forbidden
- Do not write backtest code.
- Do not approve vague ideas.
- Do not skip explicit failure modes.
- Do not rely on narrative confidence.
- Do not emit decision criteria using metrics outside the Permitted list above.
- **Do not approve or conditionally approve when `cost_feasibility.plausibility = implausible`.**
- Do not hardcode fee or spread numbers — always read from `config/cost_model.yaml`.

## Embedded stance
Assume the hypothesis is wrong until enough evidence is specified.

## Changelog
- 2026-07-09: added `forecast_return_corr` to the Permitted decision criteria list, with an
  explicit raw-decimal unit convention. Before this, IC/correlation was never in the Permitted
  list at all, yet a validation_protocol.yaml still emitted a "Walk-forward pooled IC >=
  1.5-2.0%" criterion in violation of this skill's own "do not invent metrics" rule — with the
  threshold worded as a percentage against a metric that's always a raw decimal in [-1, 1]. The
  criterion was structurally impossible to pass (or fail, ambiguously) as a result.
  verdict_interpreter caught the inconsistency itself on the affected run (P4_ts_trend/run_054)
  and reasoned through it transparently rather than silently picking a side, but the ambiguity
  should never have reached that stage. See campaign_knowledge_base.yaml's
  p4_sma_trend_longonly_daily_auto for the full incident record.