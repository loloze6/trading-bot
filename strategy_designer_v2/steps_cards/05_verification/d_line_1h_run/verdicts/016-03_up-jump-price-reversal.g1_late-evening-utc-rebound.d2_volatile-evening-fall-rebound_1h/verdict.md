---
plan: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound_1h
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: forecast-weighted mean excess 24-bar forward return of forecast>0 cases: 0.00798266; t of the forecast-weighted mean: 6.52347 (threshold: confirm: positive with t >= 2 (and top-minus-bottom third > 0); reject: negative with t <= -2; at least 100 pooled cases)
- Supporting check: top-third minus bottom-third mean excess 24-bar return: 0.01237, passed: True
- Counts: pooled cases: 3894
- Decided by: The forecast-weighted mean excess return is positive with t >= 2 and the top-minus-bottom-third difference is above 0.
- Reading: The bar 'closing at 20:00 UTC' is the bar whose start timestamp is 19:00 UTC; the fall is the recorded raw 24-bar change (recomputed from closes where missing) below 0; the high-volatility condition is read from the recorded regime 'mean_reversion' since the detector's volatility rank is not recorded; the coin's mean 24-bar return uses the non-overlapping grid 0,24,48,... of every window pooled per coin; the t of the forecast-weighted mean uses the weighted standard error sqrt(n/(n-1)*sum(w^2(x-m)^2))/sum(w); thirds are equal-size splits of the cases sorted by forecast and compared on unweighted mean excess return.
- Size: unusual move +0.51 % per case over 24 bars, 0.105 of the coin's usual move (4.87 %); normal drift in its direction +0.15 %, total +0.66 %; 3336 cases
Plan: `steps_cards/03_test_plan/d_line_1h_run/plans/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound_1h.md`
Record: `steps_cards/04_backtest/d_line_1h_run/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound_1h`
Measure: `measure.py`
