---
plan: 039-02_range-scaled-fall-rebound_1d
idea: 039-02_range-scaled-fall-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of next-day excess return on forecast, down-day bars: 0.000434148; OLS slope t, day-clustered: 2.86472 (threshold: confirm: slope > 0 with day-clustered t >= 2 (and top-quintile mean > 0); reject: slope < 0 with t <= -2)
- Supporting check: mean next-day excess return, top quintile of forecast on down-day bars: 0.00617302, passed: True
- Counts: down-day cases: 8514, distinct days: 2199, top-quintile cases: 1703
- Decided by: Confirm rule: the slope is positive with t = 2.86 >= 2 and the top-quintile mean excess return is above 0.
- Reading: Down day from the 1-bar close return inside each window (raw component sign on a window's first bar); excess = next-day return minus the coin's mean 1-bar return over all its windows; slope by pooled OLS with a day-clustered (CR1, G/(G-1)) standard error; top quintile = down-day bars with forecast at or above the pooled 80th percentile; its t is the ordinary t of the mean, as the plan does not name one.
- Size: unusual move +0.19 % (t 1.50, the cases of one day together: 1699 days) per case over 1 bars, 0.038 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.31 %; 5648 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0002565 on the check folds against +0.0004341 on every fold
Plan: `steps_cards/03_test_plan/night7_panic_run/plans/039-02_range-scaled-fall-rebound_1d.md`
Record: `steps_cards/04_backtest/night7_panic_run/backtests/039-02_range-scaled-fall-rebound_1d`
Measure: `measure.py`
