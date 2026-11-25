---
plan: 035-02_break-swings-above-continues_1d
idea: 035-02_break-swings-above-continues
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-day excess return over the coin's mean 5-day return, cases with forecast > 0: 0.0230332; t of the mean, cases of one day together: 2.06709 (threshold: confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2)
- Supporting check: Spearman correlation forecast vs 5-day excess return > 0: 0.122438, passed: True
- Counts: cases: 349, distinct days: 159, active bars: 1806
- Decided by: Mean excess return above 0 with t >= 2 and Spearman correlation above 0 (confirm rule).
- Reading: Situation recomputed from prices as close above the max high of the 20 prior bars in the window (falling back to the recorded raw component > 0 on the first 20 bars), expected side long; cases are grid bars 0,5,10,... of each window with forecast > 0 and a 5-bar return inside the window; the coin's mean 5-day return is taken on the same non-overlapping grids of all its windows; the day-clustered t sums deviations per calendar day (UTC) with a D/(D-1) correction; the plan's minimum of 100 cases on 60 days, when not reached, gives 'not observable'.
- Size: unusual move +2.14 % (t 3.47, the cases of one day together: 586 days) per case over 5 bars, 0.151 of the coin's usual move (12.35 %); normal drift in its direction +0.79 %, total +2.93 %; 1072 cases
- Direction check on folds A, D (the years step 7 does not explore): agrees: main measure +0.01539 on the check folds against +0.02303 on every fold
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/035-02_break-swings-above-continues_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/backtests/035-02_break-swings-above-continues_1d`
Measure: `measure.py`
