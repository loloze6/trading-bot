---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast, heavy-volume days: -7.68492e-06; OLS t of slope: -0.00868579 (threshold: confirm: slope positive with t >= 2; reject: slope negative with t <= -2)
- Supporting check: mean next-day excess return, lowest-quarter minus other heavy days (Welch t >= 2): -0.0132773, passed: False
- Counts: heavy-volume days: 367, lowest-quarter days: 67, other heavy-volume days: 300
- Decided by: Inconclusive: the results meet neither the confirm rule (slope t >= 2 with the supporting check passed) nor a reject rule (slope t <= -2 or Welch t <= -2).
- Reading: The volume ratio is recomputed inside each window as volume over the mean of the 20 prior bars, so active bars with fewer than 20 prior bars in their window are left out of the agreement; heavy-volume days are the bars with regime mean_reversion and a next-day return in the same window; the coin's mean daily return is over all its 1-day returns in all windows; the slope's t is the OLS slope over its standard error; the 'other heavy-volume days' are heavy days with loc_low post_pipeline_value below 8.4; the minimum counts make the result 'not observable' when not reached. Welch t = -1.233.
- Size: unusual move +0.82 % per case over 1 bars, 0.101 of the coin's usual move (7.55 %); normal drift in its direction +0.93 %, total +1.75 %; 149 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/unseen_2016_2017/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d`
Measure: `measure.py`
