---
plan: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high.g1_rebound-after-scaled-sell-offs_1d
idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high.g1_rebound-after-scaled-sell-offs
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: OLS slope of excess 3-bar forward return on forecast: 0.000164092; t of OLS slope: 0.903729 (threshold: confirm if t >= 2 with supporting check passed; reject if t <= -2; otherwise inconclusive)
- Supporting check: mean excess 3-bar return on grid bars with forecast > 0: 0.000646722, passed: True
- Counts: grid bars with forecast > 0: 2718, grid bars: 5723
- Decided by: The slope's t lies between -2 and 2, which the plan calls inconclusive.
- Reading: Situation taken as a negative one-bar close-to-close return, computed from prices within each window (each window's first bar has no prior close and is left out), and the expected side as forecast > 0; the coin's mean 3-bar return is the mean over its non-overlapping grid bars pooled across all windows; the slope t is the OLS slope over its standard error on the pooled grid; the supporting check is the sign of the mean excess return on grid bars with forecast > 0; the plan's minimum of 200 grid bars with forecast > 0 maps to 'not observable'.
Plan: `steps_cards/03_test_plan/night_013_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high.g1_rebound-after-scaled-sell-offs_1d.md`
Record: `steps_cards/04_backtest/night_013_run/backtests/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high.g1_rebound-after-scaled-sell-offs_1d`
Measure: `measure.py`
