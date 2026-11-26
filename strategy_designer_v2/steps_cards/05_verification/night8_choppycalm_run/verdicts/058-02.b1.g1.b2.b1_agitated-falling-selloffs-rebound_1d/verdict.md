---
plan: 058-02.b1.g1.b2.b1_agitated-falling-selloffs-rebound_1d
idea: 058-02.b1.g1.b2.b1_agitated-falling-selloffs-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess next-day return: 0.010976; day-clustered t of the weighted mean: 3.2409 (threshold: confirm: positive with t >= 2 (and top-minus-bottom third > 0); reject: negative with t <= -2)
- Supporting check: top third minus bottom third mean excess next-day return: 0.0132514, passed: True
- Counts: cases: 1468, distinct days: 702
- Decided by: The weighted mean excess return is positive with t >= 2 and the top third beats the bottom third.
- Reading: Situation bars are bars where the recorded scaled return (recomputed from prices if missing) is below 0, on the long side; the t is a day-clustered t of the weighted mean (per-day sums of w*(x-mean), with G/(G-1) correction); thirds are split by sorted forecast with np.array_split and compared on unweighted mean excess returns; the plan's minimum of 100 cases on 60 days is applied as 'not observable'.
- Size: unusual move +1.05 % (t 3.49, the cases of one day together: 477 days) per case over 1 bars, 0.225 of the coin's usual move (4.73 %); normal drift in its direction +0.13 %, total +1.18 %; 982 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.00483 on the check folds against +0.01098 on every fold
Plan: `steps_cards/03_test_plan/night8_choppycalm_run/plans/058-02.b1.g1.b2.b1_agitated-falling-selloffs-rebound_1d.md`
Record: `steps_cards/04_backtest/night8_choppycalm_run/backtests/058-02.b1.g1.b2.b1_agitated-falling-selloffs-rebound_1d`
Measure: `measure.py`
