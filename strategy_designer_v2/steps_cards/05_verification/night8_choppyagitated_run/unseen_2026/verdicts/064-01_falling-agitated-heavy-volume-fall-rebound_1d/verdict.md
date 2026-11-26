---
plan: 064-01_falling-agitated-heavy-volume-fall-rebound_1d
idea: 064-01_falling-agitated-heavy-volume-fall-rebound
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of excess next-day return on forecast, within windows: None (threshold: confirm: slope t >= 2 and mean excess > 0; reject: slope t <= -2 or mean excess t <= -2)
- Supporting check: mean excess next-day return > 0: None, passed: None
- Counts: distinct case days: 67, cases: 164
- Decided by: Only 67 distinct case days, fewer than the plan's 100.
- Reading: Situation profile taken from the recorded regime 'mean_reversion' (the detector's profile components are not recorded) with ret1 from closes and volume ratio from heavy_volume raw value + 1 (prices when missing); bars whose situation cannot be computed are left out; the slope uses forecast and excess return demeaned within each coin-window, and both t's use day-clustered standard errors (deviations summed per UTC day, factor G/(G-1)); the plan's 100 distinct case days is treated as the minimum count.
- Size: unusual move +0.47 % (t 0.33, the cases of one day together: 52 days) per case over 1 bars, 0.104 of the coin's usual move (3.93 %); normal drift in its direction -0.01 %, total +0.45 %; 104 cases
Plan: `steps_cards/03_test_plan/night8_choppyagitated_run/plans/064-01_falling-agitated-heavy-volume-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night8_choppyagitated_run/unseen_2026/backtests/064-01_falling-agitated-heavy-volume-fall-rebound_1d`
Measure: `measure.py`
