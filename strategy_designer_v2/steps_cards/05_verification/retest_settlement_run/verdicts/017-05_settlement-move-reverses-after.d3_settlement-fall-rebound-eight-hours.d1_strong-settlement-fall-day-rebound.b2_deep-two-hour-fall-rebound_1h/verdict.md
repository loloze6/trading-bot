---
plan: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound_1h
idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 24-bar return on forecast (post_pipeline_value): 0.000321319; OLS slope t: 3.80584 (threshold: slope > 0 with t >= 2 (and top-quintile mean > 0) confirms; slope < 0 with t <= -2 rejects)
- Supporting check: top-quintile mean excess 24-bar return, long: 0.00598711, passed: True
- Counts: cases pooled: 8707, cases in the top quintile: 1742
- Decided by: The slope is positive with t >= 2 and the top-quintile mean excess return is above 0.
- Reading: The drift is each coin's mean 24-bar return over the non-overlapping grid of all its windows, the top quintile is the cases with post_pipeline_value at or above the 80th percentile of the pooled cases, and the plan's minimum counts, if missed, give 'not observable' as the workflow requires.
- Size: unusual move +0.01 % per case over 24 bars, 0.001 of the coin's usual move (4.87 %); normal drift in its direction +0.14 %, total +0.15 %; 17241 cases
Plan: `steps_cards/03_test_plan/retest_settlement_run/plans/017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound_1h.md`
Record: `steps_cards/04_backtest/retest_settlement_run/backtests/017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound_1h`
Measure: `measure.py`
