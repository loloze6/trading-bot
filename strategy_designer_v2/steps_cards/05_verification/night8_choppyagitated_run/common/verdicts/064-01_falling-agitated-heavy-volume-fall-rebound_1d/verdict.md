---
plan: 064-01_falling-agitated-heavy-volume-fall-rebound_1d
idea: 064-01_falling-agitated-heavy-volume-fall-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess next-day return on forecast, within windows: 0.00143801; slope t, day-clustered: 3.18382 (threshold: confirm: slope t >= 2 and mean excess > 0; reject: slope t <= -2 or mean excess t <= -2)
- Supporting check: mean excess next-day return > 0 (t day-clustered: 2.498): 0.00878482, passed: True
- Counts: distinct case days: 515, cases: 1440
- Decided by: Confirm rule met: slope t 3.18 >= 2 and mean excess 0.00878 > 0.
- Reading: Situation profile taken from the recorded regime 'mean_reversion' (the detector's profile components are not recorded) with ret1 from closes and volume ratio from heavy_volume raw value + 1 (prices when missing); bars whose situation cannot be computed are left out; the slope uses forecast and excess return demeaned within each coin-window, and both t's use day-clustered standard errors (deviations summed per UTC day, factor G/(G-1)); the plan's 100 distinct case days is treated as the minimum count.
- Size: unusual move +0.99 % (t 2.43, the cases of one day together: 411 days) per case over 1 bars, 0.212 of the coin's usual move (5.12 %); normal drift in its direction +0.12 %, total +1.11 %; 1011 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/064-01_falling-agitated-heavy-volume-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/common/backtests/064-01_falling-agitated-heavy-volume-fall-rebound_1d`
Measure: `measure.py`
