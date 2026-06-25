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

`validation_decision.yaml` must include:
- hypothesis_id
- status
- rationale
- blocking_issues
- conditions (list of strings, only when status is conditional_approve)

## Checklist
- Restate the hypothesis in falsifiable form.
- Define null expectation.
- List at least 5 failure modes.
- Identify leakage, look-ahead, and overfitting risks.
- Define sample split logic.
- Return approve, conditional_approve, refine, or reject. Use conditional_approve when the hypothesis is sound but one specific, resolvable condition must be honored in the config — include a conditions list in the output.
- Check whether the idea can be tested through a minimal change to the existing bot architecture.

## Permitted decision criteria
decision_rules in validation_protocol.yaml MUST use only these measurable criteria.
Do not invent metrics not in this list — they cannot be evaluated by the backtest pipeline.

Available (directly in metrics.json):
- sharpe: annualized Sharpe ratio across walk-forward windows (median)
- win_rate: fraction of profitable trades
- max_drawdown_pct: maximum drawdown percentage
- trade_count: total trades across all windows
- min_trade_count: minimum trades in any single window

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

## Forbidden
- Do not write backtest code.
- Do not approve vague ideas.
- Do not skip explicit failure modes.
- Do not rely on narrative confidence.
- Do not emit decision criteria using metrics outside the Permitted list above.

## Embedded stance
Assume the hypothesis is wrong until enough evidence is specified.