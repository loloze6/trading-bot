# Improvement 08 — Signal Prescreen (Cheap IC Gate Before Full Backtest)

## Gap

The most common failure verdict is `weak_signal` (`forecast_return_corr < 0.03`) — discovered only **after** a full walk-forward run with portfolio construction, rebalance-threshold logic, cost simulation, and per-window aggregation. That is the most expensive possible way to learn that a forecast has no correlation with returns. Worse, the full-pipeline measurement conflates signal quality with execution effects: a near-zero end-to-end correlation could be a dead signal *or* a live signal destroyed by the allocation/rebalance layer, and current outputs cannot distinguish them (Improvement 03 helps post-hoc; this improvement prevents the spend).

The trading-bot architecture already separates raw forecast generation from portfolio reconciliation (components return a raw float forecast; `forecast_to_allocation = forecast / 10.0` and the ≥0.20 rebalance threshold are applied downstream). This makes a standalone, vectorized forecast computation feasible without re-simulation.

## New stage: `signal_prescreen` (deterministic tool, no LLM)

Inserted between `backtest_specification` and `protocol_execution` in `workflow/stages.yaml`.

### New tool: `tools/prescreen_signal.py`

Given `strategy_config.json` and the protocol's data range:

1. Compute the composite forecast series bar-by-bar over the full walk-forward range (signal layer only — no positions, no rebalancing, no costs). Reuse the existing component classes; do not reimplement indicators.
2. Compute, per window and pooled:
   - `ic_spearman`: rank correlation of forecast[t] vs return[t→t+1]
   - `ic_horizon_curve`: same at horizons {1, 4, 12, 24} bars — reveals whether the signal predicts at the timeframe the strategy trades
   - `ic_by_regime`: IC conditioned on regime label (only if `regime_detector_report.confidence == high` per Improvement 02; otherwise report ungated only)
   - `ic_significance`: p-value via moving-block bootstrap (block ≈ 24 bars for 1h) — NOT an i.i.d. test; autocorrelation would fake significance
   - `turnover_proxy`: mean |Δforecast| per bar and implied rebalance count given the 0.20 allocation threshold — feeds Improvement 09
   - `forecast_autocorr_halflife`: how persistent the forecast is (fast-decaying forecast + slow rebalance = structural mismatch)
3. Write `prescreen_result.yaml`.

### Routing (orchestrator)

| Prescreen outcome | Route |
|---|---|
| `ic_significance.p > 0.10` pooled AND in every regime | Skip backtest entirely → `verdict_interpreter` with `mechanism_failure` candidate `no_informational_content_this_venue`; verdict issued on prescreen evidence at ~1% of the compute |
| Significant but **negative** IC | Flag `signal_inversion` pre-backtest → route to refine (polarity) without spending a walk-forward on the wrong sign |
| Significant positive IC, but `turnover_proxy` fails the Improvement 09 cost hurdle | Route to refine (trade filter / signal smoothing) before backtest |
| Significant positive IC, cost hurdle passes | Proceed to `protocol_execution` (unchanged) |

### Two side benefits

- **Detector-independent kill path for Improvement 02:** ungated pooled IC ≈ 0 with tight CI supports `signal_bad_everywhere` even when regime detector confidence is low — resolving the deadlock where low detector confidence would otherwise block every conclusion indefinitely.
- **Clean attribution for Improvement 03:** if prescreen IC was healthy but the full backtest fails, the failure is by construction downstream of the signal (execution/costs/sizing) — `trade_attribution` starts from a known-good signal instead of inferring it.

## Guardrail: prescreen is a filter, not a fitness function

The prescreen must never be used to *rank and select* among many variants on the same data (that would be a new overfitting channel: IC-mining). Its output is binary/route-only per variant. Variant prioritization remains `innovation_notes.recommended_test_order` (a priori, from the hypothesis stage). Trial counting for Improvement 06 must include prescreened-and-killed variants — a prescreen kill is still a trial.

## Schema/orchestrator changes

- `workflow_artifacts/schemas/prescreen_result.schema.json` — new.
- `workflow/stages.yaml` — register `signal_prescreen`, `assigned_engine: tool`.
- `workflow/run_phase1_research.py` — insert routing table above; write prescreen kills into campaign trial count.
- `verdict-interpreter` skill — accept `prescreen_result.yaml` as an alternative evidence source when no backtest was run.

## Acceptance criteria

1. Prescreen runtime < 60 s per variant on the baseline_v2 range (vs minutes for full walk-forward).
2. Regression test: re-run prescreen on ≥3 historical runs that ended in `weak_signal` — prescreen must flag all of them (would-have-skipped), and on ≥1 historical run with a positive verdict (Keltner) — prescreen must pass it.
3. Prescreen-killed variants appear in the campaign trial count used by Improvement 06.
4. `ic_significance` uses block bootstrap (code-review check: no i.i.d. permutation of an autocorrelated series).
