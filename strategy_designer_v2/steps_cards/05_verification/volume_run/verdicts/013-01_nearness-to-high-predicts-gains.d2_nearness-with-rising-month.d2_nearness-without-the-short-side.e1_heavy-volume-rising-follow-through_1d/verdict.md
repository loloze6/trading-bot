---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of demeaned 3-bar forward return on volratio, trending grid bars: 0.00633208; OLS t of slope: 2.74505 (threshold: confirm if slope > 0 with t >= 2; reject if slope < 0 with t <= -2; at least 100 grid cases)
- Supporting check: none
- Counts: trending-regime grid cases: 2840
- Decided by: The slope is positive with t = 2.75 >= 2 from 2840 grid cases (confirm rule).
- Reading: The situation is a 30-bar close-to-close return above 0 recomputed inside each window (active bars in a window's first 30 bars, where it cannot be computed, are left out unless no other active bar exists, then the recorded regime is used), the expected side is long; the main sample is bars with recorded regime 'trending' on each window's 0,3,6,... grid, and the coin's mean 3-bar return is taken over the same grid on all bars of all its windows.
Plan: `steps_cards/03_test_plan/volume_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d.md`
Record: `steps_cards/04_backtest/volume_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d`
Measure: `measure.py`
