---
plan: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall_1d
idea: 025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall
fit: exact
status: not observable
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of position x (next-day return minus coin's mean daily return) over mean_reversion cases: -0.0143684; t of the mean: -0.828295 (threshold: confirm: mean > 0 with t >= 2; reject: mean < 0 with t <= -2)
- Supporting check: correlation of forecast with next-day drift-adjusted return > 0: -0.965428, passed: False
- Counts: cases: 4
- Decided by: Only 4 cases over all coins and windows, fewer than the plan's minimum of 30.
- Reading: Situation check uses active bars where r90 (close/close 90 bars earlier within the window), r30 (recorded fall30 raw value, else from prices) and the jump (1-day return over the 20-day std of daily returns, accepted if >= 2 with the std either including or excluding today) can be computed, side short; cases are regime == mean_reversion bars with nonzero forecast and a next close in the same window, the drift is the coin's pooled mean daily return over all its windows, the correlation is Pearson between forecast and drift-adjusted next-day return, and the plan's 'fewer than 30 cases' minimum gives 'not observable'.
- Size: unusual move +0.99 % (t 0.33, the cases of one day together: 3 days) per case over 1 bars, 0.016 of the coin's usual move (7.81 %); normal drift in its direction -1.55 %, total -0.56 %; 3 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/unseen_2016_2017/backtests/025-02_deeper-fall-bigger-giveback.b1_deeper-fall-bigger-giveback-more-coins.b1_bounce-fades-in-monthly-fall_1d`
Measure: `measure.py`
