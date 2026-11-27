---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of demeaned 3-bar forward return on volratio, trending grid bars: 0.00811052; OLS t of slope: 5.41615 (threshold: confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; at least 100 grid cases)
- Supporting check: none
- Counts: trending-regime grid cases: 8565
- Decided by: The slope is positive with t = 5.42 >= 2 from 8565 grid cases (confirm rule).
- Reading: The situation is a 30-bar close-to-close return above 0 recomputed inside each window (active bars in a window's first 30 bars, where it cannot be computed, are left out unless no other active bar exists, then the recorded regime is used), the expected side is long; the main sample is bars with recorded regime 'trending' on each window's 0,3,6,... grid, and the coin's mean 3-bar return is taken over the same grid on all bars of all its windows.
- Size: unusual move +0.34 % (t 1.62, the cases of one day together: 2221 days) per case over 3 bars, 0.034 of the coin's usual move (9.27 %); normal drift in its direction +0.48 %, total +0.81 %; 7274 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/volume_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d.md`
Record: `steps_cards/04_backtest/paying_rerun_run/common/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d`
Measure: `measure.py`
