---
plan: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines_1d
idea: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of excess 5-bar forward return on depth forecast, mean_reversion grid bars: 0.000385223; OLS slope t: 0.786705 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 100 grid cases)
- Supporting check: none
- Counts: grid cases: 1652
- Decided by: The t lies between -2 and 2 (the inconclusive rule).
- Reading: The situation is ret90 < 0, recomputed from the closes where 90 prior bars exist in the window and otherwise taken from the recorded regime, together with depth <= 0 and forecast > 0; the normal drift is each coin's mean 5-bar return over all grid bars of all its windows; the regression is one OLS of excess return on post_pipeline_value pooled over all coins; fewer than 100 cases is reported as not observable.
- Size: unusual move -0.44 % per case over 5 bars, -0.050 of the coin's usual move (10.60 %); normal drift in its direction +0.58 %, total +0.13 %; 665 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines_1d`
Measure: `measure.py`
