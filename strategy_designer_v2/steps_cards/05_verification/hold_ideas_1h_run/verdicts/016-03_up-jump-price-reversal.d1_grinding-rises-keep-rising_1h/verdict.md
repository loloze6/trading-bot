---
plan: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h
idea: 016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of forecast coefficient in pooled regression of next-72-bar excess return on forecast and past 72-bar return (rising grid bars): 1.50087; OLS t of forecast coefficient: 1.50087 (threshold: confirm if coefficient > 0 with t >= 2; reject if coefficient < 0 with t <= -2; else inconclusive; fewer than 300 rising grid cases is not enough)
- Supporting check: none
- Counts: rising grid cases pooled over the coins: 2865
- Decided by: The forecast coefficient's t lies between -2 and +2 (inconclusive rule).
- Reading: Grid at positions 0,72,144,... of each window; rising cases need a past 72-bar close and a next-72-bar close inside the window; the coin's mean 72-bar return is the mean of the forward returns of all its grid bars over all windows; OLS with an intercept and the ordinary coefficient t.
- Size: unusual move +0.43 % per case over 72 bars, 0.049 of the coin's usual move (8.23 %); normal drift in its direction +0.41 %, total +0.83 %; 2862 cases
Plan: `steps_cards/03_test_plan/hold_ideas_1h_run/plans/016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h.md`
Record: `steps_cards/04_backtest/hold_ideas_1h_run/backtests/016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising_1h`
Measure: `measure.py`
