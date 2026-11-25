---
plan: 037-01_falling-market-wide-day-decline_1d
idea: 037-01_falling-market-wide-day-decline
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 3-bar move in the short direction: -0.00521537; t of the mean, same-day cases summed: -1.11873 (threshold: confirm: mean > 0 with t >= 2 (and supporting check passes); reject: t <= -2)
- Supporting check: mean unusual move of wider half minus narrower half (split at median |forecast|): -0.00236454, passed: False
- Counts: cases: 870, distinct days: 456
- Decided by: The t of the mean unusual move lies between -2 and 2 (inconclusive rule).
- Reading: The situation is a range/30-day-return-std ratio of at least 2.0 (recorded raw value, else recomputed) with a 60-bar price change below -10 % on a short forecast, judged on the active bars where the 60-bar change can be computed inside the window; a case is the first short bet (rise of |forecast| of at least 2 from its lowest level since the last bet) in each 3-bar grid cell of a window, its return taken from that bar's close; the drift is the coin's mean 3-bar return on the grid of all its windows; the t sums the deviations per UTC day with a D/(D-1) correction; the wider half is |forecast| above the case median, the narrower half at or below it; the plan's minimum of 30 cases and 30 distinct days is applied as 'not observable'.
- Size: unusual move -0.52 % (t -1.12, the cases of one day together: 456 days) per case over 3 bars, -0.064 of the coin's usual move (7.96 %); normal drift in its direction -0.37 %, total -0.89 %; 870 cases
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/037-01_falling-market-wide-day-decline_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/037-01_falling-market-wide-day-decline_1d`
Measure: `measure.py`
