---
plan: 033-01_scaled-daily-fall-next-day-rebound_1d
idea: 033-01_scaled-daily-fall-next-day-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of next-day return minus drift against forecast, on forecast > 0: 0.000397677; slope t, day-clustered: 2.62632 (threshold: slope t (by day) >= 2 confirms (with supporting check); <= -2 rejects)
- Supporting check: forecast-weighted mean next-day excess return, t by day: 0.00349831, passed: True
- Counts: distinct days with forecast > 0: 2199, cases (coin-days with forecast > 0): 8514
- Decided by: Confirm rule met: the slope's t is >= 2 and the weighted mean excess return is > 0 with t >= 2.
- Reading: Every bar with forecast > 0 and a next close in its window is a case (1-bar horizon, so the grid is every bar), drift is the coin's mean next-day return over all its windows, both t's sum each day's contributions across coins into one cluster (with the G/(G-1) correction), and the plan's 'fewer than 300 days' is reported as not observable.
- Size: unusual move +0.18 % (t 1.45, the cases of one day together: 1702 days) per case over 1 bars, 0.038 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.30 %; 5636 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0002362 on the check folds against +0.0003977 on every fold
Plan: `steps_cards/03_test_plan/night7_chopreversal_run/plans/033-01_scaled-daily-fall-next-day-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_chopreversal_run/backtests/033-01_scaled-daily-fall-next-day-rebound_1d`
Measure: `measure.py`
