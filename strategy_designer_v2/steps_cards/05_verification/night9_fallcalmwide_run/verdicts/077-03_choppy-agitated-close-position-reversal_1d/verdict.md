---
plan: 077-03_choppy-agitated-close-position-reversal_1d
idea: 077-03_choppy-agitated-close-position-reversal
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next-day excess return on forecast: 0.000348263; slope t, clustered by day: 2.514 (threshold: t >= 2 (with supporting check) confirms; t <= -2 rejects; between is inconclusive)
- Supporting check: mean next-day excess return in forecast direction, top third |forecast|: 0.00551037, passed: True
- Counts: in-position bars: 2193, distinct days: 1065, bars with non-zero forecast (regression cases): 2278, top-third bars: 731
- Decided by: The slope's t is 2 or more and the top-third mean directional excess return is above 0.
- Reading: In-position bars are bars with a non-zero postRebalance_current_allocation and a next-day return in the same window; the top third is the n//3 largest |forecast| among them; the slope is OLS with an intercept on non-zero-forecast bars, its t from day-clustered (sandwich, G/(G-1)*(n-1)/(n-2)) standard errors; the coin's mean daily return uses all its in-window close-to-close returns.
- Size: unusual move +0.36 % (t 2.19, the cases of one day together: 883 days) per case over 1 bars, 0.076 of the coin's usual move (5.33 %); normal drift in its direction -0.00 %, total +0.36 %; 1579 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0001479 on the check folds against +0.0003483 on every fold
Plan: `steps_cards/03_test_plan/night9_fallcalmwide_run/plans/077-03_choppy-agitated-close-position-reversal_1d.md`
Record: `steps_cards/04_backtest/night9_fallcalmwide_run/backtests/077-03_choppy-agitated-close-position-reversal_1d`
Measure: `measure.py`
