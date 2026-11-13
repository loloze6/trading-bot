---
plan: N6-01_breakout-after-longer-decline_1d
idea: N6-01_breakout-after-longer-decline
fit: adapted
status: inconclusive
---
Situation check: 100 % of the active bars match the plan's situation and side
Evidence:
- Main measure: mean forward 10-bar excess return after forecast >= 10: -0.00515649; t of the mean: -0.363486 (threshold: mean > 0 with t >= 2 confirms; mean < 0 with t <= -2 rejects)
- Supporting check: correlation of forecast with forward 10-bar excess return, trending bars, non-overlapping: 0.0263233, passed: True
- Counts: independent cases: 99, supporting samples: 830
- Decided by: The t lies between -2 and 2, which neither confirms nor rejects.
- Reading: Situation bars are those with regime 'trending' (the detector's close-below-close-60-bars-ago rule) and range_top raw value > 0 (upper half of the 21-close range, the graded 'top of range'), on the long side; the coin's mean 10-bar return is over all its bars with a 10-bar forward return in all windows (overlapping); qualifying bars (forecast >= 10) are chained into one case while each is within 10 bars of the previous qualifying bar in the same window, and each case takes the excess return of its first bar; the t is the ordinary t of the mean; the supporting correlation is Pearson on trending bars at grid positions 0,10,20,... of each window.
Plan: `steps_cards/03_test_plan/overnight_run/plans/N6-01_breakout-after-longer-decline_1d.md`
Record: `steps_cards/04_backtest/overnight_run/backtests/N6-01_breakout-after-longer-decline_1d`
Measure: `measure.py`
