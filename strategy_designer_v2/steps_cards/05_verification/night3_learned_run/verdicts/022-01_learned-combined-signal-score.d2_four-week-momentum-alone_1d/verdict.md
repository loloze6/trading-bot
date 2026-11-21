---
plan: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone_1d
idea: 022-01_learned-combined-signal-score.d2_four-week-momentum-alone
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x (5-day return minus coin's normal drift), non-overlapping 5-bar grid, before costs: 0.00446863; ordinary t of the mean: 1.95212 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2; at least 300 grid cases with a non-zero forecast)
- Supporting check: none
- Counts: grid cases with a non-zero forecast: 3419, grid cases: 3419
- Decided by: Inconclusive rule met: -2 < t < 2 with at least 300 grid cases with a non-zero forecast.
- Reading: The mean and t are taken over every grid cell (bars 0, 5, 10, ... of each window with a 5-bar return inside it, zero-forecast cells contributing 0), the normal drift is each coin's mean 5-bar return over that grid in all its windows, and the 300 minimum is counted on grid cells with a non-zero forecast.
- Size: unusual move +0.51 % per case over 5 bars, 0.043 of the coin's usual move (10.60 %); normal drift in its direction -0.01 %, total +0.50 %; 2452 cases
Plan: `steps_cards/03_test_plan/night3_learned_run/plans/022-01_learned-combined-signal-score.d2_four-week-momentum-alone_1d.md`
Record: `steps_cards/04_backtest/night3_learned_run/backtests/022-01_learned-combined-signal-score.d2_four-week-momentum-alone_1d`
Measure: `measure.py`
