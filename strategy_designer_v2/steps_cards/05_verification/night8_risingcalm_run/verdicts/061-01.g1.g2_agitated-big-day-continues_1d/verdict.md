---
plan: 061-01.g1.g2_agitated-big-day-continues_1d
idea: 061-01.g1.g2_agitated-big-day-continues
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of demeaned 5-bar forward return on forecast: -0.000625871; slope t (day-clustered): -1.49446 (threshold: slope > 0 with t >= 2 (confirm), slope < 0 with t <= -2 (reject), on at least 100 cases)
- Supporting check: none
- Counts: non-overlapping cases with a non-zero forecast: 1519, days: 455
- Decided by: The slope's t lies between -2 and 2 (inconclusive rule).
- Reading: Agitated profile read as regime != 'chop'; the forecast is regressed with an intercept, and 'cases of one day summed together' is read as a day-clustered standard error (each day's score contributions summed, G/(G-1) correction); the coin mean is over its non-overlapping 5-bar grid returns of all windows.
- Size: unusual move -0.49 % (t -1.19, the cases of one day together: 819 days) per case over 5 bars, -0.052 of the coin's usual move (10.60 %); normal drift in its direction -0.02 %, total -0.51 %; 1685 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/061-01.g1.g2_agitated-big-day-continues_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.g2_agitated-big-day-continues_1d`
Measure: `measure.py`
