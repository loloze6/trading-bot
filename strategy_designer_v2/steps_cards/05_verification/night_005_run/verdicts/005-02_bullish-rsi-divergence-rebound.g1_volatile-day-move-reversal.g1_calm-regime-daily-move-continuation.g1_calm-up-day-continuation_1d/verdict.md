---
plan: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation.g1_calm-up-day-continuation_1d
idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation.g1_calm-up-day-continuation
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean 5-bar forward return, forecast >= 2 minus all other grid bars: 0.020178; Welch t: 2.80773 (threshold: confirm: difference > 0 with Welch t >= 2 and >= 30 cases with forecast >= 2; reject: difference < 0 with Welch t <= -2)
- Supporting check: OLS slope of 5-bar forward return on forecast, grid bars with forecast > 0: 0.00171509, passed: True
- Counts: cases with forecast >= 2: 205, other grid bars: 934, grid bars with forecast > 0: 522
- Decided by: The difference is positive with Welch t >= 2 from at least 30 cases with forecast >= 2, and the supporting slope is positive.
- Reading: Situation taken as bars where the raw component is positive (and the day's in-window close-to-close return is up when computable), side long; grid is positions 0,5,10,... of each BTC and ETH window with grid bars lacking a 5-bar forward return in the window dropped, 'all other grid bars' means grid bars with forecast < 2, and the slope is undefined (not positive) with fewer than 2 positive-forecast cases.
Plan: `steps_cards/03_test_plan/night_005_run/plans/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation.g1_calm-up-day-continuation_1d.md`
Record: `steps_cards/04_backtest/night_005_run/backtests/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation.g1_calm-up-day-continuation_1d`
Measure: `measure.py`
