---
plan: 061-01_calm-big-up-day-continues_1d
idea: 061-01_calm-big-up-day-continues
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of 5-bar excess return on forecast, day-clustered t: 0.000901481; slope t (day-clustered): 3.01248 (threshold: confirm if slope t >= 2 (100+ cases) and largest |forecast| third above smallest; reject if t <= -2 (100+ cases))
- Supporting check: mean directional excess 5-bar return, largest |forecast| third minus smallest third: 0.00693946, passed: True
- Counts: non-overlapping cases inside the calm profile: 1827, days: 483
- Decided by: Slope t >= 2 with at least 100 cases and the largest |forecast| third above the smallest third.
- Reading: Calm profile read as regime 'unknown' (no 'chop' veto) and the day's direction as the sign of the raw component (price return where missing); the slope t uses OLS with residual-score deviations summed per day (cluster-robust, G/(G-1) correction); the coin's mean 5-bar return is over all grid bars of all its windows; thirds are floor(n/3) cases at each end of |forecast|.
- Size: unusual move +0.94 % (t 3.08, the cases of one day together: 903 days) per case over 5 bars, 0.088 of the coin's usual move (10.60 %); normal drift in its direction -0.01 %, total +0.93 %; 1965 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0005111 on the check folds against +0.0009015 on every fold
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/061-01_calm-big-up-day-continues_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01_calm-big-up-day-continues_1d`
Measure: `measure.py`
