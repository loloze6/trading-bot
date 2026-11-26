---
plan: 032-02.b1.e2_tight-range-breakouts-continue_1d
idea: 032-02.b1.e2_tight-range-breakouts-continue
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean unusual 10-bar move per long case (percent): 4.52012; t of the mean, cases of one day taken together: 2.58843 (threshold: confirm: mean > 0 with day-clustered t >= 2; reject: t <= -2)
- Supporting check: Spearman rank correlation entry forecast vs unusual move (> 0): 0.0332179, passed: True
- Counts: cases: 188, distinct days: 156
- Decided by: Confirm: mean unusual move > 0 with t >= 2 and the rank correlation is above 0.
- Reading: Situation recomputed from prices on active bars with enough in-window history (ER(60) smoothed by a 5-bar mean or EMA, or unsmoothed, at or below 0.3, and close strictly above the max high of the prior 60 bars, forecast > 0), falling back to regime=='trending' only if no bar is evaluable; a case is the first forecast bet (rise >= 2 points from its lowest positive level since the last bet) in each 10-bar grid cell from each window's first row, cases without 10 bars ahead in the window are dropped, the per-day clustered t uses D/(D-1) correction, the rank-correlation t is rho*sqrt((n-2)/(1-rho^2)), and the plan's '30 cases on 30 days' minimum is reported as 'not observable'.
- Size: unusual move +4.52 % (t 2.60, the cases of one day together: 156 days) per case over 10 bars, 0.262 of the coin's usual move (14.49 %); normal drift in its direction +1.15 %, total +5.67 %; 188 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: too few cases on the check folds (86 cases, 75 days)
Plan: `steps_cards/03_test_plan/night7c_rangefail_run/plans/032-02.b1.e2_tight-range-breakouts-continue_1d.md`
Record: `steps_cards/04_backtest/night7c_rangefail_run/backtests/032-02.b1.e2_tight-range-breakouts-continue_1d`
Measure: `measure.py`
