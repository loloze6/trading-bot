---
plan: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising_1d
idea: 022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: Mean 5-day excess return, top fifth of positive forecasts minus all other grid bars: 0.0204614; Welch t: 4.81835 (threshold: Welch t >= 2 confirms (with supporting check); Welch t <= -2 rejects)
- Supporting check: Top-fifth mean excess minus remaining positive-forecast mean excess: 0.0172113, passed: True
- Counts: top-fifth grid cases: 1747, other grid cases: 9220, remaining positive-forecast grid cases: 3371, positive-forecast grid cases: 5118
- Decided by: Welch t >= 2 (top fifth minus the rest) and the supporting check passes.
- Reading: The top fifth is the positive-forecast grid bars whose forecast is at or above the 80th percentile of positive grid forecasts (ties at the cut kept in the top group), the coin's mean 5-day return is taken over its non-overlapping grid in all windows, and the plan's minimum of 30 top-fifth cases gives 'not observable' when unmet.
- Size: unusual move +1.08 % (t 2.27, the cases of one day together: 1263 days) per case over 5 bars, 0.066 of the coin's usual move (12.26 %); normal drift in its direction +0.81 %, total +1.89 %; 3089 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/022-01_learned-combined-signal-score.d1_fixed-weight-combined-signal-score.d2_strong-rises-keep-rising_1d`
Measure: `measure.py`
