---
plan: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h
idea: 017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean per-bar timing gain of the position vs holding the coin, 1 bar: 8.10255e-05; ordinary t of the mean: 11.2128 (threshold: confirm: mean > 0 with t >= 2 (and supporting check passes); reject: mean < 0 with t <= -2)
- Supporting check: mean timing gain, top minus bottom quintile of abs(forecast): 0.000251551, passed: True
- Counts: bars with a non-zero position across all coins and windows: 257864, bars in the main measure: 416645
- Decided by: Mean timing gain positive with t >= 2 and top-minus-bottom quintile difference above 0.
- Reading: Quintiles of abs(forecast) are cut on the pooled bars of the main measure by rank (ties broken by row order); the coin's mean hourly return is the mean of all its within-window 1-bar returns; the 10,000-bar minimum counts bars with a non-zero postRebalance_current_allocation and a next-bar return inside the window, and is treated as 'not observable' when unmet.
Plan: `steps_cards/03_test_plan/hold_confirmed_1h_run/plans/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h.md`
Record: `steps_cards/04_backtest/hold_confirmed_1h_run/backtests/017-02_presettle-rise-after-downtrend.g2_hourly-reversal-in-volatile-periods_1h`
Measure: `measure.py`
