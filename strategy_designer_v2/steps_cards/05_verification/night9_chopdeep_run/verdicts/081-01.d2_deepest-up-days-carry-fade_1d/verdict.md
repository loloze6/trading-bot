---
plan: 081-01.d2_deepest-up-days-carry-fade_1d
idea: 081-01.d2_deepest-up-days-carry-fade
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean next-day excess return of top-|forecast|-quintile up days, short-signed: 0.00451171; t of the mean (per-day sums): 2.49148 (threshold: confirm t >= 2 with supporting check < 0; reject t <= -2)
- Supporting check: next-day excess return, top-quintile minus bottom-quintile up days: -0.00778819, passed: True
- Counts: top-quintile cases: 4222, distinct days: 1132, bottom-quintile cases: 4242
- Decided by: The main measure has t >= 2 and the top-minus-bottom excess return is below 0.
- Reading: Up days are bars whose close is above the prior close in the same window (each window's first bar, with no prior close, is left out); the top and bottom quintiles are the up-day bars with |forecast| at or above the pooled 80th percentile and at or below the pooled 20th percentile; the main mean is over cases and its t is the ordinary t over per-day sums of the short-signed excess returns; the supporting check uses the unsigned excess returns, top minus bottom.
- Size: unusual move +0.38 % (t 2.71, the cases of one day together: 1513 days) per case over 1 bars, 0.072 of the coin's usual move (5.31 %); normal drift in its direction -0.15 %, total +0.22 %; 7041 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.001189 on the check folds against +0.004512 on every fold
Plan: `steps_cards/03_test_plan/night9_chopdeep_run/plans/081-01.d2_deepest-up-days-carry-fade_1d.md`
Record: `steps_cards/04_backtest/night9_chopdeep_run/backtests/081-01.d2_deepest-up-days-carry-fade_1d`
Measure: `measure.py`
