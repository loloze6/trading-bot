---
plan: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
idea: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of forecast coefficient in pooled regression of next-72-bar excess return on forecast and past 72-bar return (rising grid bars): 2.39707; OLS t of forecast coefficient: 2.39707 (threshold: confirm if coefficient > 0 with t >= 2; reject if coefficient < 0 with t <= -2; else inconclusive; fewer than 300 rising grid cases is not enough)
- Supporting check: none
- Counts: rising grid cases pooled over the coins: 2865
- Decided by: The forecast coefficient is positive with t >= 2 on at least 300 rising grid cases (confirm rule).
- Reading: Grid at positions 0,72,144,... of each window; rising cases need a past 72-bar close and a next-72-bar close inside the window; the coin's mean 72-bar return is the mean of the forward returns of all its grid bars over all windows; OLS with an intercept and the ordinary coefficient t.
- Size: unusual move +0.37 % per case over 72 bars, 0.043 of the coin's usual move (8.23 %); normal drift in its direction +0.41 %, total +0.78 %; 2935 cases
Plan: `steps_cards/03_test_plan/std_time_pilot_run/plans/016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h.md`
Record: `steps_cards/04_backtest/std_time_pilot_run/backtests/016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h`
Measure: `measure.py`
