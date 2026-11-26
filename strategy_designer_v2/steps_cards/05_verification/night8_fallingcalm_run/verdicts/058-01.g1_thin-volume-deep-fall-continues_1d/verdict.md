---
plan: 058-01.g1_thin-volume-deep-fall-continues_1d
idea: 058-01.g1_thin-volume-deep-fall-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of next 5-bar excess return on forecast (nonzero-forecast grid cells): 0.000844189; OLS slope t: 1.21971 (threshold: slope t >= 2 with check passing confirms; slope t <= -2 rejects)
- Supporting check: mean of minus excess 5-bar return on cells with forecast <= -2: 0.00492255, passed: True
- Counts: grid cells with a nonzero forecast: 444, grid cells with forecast <= -2: 393
- Decided by: The slope's t is between -2 and 2, which the plan calls inconclusive.
- Reading: Cells from all coins are pooled into one OLS regression of the excess return on the forecast, with the coin's mean 5-bar return taken over the same non-overlapping grid of all its windows; the plan's minimum of 100 nonzero cells is treated as a minimum count, so missing it gives 'not observable'; and the supporting check fails when no cell has a forecast of -2 or below.
- Size: unusual move +0.88 % (t 1.49, the cases of one day together: 307 days) per case over 5 bars, 0.082 of the coin's usual move (10.60 %); normal drift in its direction -0.68 %, total +0.21 %; 438 cases
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/058-01.g1_thin-volume-deep-fall-continues_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/058-01.g1_thin-volume-deep-fall-continues_1d`
Measure: `measure.py`
