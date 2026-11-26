---
plan: 035-03.b1_choppy-far-below-high-falls_1d
idea: 035-03.b1_choppy-far-below-high-falls
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean excess 5-bar fall of short bets vs coin's normal drift: 0.00882686; t of the mean, cases of one day taken together: 2.46608 (threshold: confirm: mean > 0 with t >= 2 and supporting check passed; reject: mean < 0 with t <= -2)
- Supporting check: mean excess fall of cases with |forecast| above median minus at/below median: -0.00296966, passed: False
- Counts: independent case days across coins and windows: 827, cases: 1461
- Decided by: t >= 2 but the supporting check failed, which the plan calls inconclusive.
- Reading: A case is the first short bet (forecast deepening >= 2 points below 0 from its lowest size since the last bet) in each non-overlapping 5-bar grid cell of a window, its 5-bar return taken from that bar's close, drift is the coin's mean grid 5-bar return over all windows, the day-clustered t uses a D/(D-1) correction, and the situation's choppy profile is the 60-bar percent change within +-10, untested where fewer than 60 window bars precede the bar.
- Size: unusual move +0.88 % (t 2.47, the cases of one day together: 827 days) per case over 5 bars, 0.067 of the coin's usual move (12.35 %); normal drift in its direction -0.80 %, total +0.08 %; 1461 cases
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/035-03.b1_choppy-far-below-high-falls_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/035-03.b1_choppy-far-below-high-falls_1d`
Measure: `measure.py`
