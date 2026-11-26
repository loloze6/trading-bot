---
plan: 060-02_volume-growth-fall-stalls_1d
idea: 060-02_volume-growth-fall-stalls
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 5-bar excess return on forecast (grid cases, nonzero forecast): 0.000759295; OLS slope t: 2.9606 (threshold: confirm t >= 2 (with positive-minus-negative difference > 0); reject t <= -2; at least 100 cases)
- Supporting check: mean excess 5-bar return, positive minus negative forecast cases: 0.0150401, passed: True
- Counts: grid cases with a nonzero forecast: 1255, cases with a positive forecast: 535, cases with a negative forecast: 720
- Decided by: The slope has t >= 2 and the positive-minus-negative excess return difference is above 0, with at least 100 cases.
- Reading: Falling profile recomputed as 60-bar % price change < -10 inside each window (detector regime 'unknown' where 60 prior bars are not in the window), expected side = sign of the raw log volume ratio; the slope is one pooled least-squares fit with intercept over all coins' grid cases, each coin's drift being its mean grid 5-bar return over all its windows.
- Size: unusual move +1.08 % (t 2.76, the cases of one day together: 652 days) per case over 5 bars, 0.098 of the coin's usual move (10.60 %); normal drift in its direction -0.09 %, total +0.99 %; 906 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0001315 on the check folds against +0.0007593 on every fold
Plan: `steps_cards/03_test_plan/night8_fallingcalm_run/plans/060-02_volume-growth-fall-stalls_1d.md`
Record: `steps_cards/04_backtest/night8_fallingcalm_run/backtests/060-02_volume-growth-fall-stalls_1d`
Measure: `measure.py`
