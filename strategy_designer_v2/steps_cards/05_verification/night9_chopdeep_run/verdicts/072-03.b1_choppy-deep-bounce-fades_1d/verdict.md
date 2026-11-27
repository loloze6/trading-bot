---
plan: 072-03.b1_choppy-deep-bounce-fades_1d
idea: 072-03.b1_choppy-deep-bounce-fades
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual move over 10 bars after short bets, short direction: 0.0115932; t of the mean, cases summed per day: 1.98863 (threshold: mean > 0 with t >= 2 confirms (with deeper-minus-shallower > 0); mean < 0 with t <= -2 rejects)
- Supporting check: deeper-minus-shallower mean unusual move (median |forecast| split): -0.00165973, passed: False
- Counts: cases: 628, distinct days: 463
- Decided by: The main measure's t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Up day computed from consecutive closes (first window bar from the recorded regime) and the choppy profile taken as the recorded regime not being 'chop'; a case is the first short bet in each 10-bar cell of a window's grid, the per-day clustered t uses a D/(D-1) correction, the deeper half is |forecast| strictly above the median, and the plan's minimum-count clause is reported as 'not observable'.
- Size: unusual move +1.16 % (t 1.99, the cases of one day together: 463 days) per case over 10 bars, 0.084 of the coin's usual move (14.49 %); normal drift in its direction -1.14 %, total +0.02 %; 628 cases
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/072-03.b1_choppy-deep-bounce-fades_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/072-03.b1_choppy-deep-bounce-fades_1d`
Measure: `measure.py`
