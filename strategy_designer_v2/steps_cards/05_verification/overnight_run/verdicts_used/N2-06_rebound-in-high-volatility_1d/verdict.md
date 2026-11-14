---
plan: N2-06_rebound-in-high-volatility_1d
idea: N2-06_rebound-in-high-volatility
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: net share of higher next closes, high-vol minus quiet, top-decile forecast bars: 0.00234706; two-proportion z: 0.099304 (threshold: two-proportion z >= 2 confirms, z <= -2 rejects, between is inconclusive; at least 30 bars per group)
- Supporting check: mean next-bar excess return, top-decile high-vol drop bars (t of mean), t=5.315: 0.0111144, passed: True
- Counts: top-decile drop bars, high volatility: 992, top-decile drop bars, quiet: 749
- Decided by: Inconclusive rule met: z = 0.10 lies between -2 and 2.
- Reading: Situation taken as a negative one-day change (drop component's raw value, else the close-to-close return) with a long forecast; top decile = bars whose forecast is at or above the 90th percentile of all non-missing forecasts pooled over coins and windows and is positive, keeping those with a next close in the same window; high volatility = regime 'trending' (volp >= 0.5) and quiet = regime 'unknown'; each bar's up indicator is netted by its coin's share of higher next closes over all windows, the z numerator is the difference of the net shares with the pooled raw share giving the standard error; the supporting check passes at t >= 2 since the plan states no threshold for it; fewer than 30 bars in a group is reported as not observable.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N2-06_rebound-in-high-volatility_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N2-06_rebound-in-high-volatility_1d`
Measure: `measure.py`
