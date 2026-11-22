---
plan: 025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d
idea: 025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend
fit: exact
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of the pooled slope of 5-day excess return on month_move forecast: 0.99555; OLS slope t: 0.99555 (threshold: confirm: slope > 0 with t >= 2.0; reject: slope < 0 with t <= -2.0; at least 30 cases)
- Supporting check: none
- Counts: cases: 116
- Decided by: The slope's t lies between -2.0 and 2.0 (inconclusive rule).
- Reading: A case is the first bar in each 5-bar grid cell (positions 0,5,10,... from each window's first row) with regime 'trending' and non-zero forecast, its return taken from that bar's close over 5 bars inside the window; the coin's normal 5-day drift is the mean of its 5-bar returns at the grid positions over all windows; the slope's t is the ordinary OLS t; day_rise is recomputed as the 1-bar return over the 20-bar rolling std of 1-bar returns (current bar included), using the regime column where that std is not yet computable in the window; and a case count under 30 is reported as not observable.
- Size: unusual move +4.59 % per case over 5 bars, 0.211 of the coin's usual move (18.32 %); normal drift in its direction +3.41 %, total +8.00 %; 104 cases
Plan: `steps_cards/03_test_plan/night4_fallingbounce_run/plans/025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d.md`
Record: `steps_cards/04_backtest/night4_fallingbounce_run/unseen_2016_2017/backtests/025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d`
Measure: `measure.py`
