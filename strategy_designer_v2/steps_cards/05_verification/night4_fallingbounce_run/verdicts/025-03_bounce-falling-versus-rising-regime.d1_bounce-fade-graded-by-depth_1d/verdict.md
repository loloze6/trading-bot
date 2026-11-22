---
plan: 025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth_1d
idea: 025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: Welch t of 5-day return, rising-coin rises (A) minus forecast-negative bars (B): 0.0613492; Welch t: 1.96039 (threshold: confirm if t >= 2 with supporting slope > 0; reject if t <= -2; at least 30 cases per group)
- Supporting check: slope of short-signed 5-day return minus drift on |forecast|, group B: -0.00482432, passed: False
- Counts: group A (rise bars with positive 90-day return): 7, group B (bars with negative forecast): 24
- Decided by: A group has fewer than 30 cases (A: 7, B: 24), the plan's minimum.
- Reading: Situation recomputed from prices (1-day return over the std of the last 20 daily returns including the bar, 90-day close-to-close return inside the window), falling back to the recorded regime where the 90-day history is not inside the window; group B is the grid bars with forecast < 0; the supporting y is -(5-day return - coin's mean non-overlapping 5-day return over all windows); a group under 30 cases is 'not observable'.
- Size: unusual move +1.08 % per case over 5 bars, 0.107 of the coin's usual move (10.60 %); normal drift in its direction -0.59 %, total +0.49 %; 92 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/backtests/025-03_bounce-falling-versus-rising-regime.d1_bounce-fade-graded-by-depth_1d`
Measure: `measure.py`
