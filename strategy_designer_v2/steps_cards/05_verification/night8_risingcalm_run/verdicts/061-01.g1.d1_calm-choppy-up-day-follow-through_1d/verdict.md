---
plan: 061-01.g1.d1_calm-choppy-up-day-follow-through_1d
idea: 061-01.g1.d1_calm-choppy-up-day-follow-through
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: slope of 5-bar excess return on forecast (grid bars, forecast > 0, pooled): 0.00223133; OLS slope t: 2.94873 (threshold: t >= 2 confirms (with mean unusual move > 0); t <= -2 rejects; otherwise inconclusive)
- Supporting check: mean unusual move of the cases > 0: 0.00281912, passed: True
- Counts: grid cases with forecast > 0: 285
- Decided by: The slope's t is 2 or more and the mean unusual move of the cases is above 0.
- Reading: The profile is read from the recorded regime ('unknown' = inside the choppy calm profile, since the detector's components are not recorded), the situation is a raw day_move value above 0 on such a bar on the long side, the coin's mean 5-bar return is taken on the non-overlapping grid of all its windows, the slope is a pooled OLS of excess return on forecast with its ordinary t, and the plan's 'fewer than 50 grid cases' minimum is applied as 'not observable'.
- Size: unusual move -0.60 % (t -1.63, the cases of one day together: 465 days) per case over 5 bars, -0.069 of the coin's usual move (10.60 %); normal drift in its direction +0.62 %, total +0.02 %; 675 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.001134 on the check folds against +0.002231 on every fold
Plan: `steps_cards/03_test_plan/night8_risingcalm_run/plans/061-01.g1.d1_calm-choppy-up-day-follow-through_1d.md`
Record: `steps_cards/04_backtest/night8_risingcalm_run/backtests/061-01.g1.d1_calm-choppy-up-day-follow-through_1d`
Measure: `measure.py`
