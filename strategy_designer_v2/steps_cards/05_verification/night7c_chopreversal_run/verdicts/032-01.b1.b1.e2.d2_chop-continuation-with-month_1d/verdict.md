---
plan: 032-01.b1.b1.e2.d2_chop-continuation-with-month_1d
idea: 032-01.b1.b1.e2.d2_chop-continuation-with-month
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the slope of next 7-day return minus drift on forecast, regime grid bars: 3.89505; OLS slope t: 3.89505 (threshold: confirm if t >= 2 with positive supporting mean; reject if t <= -2)
- Supporting check: mean of sign(forecast) x (next 7-day return minus drift): 0.0135488, passed: True
- Counts: grid cases in the regime across coins and windows: 1114
- Decided by: The slope t is 2 or more and the supporting mean is positive (confirm rule).
- Reading: The situation is recomputed inside each window from closes (ER = |close[t]-close[t-30]| / sum of the last 30 absolute daily changes, 7- and 30-bar returns as close[t]/close[t-h]-1) and checked only on active bars where all three can be computed from the window's own bars; regime bars are those whose recorded regime is 'mean_reversion', the drift is the coin's mean 7-bar return over the non-overlapping grid of all its windows, the slope is a pooled OLS over coins and windows, and the plan's 'fewer than 50 grid cases' is applied as the minimum count giving 'not observable'.
- Size: unusual move +1.06 % (t 2.75, the cases of one day together: 1043 days) per case over 7 bars, 0.079 of the coin's usual move (12.44 %); normal drift in its direction -0.03 %, total +1.03 %; 1758 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.8333 on the check folds against +3.895 on every fold
Plan: `steps_cards/03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1.e2.d2_chop-continuation-with-month_1d.md`
Record: `steps_cards/04_backtest/night7c_chopreversal_run/backtests/032-01.b1.b1.e2.d2_chop-continuation-with-month_1d`
Measure: `measure.py`
