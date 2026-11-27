---
plan: 061-01.b1.b1.b1.d2.d3.d3_broad-pullback-high-close-fade_1d
idea: 061-01.b1.b1.b1.d2.d3.d3_broad-pullback-high-close-fade
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 5-bar move of short cases (return minus coin drift, signed short): 0.00427726; t of the mean, cases clustered by day: 0.907126 (threshold: t >= 2 confirms (with supporting check), t <= -2 rejects, otherwise inconclusive; at least 30 case-days)
- Supporting check: mean unusual move, larger half of |forecast| minus smaller half: 0.000375328, passed: True
- Counts: case-days: 647, cases: 1333
- Decided by: Main measure t between -2 and 2 (inconclusive rule).
- Reading: Situation computed from prices as close location (close-low)/(high-low) >= 0.75, close above prior close, and close[t-1] < close[t-6] inside each window, with active bars whose situation cannot be computed (window start) left out of the agreement; cases are short bets (forecast falling by at least 2 points below its lowest short level since the last bet, from 0 after a flat), the first bet of each 5-bar grid cell per window; drift is the coin's mean non-overlapping 5-bar return over all its windows; the t clusters deviations by UTC day; the halves split the cases sorted by |forecast| at the signal bar into the top and bottom n//2 (the middle case dropped when n is odd); fewer than 30 case-days gives 'not observable' as the workflow requires.
- Size: unusual move +0.43 % (t 0.91, the cases of one day together: 647 days) per case over 5 bars, 0.030 of the coin's usual move (12.35 %); normal drift in its direction -0.82 %, total -0.39 %; 1333 cases
Plan: `steps_cards/03_test_plan/night9_chopagishort_run/plans/061-01.b1.b1.b1.d2.d3.d3_broad-pullback-high-close-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopagishort_run/backtests/061-01.b1.b1.b1.d2.d3.d3_broad-pullback-high-close-fade_1d`
Measure: `measure.py`
