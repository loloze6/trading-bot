---
plan: 058-02.b1.b2.b1.b2.e2_calm-nearness-to-high-short-horizon_1d
idea: 058-02.b1.b2.b1.b2.e2_calm-nearness-to-high-short-horizon
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 3-day return on forecast, in-profile grid cases: 0.000702672; OLS slope t: 3.95502 (threshold: confirm: slope t >= 2 with top-minus-bottom > 0; reject: slope t <= -2)
- Supporting check: top-third minus bottom-third mean excess 3-day return (Welch t 3.388): 0.00815997, passed: True
- Counts: grid cases: 5737, active bars: 17583
- Decided by: The slope's t is 2 or more and the top-minus-bottom difference is above 0.
- Reading: Calm profile read as regime other than 'chop'; the coin's mean 3-day return is taken on the same non-overlapping grid over all its windows; thirds are the n//3 lowest and highest forecasts after a stable sort, pooled across coins; the plan's 'inconclusive' under 300 cases is reported as 'not observable' per the workflow.
- Size: unusual move +0.08 % (t 0.35, the cases of one day together: 1192 days) per case over 3 bars, 0.010 of the coin's usual move (8.85 %); normal drift in its direction +0.42 %, total +0.50 %; 3032 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.0002896 on the check folds against +0.0007027 on every fold
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.b2.b1.b2.e2_calm-nearness-to-high-short-horizon_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.b2.b1.b2.e2_calm-nearness-to-high-short-horizon_1d`
Measure: `measure.py`
