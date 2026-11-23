---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast, heavy-volume days: 0.00127958; OLS t of slope: 4.8314 (threshold: confirm: slope positive with t >= 2; reject: slope negative with t <= -2)
- Supporting check: mean next-day excess return, lowest-quarter minus other heavy days (Welch t >= 2): 0.0180543, passed: True
- Counts: heavy-volume days: 1616, lowest-quarter days: 409, other heavy-volume days: 1207
- Decided by: Confirm: the slope is positive with t >= 2 and lowest-quarter days beat the other heavy days with Welch t >= 2.
- Reading: The volume ratio is recomputed inside each window as volume over the mean of the 20 prior bars, so active bars with fewer than 20 prior bars in their window are left out of the agreement; heavy-volume days are the bars with regime mean_reversion and a next-day return in the same window; the coin's mean daily return is over all its 1-day returns in all windows; the slope's t is the OLS slope over its standard error; the 'other heavy-volume days' are heavy days with loc_low post_pipeline_value below 8.4; the minimum counts make the result 'not observable' when not reached. Welch t = 4.923.
- Size: unusual move +0.70 % per case over 1 bars, 0.152 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.82 %; 783 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d`
Measure: `measure.py`
