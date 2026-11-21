---
plan: 020-01_resistance-retest-turns-down.d2_thirty-day-momentum-continues_1d
idea: 020-01_resistance-retest-turns-down.d2_thirty-day-momentum-continues
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of de-drifted 5-bar forward return on the forecast (pooled, non-overlapping grid): 0.000385566; OLS t of the slope: 2.354 (threshold: t >= 2 confirms (with timing gain > 0); t <= -2 rejects; at least 300 grid cases)
- Supporting check: book's mean daily return before costs minus its gain from the market's rise: 0.00076836, passed: True
- Counts: non-overlapping grid cases with a recorded forecast: 3419
- Decided by: Confirm: the slope's t is 2 or more and the book's timing gain is above 0.
- Reading: Grid bars are positions 0,5,10,... of each window with a full 5-bar return inside it, the drift is each coin's mean grid return over all its windows, zero forecasts count as recorded, and the book is position x next-bar return averaged over coins per day with fewer than 300 cases treated as not observable.
- Size: unusual move +0.58 % per case over 5 bars, 0.048 of the coin's usual move (10.60 %); normal drift in its direction -0.02 %, total +0.56 %; 2409 cases
Plan: `steps_cards/03_test_plan/night3_levels_run/plans/020-01_resistance-retest-turns-down.d2_thirty-day-momentum-continues_1d.md`
Record: `steps_cards/04_backtest/night3_levels_run/backtests/020-01_resistance-retest-turns-down.d2_thirty-day-momentum-continues_1d`
Measure: `measure.py`
