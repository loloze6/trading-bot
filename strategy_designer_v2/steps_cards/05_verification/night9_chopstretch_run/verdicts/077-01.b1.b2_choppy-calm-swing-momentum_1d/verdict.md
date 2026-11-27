---
plan: 077-01.b1.b2_choppy-calm-swing-momentum_1d
idea: 077-01.b1.b2_choppy-calm-swing-momentum
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of 7-bar forward excess return (minus coin's normal 7-bar drift) on the forecast, grid bars with nonzero forecast: 0.000266304; slope t (day-clustered): 0.352559 (threshold: confirm: t >= 2 with both sides passing; reject: t <= -2; else inconclusive)
- Supporting check: mean excess forward return: long > 0 and short < 0: 0.00612497, passed: True
- Counts: grid cases with a nonzero forecast: 777, long cases: 409, short cases: 368, days (clusters): 229
- Decided by: The slope's t is between -2 and 2.
- Reading: Profile taken from the recorded regime ('unknown' = choppy-calm, the only regime with a strategy) and side from the sign of the raw swing-scaled 14-day move (recomputed from prices where unrecorded); the slope is an OLS slope with intercept whose t uses day-clustered standard errors (scores summed per UTC day, G/(G-1) correction); the normal drift is the mean of each coin's non-overlapping 7-bar grid returns over all its windows; fewer than the plan's minimum cases is reported as not observable.
- Size: unusual move +0.56 % (t 1.07, the cases of one day together: 681 days) per case over 7 bars, 0.040 of the coin's usual move (12.84 %); normal drift in its direction +0.05 %, total +0.61 %; 1125 cases
Plan: `steps_cards/03_test_plan/night9_chopstretch_run/plans/077-01.b1.b2_choppy-calm-swing-momentum_1d.md`
Record: `steps_cards/04_backtest/night9_chopstretch_run/backtests/077-01.b1.b2_choppy-calm-swing-momentum_1d`
Measure: `measure.py`
