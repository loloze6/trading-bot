---
plan: 032-02.b1.e1_quiet-breakouts-continue-longer_1d
idea: 032-02.b1.e1_quiet-breakouts-continue-longer
fit: adapted
status: inconclusive
---
Situation check: 99 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar move per case (long, minus coin's normal 10-bar drift): 0.0255605; t of the mean, cases of the same day pooled: 1.99695 (threshold: mean > 0 with day-pooled t >= 2 to confirm; mean < 0 with t <= -2 to reject)
- Supporting check: mean unusual move of larger-forecast half minus smaller-forecast half (Welch t): -0.0138754, passed: False
- Counts: cases: 261, distinct days: 217
- Decided by: Inconclusive: the main measure meets neither the confirm nor the reject rule.
- Reading: Situation recomputed as the 60-bar Kaufman efficiency ratio smoothed by a 5-bar simple mean below 0.3 and the close above the highest of the prior 60 closes, long side, on active bars where the record holds enough bars to compute it (earlier active bars left out of the agreement); cases are the first 2-point forecast rise (holding-period bet) in each 10-bar grid cell from each window's first row, the day-pooled t uses cluster sums of deviations with a G/(G-1) correction, the larger half is entry forecast above the median and the smaller half at or below it, the reject rule is applied before the confirm rule, and the plan's minimum of 30 cases on 30 days gives 'not observable' when not reached.
- Size: unusual move +2.56 % (t 2.00, the cases of one day together: 217 days) per case over 10 bars, 0.165 of the coin's usual move (14.49 %); normal drift in its direction +1.16 %, total +3.72 %; 261 cases
Plan: `steps_cards/03_test_plan/night7c_rangefail_run/plans/032-02.b1.e1_quiet-breakouts-continue-longer_1d.md`
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1.e1_quiet-breakouts-continue-longer_1d`
Measure: `measure.py`
