---
plan: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise_1d
idea: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the OLS slope of excess 5-day return on forecast: 3.00384; OLS slope t: 3.00384 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2; at least 50 grid cases)
- Supporting check: none
- Counts: grid cases with a forecast above 0: 852
- Decided by: The slope is positive with t >= 2: excess 5-day returns grow with cloud thinness.
- Reading: Situation recomputed from each window's recorded prices (close above max(spanA, spanB), 26-bar percent change of the cloud mid > 0); on active bars too early in a window for the Ichimoku lines to be computed, the recorded regime ('trending') stands in for the detector; the plan's 'fewer than 50 grid cases' minimum is reported as 'not observable'; the coin's normal 5-day drift is the mean of its non-overlapping 5-bar grid returns over all windows; the slope's t is the ordinary OLS t (slope / its standard error).
- Size: unusual move +1.28 % per case over 5 bars, 0.119 of the coin's usual move (10.60 %); normal drift in its direction +0.57 %, total +1.85 %; 476 cases
Plan: `steps_cards/03_test_plan/night3_ichimoku_run/plans/021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise_1d.md`
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues.b1_thin-cloud-short-rise_1d`
Measure: `measure.py`
