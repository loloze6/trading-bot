---
plan: 058-01.g2.b1.d1_raw-sized-one-day-rise-fade_1d
idea: 058-01.g2.b1.d1_raw-sized-one-day-rise-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move of short cases (short direction): 0.00431077; t of the mean, cases of one day taken together: 0.970977 (threshold: confirm if mean > 0 with t >= 2 (and supporting check passes); reject if mean < 0 with t <= -2)
- Supporting check: mean unusual move, forecast <= -10 minus forecast in [-10, -2]: 0.00214151, passed: True
- Counts: cases: 1137, distinct days: 430, cases with forecast <= -10: 595, cases with forecast between -2 and -10: 542
- Decided by: The t of the mean unusual move lies between -2 and 2.
- Reading: A case is the first short bet (forecast short size rising >= 2 from its lowest since the last bet) in each 3-bar grid cell of a window, its return taken from that bar's close 3 bars ahead within the window, groups split on the case bar's forecast (<= -10 vs > -10 and <= -2), and the day-clustered standard error is sqrt(sum of squared per-day summed deviations) / number of cases; the profile is the recorded regime 'unknown'.
- Size: unusual move +0.43 % (t 0.97, the cases of one day together: 430 days) per case over 3 bars, 0.049 of the coin's usual move (8.85 %); normal drift in its direction -0.43 %, total -0.00 %; 1137 cases
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.b1.d1_raw-sized-one-day-rise-fade_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.b1.d1_raw-sized-one-day-rise-fade_1d`
Measure: `measure.py`
