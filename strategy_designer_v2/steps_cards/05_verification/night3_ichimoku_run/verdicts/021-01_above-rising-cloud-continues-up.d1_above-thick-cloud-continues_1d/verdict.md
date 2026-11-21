---
plan: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues_1d
idea: 021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 26-bar excess return on recorded forecast: -0.00827817; OLS slope t: -1.25962 (threshold: slope > 0 with t >= 2 confirms; slope < 0 with t <= -2 rejects; on at least 30 cases)
- Supporting check: width coefficient minus slope coefficient (standardised joint regression): None, passed: None
- Counts: independent in-regime cases: 149, supporting check cases: 0
- Decided by: The forecast slope's t lies between -2 and 2.
- Reading: The cloud position and 26-bar cloud slope are recomputed from each window's prices with the standard Ichimoku spans displaced 26 bars (falling back to the recorded regime on bars too early in a window to recompute them); in-regime cases are grid bars whose recorded regime is 'trending'; the supporting check z-scores width and slope across its cases and compares their OLS coefficients, using only cases where the slope can be recomputed; fewer than 30 cases gives 'not observable'.
- Size: unusual move +3.25 % per case over 26 bars, 0.093 of the coin's usual move (25.48 %); normal drift in its direction +3.88 %, total +7.13 %; 237 cases
Plan: `steps_cards/03_test_plan/night3_ichimoku_run/plans/021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues_1d.md`
Record: `steps_cards/04_backtest/night3_ichimoku_run/backtests/021-01_above-rising-cloud-continues-up.d1_above-thick-cloud-continues_1d`
Measure: `measure.py`
