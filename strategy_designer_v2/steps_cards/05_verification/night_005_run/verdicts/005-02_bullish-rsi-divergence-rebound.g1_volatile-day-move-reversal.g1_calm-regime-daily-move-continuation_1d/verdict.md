---
plan: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation_1d
idea: 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation
fit: adapted
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean sign(forecast) x excess 5-bar return, top |forecast| quintile, pooled: 0.0126832; t of the mean: 2.26839 (threshold: confirm t >= 2, reject t <= -2, with at least 30 top-quintile cases)
- Supporting check: top-quintile mean minus other-four-quintiles mean of signed excess return: 0.0169429, passed: True
- Counts: top-quintile cases: 228, other-quintile cases: 911
- Decided by: Confirm: t >= 2 with at least 30 top-quintile cases and a positive top-minus-other difference.
- Reading: The top quintile of each coin is the 20% of its grid cases with the largest |forecast| (ranked with ties broken by time order, cases with rank above 0.8 x n), zero forecasts included with sign 0, and fewer than 30 top-quintile cases is reported as not observable.
- Size: unusual move +0.75 % per case over 5 bars, 0.079 of the coin's usual move (9.19 %); normal drift in its direction +0.03 %, total +0.78 %; 839 cases
Plan: `steps_cards/03_test_plan/night_005_run/plans/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation_1d.md`
Record: `steps_cards/04_backtest/night_005_run/backtests/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g1_calm-regime-daily-move-continuation_1d`
Measure: `measure.py`
