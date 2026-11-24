---
plan: 033-03_downside-break-continues-falling_1d
idea: 033-03_downside-break-continues-falling
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar fall of short bets (return minus coin's mean 5-bar return, short direction): 0.00775672; t of the mean, cases on the same day pooled: 0.668928 (threshold: confirm: mean > 0 with t >= 2 and supporting check passes; reject: mean < 0 with t <= -2; at least 30 cases on at least 30 distinct days)
- Supporting check: mean excess fall of cases with |forecast| above median minus below median: 0.0163577, passed: True
- Counts: cases: 232, distinct days: 114
- Decided by: The t lies between -2 and 2, which the plan calls inconclusive.
- Reading: A case is a short bet (a rise of the forecast's size of at least 2 points from its lowest level since the last bet, from 0 after a flat), the first in each non-overlapping 5-bar grid cell from each window's first row, returned from its own close over 5 bars inside the window; the drift is the coin's mean return on the 5-bar grid of all its windows; the same-day t sums deviations per UTC day with a G/(G-1) correction; cases exactly at the median |forecast| are left out of the supporting check; the situation uses the recorded raw value, recomputed from prices where missing.
- Size: unusual move +0.78 % (t 0.67, the cases of one day together: 114 days) per case over 5 bars, 0.076 of the coin's usual move (10.60 %); normal drift in its direction -0.58 %, total +0.20 %; 232 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/033-03_downside-break-continues-falling_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/033-03_downside-break-continues-falling_1d`
Measure: `measure.py`
