---
plan: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.d1_breakout-above-rising-trend_1d
idea: 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.d1_breakout-above-rising-trend
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 20-bar unusual move of the cases (return minus coin's normal 20-bar drift), before costs: 0.0137321; one-group t: 0.947593 (threshold: mean > 0 with t >= 2 over at least 30 cases (confirm); mean < 0 with t <= -2 over at least 30 cases (reject))
- Supporting check: upper-half minus lower-half mean unusual move, split at median entry forecast: -0.0277999, passed: False
- Counts: cases: 507
- Decided by: The t lies between -2 and 2 over at least 30 cases, which the plan calls inconclusive.
- Reading: The situation is read from the recorded raw rb and ma values (both > 0, long side); a case is the first bet (forecast rise of >= 2 points from its lowest level on its side since the last bet, from 0 after a flat or side change) in each 20-bar grid cell counted from each window's first row, dropped if its 20-bar return leaves the window; the median split ranks cases by entry forecast and takes the lower and upper floor(n/2), leaving out the middle case when n is odd.
- Size: unusual move +1.37 % per case over 20 bars, 0.036 of the coin's usual move (21.24 %); normal drift in its direction +2.44 %, total +3.81 %; 507 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.d1_breakout-above-rising-trend_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.e1_resistance-break-weeks-long-continuation.d1_breakout-above-rising-trend_1d`
Measure: `measure.py`
