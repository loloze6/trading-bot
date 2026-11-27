---
plan: 064-01.g1_calm-decline-up-day-fade_1d
idea: 064-01.g1_calm-decline-up-day-fade
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean position-weighted 3-bar fade beyond drift (cases summed per day): 0.000309472; t of the mean (per-day sums): 0.0679641 (threshold: confirm t >= 2 (with slope > 0); reject t <= -2)
- Supporting check: OLS slope of -(unusual 3-bar return) on forecast size: 0.000907198, passed: True
- Counts: independent cases (distinct days): 268, cases: 534
- Decided by: Inconclusive: the main t is between -2 and 2 and no reject rule is met.
- Reading: Profile membership read from the recorded regime; cases are grid bars (0,3,6,... of each window) with forecast < 0 and a close 3 bars later in the same window; the main value is the mean per case and its t is the ordinary t of the per-day sums; the slope is on |forecast|, with its t from OLS; fewer than 30 distinct days is treated as not observable.
- Size: unusual move -0.02 % (t -0.05, the cases of one day together: 483 days) per case over 3 bars, 0.001 of the coin's usual move (7.96 %); normal drift in its direction -0.39 %, total -0.41 %; 838 cases
Plan: `steps_cards/03_test_plan/night9_fallcalmfade_run/plans/064-01.g1_calm-decline-up-day-fade_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmfade_run/backtests/064-01.g1_calm-decline-up-day-fade_1d`
Measure: `measure.py`
