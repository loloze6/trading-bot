---
plan: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising_1d
idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: Mean 5-day excess return, top fifth of positive forecasts minus all other grid bars: 0.0439111; Welch t: 2.32814 (threshold: Welch t >= 2 confirms (with supporting check); Welch t <= -2 rejects)
- Supporting check: Top-fifth mean excess minus remaining positive-forecast mean excess: 0.0318718, passed: True
- Counts: top-fifth grid cases: 161, other grid cases: 411, remaining positive-forecast grid cases: 218, positive-forecast grid cases: 379
- Decided by: Welch t >= 2 (top fifth minus the rest) and the supporting check passes.
- Reading: The top fifth is the positive-forecast grid bars whose forecast is at or above the 80th percentile of positive grid forecasts (ties at the cut kept in the top group), the coin's mean 5-day return is taken over its non-overlapping grid in all windows, and the plan's minimum of 30 top-fifth cases gives 'not observable' when unmet.
- Size: unusual move +2.07 % per case over 5 bars, 0.088 of the coin's usual move (18.32 %); normal drift in its direction +4.71 %, total +6.78 %; 214 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/unseen_2016_2017/backtests/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising_1d`
Measure: `measure.py`
