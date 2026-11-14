---
plan: N2-06_rebound-in-high-volatility_1d
idea: N2-06_rebound-in-high-volatility
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: net share of higher next closes, high-vol minus quiet, top-decile drop bars: 0.00234706; two-proportion z: 0.099304 (threshold: z >= 2 confirms, z <= -2 rejects, otherwise inconclusive)
- Supporting check: mean next-bar return minus coin mean, top-decile high-vol drop bars (t): 0.0111144, passed: True
- Counts: top-decile drop bars high-volatility: 992, top-decile drop bars quiet: 749
- Decided by: z lies between -2 and 2.
- Reading: Drop day = close below the previous close in the same window (raw drop component value < 0 on a window's first bar), expected side long; top 10 percent = forecast at or above the 90th percentile of all non-missing forecasts pooled over coins and windows, and positive; high volatility = regime 'trending' (the detector's volp >= 0.5 rule), quiet = 'unknown'; each bar's up indicator is netted by its coin's up-day share over all windows, the z uses the difference of net shares over the pooled raw-proportion standard error; the supporting check passes when its one-sample t >= 2; the plan's 'fewer than 30 in either group' is treated as the minimum count (not observable).
Plan: `steps_cards/03_test_plan/plans/N2-06_rebound-in-high-volatility_1d.md`
Record: `steps_cards/04_backtest/backtests/N2-06_rebound-in-high-volatility_1d`
Measure: `measure.py`
