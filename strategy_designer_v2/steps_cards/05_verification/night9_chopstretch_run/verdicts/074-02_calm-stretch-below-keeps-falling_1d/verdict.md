---
plan: 074-02_calm-stretch-below-keeps-falling_1d
idea: 074-02_calm-stretch-below-keeps-falling
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS t of the slope of drift-removed next-10-bar return on the forecast, negative-forecast grid cells: 0.291446; OLS t of the slope: 0.291446 (threshold: t >= 2 confirms (with the supporting check), t <= -2 rejects, otherwise inconclusive; at least 100 cells)
- Supporting check: mean drift-removed 10-bar return in the signal's direction (short) > 0: 0.00960061, passed: True
- Counts: grid cells with a negative forecast: 445
- Decided by: The slope's t lies between -2 and 2.
- Reading: The calm market is read as the bars whose regime is 'unknown' (the detector's default, not vetoed to 'chop'), below the average as a raw stretch_below value under 0; the grid is pooled over all coins and windows, each coin's normal 10-bar drift is the mean of all its grid cells' 10-bar returns over all windows, the slope's t is the ordinary least-squares t of the pooled regression, and a count under the plan's 100-cell minimum is reported as 'not observable'.
- Size: unusual move +0.69 % (t 0.99, the cases of one day together: 392 days) per case over 10 bars, 0.050 of the coin's usual move (14.49 %); normal drift in its direction -1.30 %, total -0.61 %; 643 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/074-02_calm-stretch-below-keeps-falling_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/074-02_calm-stretch-below-keeps-falling_1d`
Measure: `measure.py`
