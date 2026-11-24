---
plan: 031-03.g1.b1.d2.e2.g1.g2_fade-during-volatility-bursts_1d
idea: 031-03.g1.b1.d2.e2.g1.g2_fade-during-volatility-bursts
fit: exact
status: confirmed
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of demeaned next-bar return on forecast: 0.000425769; OLS slope t: 5.18031 (threshold: confirm: slope > 0 with t >= 2 and timing gain > 0; reject: slope < 0 with t <= -2; otherwise inconclusive)
- Supporting check: book timing gain (mean daily return minus position x coin mean daily return): 0.000848938, passed: True
- Counts: bars with a non-zero forecast: 2894, bars in regression: 2897
- Decided by: The slope is positive with t >= 2 and the timing gain is above 0.
- Reading: The 1000-bar minimum is counted on the regression bars (those with a next-bar return in the same window) with a non-zero forecast, and the coin's mean daily return is the mean of all close-to-close daily returns pooled over windows.
- Size: unusual move +0.57 % (t 5.15, the cases of one day together: 1678 days) per case over 1 bars, 0.122 of the coin's usual move (4.65 %); normal drift in its direction -0.00 %, total +0.57 %; 1678 cases
Plan: `steps_cards/03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2.g1.g2_fade-during-volatility-bursts_1d.md`
Record: `steps_cards/04_backtest/night6_longreversal_run/backtests/031-03.g1.b1.d2.e2.g1.g2_fade-during-volatility-bursts_1d`
Measure: `measure.py`
