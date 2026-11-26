---
plan: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound_1h
idea: 017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 24-bar return on forecast (post_pipeline_value): None (threshold: slope > 0 with t >= 2 (and top-quintile mean > 0) confirms; slope < 0 with t <= -2 rejects)
- Supporting check: top-quintile mean excess 24-bar return, long: 0.00714322, passed: True
- Counts: cases pooled: 1157, cases in the top quintile: 1157
- Decided by: The slope or its t could not be computed, so neither the confirm nor the reject rule is met.
- Reading: The drift is each coin's mean 24-bar return over the non-overlapping grid of all its windows, the top quintile is the cases with post_pipeline_value at or above the 80th percentile of the pooled cases, and the plan's minimum counts, if missed, give 'not observable' as the workflow requires.
- Size: unusual move +0.04 % per case over 24 bars, 0.005 of the coin's usual move (4.87 %); normal drift in its direction +0.14 %, total +0.18 %; 9828 cases
Plan: `steps_cards/03_test_plan/book_reflects_idea_run/plans/017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound_1h.md`
Record: `steps_cards/04_backtest/book_reflects_idea_run/backtests/017-05_settlement-move-reverses-after.d3_settlement-fall-rebound-eight-hours.d1_strong-settlement-fall-day-rebound.b2_deep-two-hour-fall-rebound_1h`
Measure: `measure.py`
