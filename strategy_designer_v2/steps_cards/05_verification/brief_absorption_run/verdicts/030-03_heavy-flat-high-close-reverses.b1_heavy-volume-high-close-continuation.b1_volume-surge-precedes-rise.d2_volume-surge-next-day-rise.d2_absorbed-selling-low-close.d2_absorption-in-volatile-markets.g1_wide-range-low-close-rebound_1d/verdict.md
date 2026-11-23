---
plan: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.g1_wide-range-low-close-rebound_1d
idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.g1_wide-range-low-close-rebound
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: pooled OLS slope of excess next-day return on post_pipeline_value: 0.000363224; OLS t of slope: 6.15347 (threshold: confirm: slope > 0 with t >= 2; reject: slope < 0 with t <= -2)
- Supporting check: mean excess next-day return, top fifth of forecasts minus other bars (Welch t) [Welch t = 5.026]: 0.00494861, passed: True
- Counts: bars with a next-day return: 17380, bars in the top fifth: 3476
- Decided by: Slope positive with t >= 2 and top-fifth mean excess return larger with Welch t >= 2 (confirm rule).
- Reading: Top fifth taken as pooled bars with post_pipeline_value at or above its pooled 80th percentile; each coin's mean daily return is the mean of its next-bar returns over all its windows; the supporting check passes when the top-fifth mean is larger with Welch t >= 2, as the confirm rule needs.
- Size: unusual move +0.09 % per case over 1 bars, 0.020 of the coin's usual move (4.78 %); normal drift in its direction +0.12 %, total +0.21 %; 7074 cases
Plan: `steps_cards/03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.g1_wide-range-low-close-rebound_1d.md`
Record: `steps_cards/04_backtest/brief_absorption_run/backtests/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d2_absorbed-selling-low-close.d2_absorption-in-volatile-markets.g1_wide-range-low-close-rebound_1d`
Measure: `measure.py`
