---
plan: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound.b1_volatile-evening-fall-more-coins_1h
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound.b1_volatile-evening-fall-more-coins
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: t of mean of forecast/10 x excess 24-bar return, one case per coin-day: 0.00805157; t of the mean: 8.94501 (threshold: confirm t >= 2 with >= 100 cases and slope > 0; reject t <= -2 with >= 100 cases)
- Supporting check: OLS slope of excess 24-bar return on forecast: 0.000837372, passed: True
- Counts: cases: 7691
- Decided by: Confirm: t >= 2 with at least 100 cases, and the slope is above 0.
- Reading: The 20:00 UTC close is the bar whose timestamp (start) is 19:00 UTC; volatility high is the 240-bar std of hourly simple returns at or above its 720-bar mean, recomputed inside each window, with the agreement taken over active bars where that ratio is computable; a fall is a negative raw fall_x_vol value; one case per coin-day is the first qualifying bar of that UTC date within a window, cases without a bar 24 rows later in the same window are dropped, and the coin's mean 24-bar return uses the non-overlapping grid of all its windows.
Plan: `steps_cards/03_test_plan/more_coins_1h_run/plans/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound.b1_volatile-evening-fall-more-coins_1h.md`
Record: `steps_cards/04_backtest/more_coins_1h_run/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound.b1_volatile-evening-fall-more-coins_1h`
Measure: `measure.py`
