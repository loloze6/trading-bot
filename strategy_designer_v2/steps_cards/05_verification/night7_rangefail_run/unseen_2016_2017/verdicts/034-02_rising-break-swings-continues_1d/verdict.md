---
plan: 034-02_rising-break-swings-continues_1d
idea: 034-02_rising-break-swings-continues
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 5-bar return: 0.0613784; t of the weighted mean, cases of one day together: 2.01714 (threshold: confirm: mean > 0 with t >= 2 and Spearman > 0; reject: mean < 0 with t <= -2)
- Supporting check: Spearman correlation of forecast with 5-bar excess return: 0.0110042, passed: True
- Counts: cases: 140, distinct days: 111
- Decided by: The forecast-weighted mean excess 5-bar return is above 0 with t >= 2 and the Spearman correlation is above 0.
- Reading: A case is a holding-period bet of the forecast (a rise of at least 2 points from its lowest level on its side since the last bet), the first one in each 5-bar grid cell of a window; the t of the weighted mean sums the weighted deviations per day; the plan's 'fewer than 30 cases/days' is reported as not observable.
- Size: unusual move +5.31 % (t 2.34, the cases of one day together: 111 days) per case over 5 bars, 0.328 of the coin's usual move (18.32 %); normal drift in its direction +4.77 %, total +10.08 %; 140 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night7_rangefail_run/plans/034-02_rising-break-swings-continues_1d.md`
Record: `steps_cards/04_backtest/night7_rangefail_run/unseen_2016_2017/backtests/034-02_rising-break-swings-continues_1d`
Measure: `measure.py`
