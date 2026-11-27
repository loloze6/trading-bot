---
plan: 025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d
idea: 025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the pooled slope of 5-day excess return on month_move forecast: 5.89081; OLS slope t: 5.89081 (threshold: confirm: slope > 0 with t >= 2.0; reject: slope < 0 with t <= -2.0; at least 30 cases)
- Supporting check: none
- Counts: cases: 1730
- Decided by: The slope is positive with t >= 2.0 on at least 30 cases (confirm rule).
- Reading: A case is the first bar in each 5-bar grid cell (positions 0,5,10,... from each window's first row) with regime 'trending' and non-zero forecast, its return taken from that bar's close over 5 bars inside the window; the coin's normal 5-day drift is the mean of its 5-bar returns at the grid positions over all windows; the slope's t is the ordinary OLS t; day_rise is recomputed as the 1-bar return over the 20-bar rolling std of 1-bar returns (current bar included), using the regime column where that std is not yet computable in the window; and a case count under 30 is reported as not observable.
- Size: unusual move +2.97 % (t 4.70, the cases of one day together: 733 days) per case over 5 bars, 0.205 of the coin's usual move (12.26 %); normal drift in its direction +0.34 %, total +3.31 %; 1550 cases
- Direction check on folds A, D (the years step 7 does not explore): not judged: no check fold (the plan has none, or the backtest did not run on its folds)
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/common/backtests/025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d`
Measure: `measure.py`
