---
plan: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound_1h
idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of forecast/10 x excess 24-bar return: 0.00855405; t of the mean: 7.0489 (threshold: t >= 2 (confirm, with slope > 0) or t <= -2 (reject), with at least 100 cases)
- Supporting check: OLS slope of excess 24-bar return on forecast: 0.00080228, passed: True
- Counts: cases: 3592
- Decided by: Confirm rule met: t >= 2 with at least 100 cases and an OLS slope above 0.
- Reading: The bar 'closing at 20:00 UTC' is the bar whose timestamp plus the bar length is 20:00 (timestamp is the start); high volatility is the 240-bar std of hourly returns at or above its 720-bar mean, recomputed from prices inside each window, and active bars where it cannot be computed (window warm-up) are left out of the agreement; the fall is the 24-bar price return below 0 (raw component sign where the return is not computable); the coin's mean 24-bar return uses the non-overlapping grid 0,24,48,... of every window pooled; one case per coin-day is the first qualifying bar of that UTC date.
- Size: unusual move +0.57 % per case over 24 bars, 0.116 of the coin's usual move (4.87 %); normal drift in its direction +0.15 %, total +0.71 %; 3104 cases
Plan: `steps_cards/03_test_plan/std_time_pilot_run/plans/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound_1h.md`
Record: `steps_cards/04_backtest/std_time_pilot_run/backtests/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound_1h`
Measure: `measure.py`
