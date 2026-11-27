---
plan: 035-02_break-swings-above-continues_1d
idea: 035-02_break-swings-above-continues
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-day excess return over the coin's mean 5-day return, cases with forecast > 0: 0.027436; t of the mean, cases of one day together: 2.56512 (threshold: confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2)
- Supporting check: Spearman correlation forecast vs 5-day excess return > 0: 0.0886194, passed: True
- Counts: cases: 511, distinct days: 229, active bars: 2642
- Decided by: Mean excess return above 0 with t >= 2 and Spearman correlation above 0 (confirm rule).
- Reading: Situation recomputed from prices as close above the max high of the 20 prior bars in the window (falling back to the recorded raw component > 0 on the first 20 bars), expected side long; cases are grid bars 0,5,10,... of each window with forecast > 0 and a 5-bar return inside the window; the coin's mean 5-day return is taken on the same non-overlapping grids of all its windows; the day-clustered t sums deviations per calendar day (UTC) with a D/(D-1) correction; the plan's minimum of 100 cases on 60 days, when not reached, gives 'not observable'.
- Size: unusual move +2.55 % (t 4.53, the cases of one day together: 825 days) per case over 5 bars, 0.181 of the coin's usual move (12.26 %); normal drift in its direction +0.81 %, total +3.36 %; 1544 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/035-02_break-swings-above-continues_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/common/backtests/035-02_break-swings-above-continues_1d`
Measure: `measure.py`
