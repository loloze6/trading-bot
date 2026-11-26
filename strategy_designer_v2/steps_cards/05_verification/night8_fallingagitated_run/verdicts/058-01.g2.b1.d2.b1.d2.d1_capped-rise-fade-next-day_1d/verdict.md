---
plan: 058-01.g2.b1.d2.b1.d2.d1_capped-rise-fade-next-day_1d
idea: 058-01.g2.b1.d2.b1.d2.d1_capped-rise-fade-next-day
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day unusual move in the short direction: 0.00529898; t of the mean, cases of one day summed: 2.03989 (threshold: mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects)
- Supporting check: OLS slope of the short unusual move on |forecast|: 0.000267987, passed: True
- Counts: distinct days with cases: 519, cases: 1283
- Decided by: the mean unusual move is positive with t >= 2 and the slope on forecast size is above 0
- Reading: a case is a short bet as the workflow defines it (a rise of the short forecast of at least 2 points from its lowest level since the last bet, every bar being a 1-bar grid cell), forecast size is |forecast|, the day-clustered standard error uses a G/(G-1) correction, the 30-day minimum maps to 'not observable', and the situation check uses the rise condition and short side only since the profile components are not recorded
- Size: unusual move +0.53 % (t 2.04, the cases of one day together: 519 days) per case over 1 bars, 0.108 of the coin's usual move (5.33 %); normal drift in its direction -0.14 %, total +0.39 %; 1283 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.003237 on the check folds against +0.005299 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingagitated_run/plans/058-01.g2.b1.d2.b1.d2.d1_capped-rise-fade-next-day_1d.md`
Record: `steps_cards/04_backtest/night8_fallingagitated_run/backtests/058-01.g2.b1.d2.b1.d2.d1_capped-rise-fade-next-day_1d`
Measure: `measure.py`
