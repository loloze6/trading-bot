---
plan: 061-01.g1.d1.d2.g2_choppy-swing-scaled-move-continues_1d
idea: 061-01.g1.d1.d2.g2_choppy-swing-scaled-move-continues
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled slope of drift-adjusted next 5-bar return on forecast: 0.000480718; slope t, clustered by day: 1.11408 (threshold: t >= 2 confirms (with supporting check), t <= -2 rejects)
- Supporting check: top minus bottom third of |forecast|, mean sign(f) x drift-adjusted 5-bar return: 0.0108053, passed: True
- Counts: grid cases with a nonzero forecast: 818, days: 374, top third cases: 272, bottom third cases: 272
- Decided by: The slope's t is between -2 and 2: inconclusive.
- Reading: Grid of positions 0,5,10,... per window with a full 5-bar return inside the window; drift is the coin's mean 5-bar grid return over all its windows; slope t from OLS with intercept and standard errors clustered by UTC day; thirds are the n//3 cases with largest and smallest |forecast|; the choppy profile is the recorded regime 'unknown'.
- Size: unusual move +0.13 % (t 0.43, the cases of one day together: 837 days) per case over 5 bars, 0.006 of the coin's usual move (10.60 %); normal drift in its direction +0.01 %, total +0.14 %; 1157 cases
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/061-01.g1.d1.d2.g2_choppy-swing-scaled-move-continues_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.d1.d2.g2_choppy-swing-scaled-move-continues_1d`
Measure: `measure.py`
