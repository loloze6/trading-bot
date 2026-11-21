---
plan: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal_1d
idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean of position x (next-bar return - coin mean daily return) on weekend bars: 0.00103142; t of the mean: 4.61315 (threshold: t >= 2 confirms (with supporting t >= 2); t <= -2 rejects)
- Supporting check: Welch t of per-unit fade -z_t x (r_{t+1} - coin mean), weekend minus weekday: 3.47038, passed: True
- Counts: weekend bars (main measure): 10535, weekend bars (supporting check): 8806, weekday bars (supporting check): 22022
- Decided by: Confirm rule met: the main measure's t is >= 2 and the supporting check's t is >= 2.
- Reading: Weekend bars are the bars with regime mean_reversion (bar just closed is Saturday or Sunday), weekday bars all others; z_t is the bar's close-to-close return over the std of the last 20 daily returns including it, inside each window; every bar with a next close in its window is one case. Supporting weekend-minus-weekday mean difference: 0.002808274751651743.
- Size: unusual move +0.32 % per case over 1 bars, 0.061 of the coin's usual move (5.31 %); normal drift in its direction -0.01 %, total +0.31 %; 7739 cases
Plan: `steps_cards/03_test_plan/night_run/plans/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal_1d.md`
Record: `steps_cards/04_backtest/night_run/backtests/011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal_1d`
Measure: `measure.py`
