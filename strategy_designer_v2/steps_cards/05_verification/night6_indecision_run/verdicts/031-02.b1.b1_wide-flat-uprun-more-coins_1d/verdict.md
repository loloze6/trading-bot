---
plan: 031-02.b1.b1_wide-flat-uprun-more-coins_1d
idea: 031-02.b1.b1_wide-flat-uprun-more-coins
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar move of the cases (before costs): 0.0223777; t of the mean, cases of one day summed together: 1.29214 (threshold: confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2)
- Supporting check: Spearman correlation of case forecast vs unusual move > 0: 0.125995, passed: True
- Counts: cases: 181, distinct case days: 134
- Decided by: t between -2 and 2: inconclusive by the plan.
- Reading: A case is the first bet (forecast rise >= 2 from its low on its side since the last bet) in each 10-bar grid cell from each window's first row, kept only if 10 bars follow in its window; the drift is the coin's mean 10-bar return on that grid over all its windows; a day is the UTC date of the case bar; situation bars without 20 bars of history use the recorded regime 'trending'.
- Size: unusual move +2.24 % (t 1.30, the cases of one day together: 134 days) per case over 10 bars, 0.130 of the coin's usual move (16.82 %); normal drift in its direction +1.60 %, total +3.84 %; 181 cases
Plan: `steps_cards/03_test_plan/night6_indecision_run/plans/031-02.b1.b1_wide-flat-uprun-more-coins_1d.md`
Record: `steps_cards/04_backtest/night6_indecision_run/backtests/031-02.b1.b1_wide-flat-uprun-more-coins_1d`
Measure: `measure.py`
