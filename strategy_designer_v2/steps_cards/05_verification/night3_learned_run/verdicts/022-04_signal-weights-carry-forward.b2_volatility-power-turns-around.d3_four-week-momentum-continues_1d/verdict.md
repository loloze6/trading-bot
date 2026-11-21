---
plan: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues_1d
idea: 022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of demeaned 5-bar forward return on forecast: 0.000343736; OLS t of slope: 2.0745 (threshold: confirm: slope > 0 with t >= 2 (and timing gain > 0); reject: slope < 0 with t <= -2)
- Supporting check: book timing gain (mean daily return before costs minus market-rise gain): 0.000788561, passed: True
- Counts: non-overlapping cases: 3419
- Decided by: The slope is positive with t >= 2 and the timing gain is above 0.
- Reading: The regression is ordinary least squares with an intercept on all grid bars (positions 0,5,10,... with close[t+5] in the window), the coin mean is the mean of its grid 5-bar returns over all windows, and the book is the daily mean over coins of postRebalance_current_allocation x next-bar return, per window and day.
- Size: unusual move +0.51 % per case over 5 bars, 0.043 of the coin's usual move (10.60 %); normal drift in its direction -0.01 %, total +0.50 %; 2452 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-04_signal-weights-carry-forward.b2_volatility-power-turns-around.d3_four-week-momentum-continues_1d`
Measure: `measure.py`
