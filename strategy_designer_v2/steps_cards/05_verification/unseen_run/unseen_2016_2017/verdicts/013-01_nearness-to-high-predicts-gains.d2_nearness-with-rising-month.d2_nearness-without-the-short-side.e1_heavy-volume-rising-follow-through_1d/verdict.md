---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of demeaned 3-bar forward return on volratio, trending grid bars: 0.00992107; OLS t of slope: 1.47365 (threshold: confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; at least 100 grid cases)
- Supporting check: none
- Counts: trending-regime grid cases: 644
- Decided by: The slope's t = 1.47 lies between -2 and +2 (inconclusive rule).
- Reading: The situation is a 30-bar close-to-close return above 0 recomputed inside each window (active bars in a window's first 30 bars, where it cannot be computed, are left out unless no other active bar exists, then the recorded regime is used), the expected side is long; the main sample is bars with recorded regime 'trending' on each window's 0,3,6,... grid, and the coin's mean 3-bar return is taken over the same grid on all bars of all its windows.
Plan: `steps_cards/03_test_plan/volume_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d.md`
Record: `steps_cards/04_backtest/unseen_run/unseen_2016_2017/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d`
Measure: `measure.py`
