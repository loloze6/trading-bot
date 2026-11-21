---
idea: 020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds
brief: 020_support-and-resistance-at-past-turning-prices
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
catalogue: e48527ec0eac
---
Fidelity:
- Situation: close far below a price where the coin turned up several times in the past 90 days -> adapted: "far below" and "several times" are made graded as touch count × percent depth under the level (TouchWeightedSupportBreakDepthComponent, 90 bars).
- Comparison: deeper close and more times the level held give a larger rise -> kept: the forecast grows with both depth and touch count.
- Outcome: the coin rises over the next 5 days -> kept: long position held 5 daily bars.
- Verdict transfer: yes: the forecast measures the stated situation and its strength, and is judged on the stated 5-day rise.
Forecast: One component, TouchWeightedSupportBreakDepthComponent (period 90, side 2, band 2.0), computed on every bar. It finds the most-touched swing-low level at or above the close. Its value is the touch count times the close's percent depth below that level, and it is 0 when the close is above every swing low. The component is standardised against its own past 90 values (min_periods 22). It is then passed through signed_power with exponent 3 and pivot 20, the strongest graded dead zone, so ordinary readings sit near 0 and only deep breaks of much-touched levels give a large long. The forecast is never negative: flat when no support is broken, and it grows smoothly with depth × touches up to +20.
Config: 020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: The cases are the bars on each window's non-overlapping 5-bar grid where the forecast is above 0. Among them, take the top fifth by forecast, pooled over coins and windows. For each, take the coin's 5-bar return from that close minus the coin's mean 5-bar return over all its windows (the unusual move). Measure the mean of these and its t.
- Supporting check: none
- Confirm: The mean unusual 5-bar return of the top-fifth cases is above 0 with t ≥ 2, on at least 30 cases.
- Reject: The mean unusual 5-bar return of the top-fifth cases is below 0 with t ≤ -2, on at least 30 cases.
- Inconclusive: Any t between -2 and 2, or fewer than 30 top-fifth cases, neither confirms nor rejects.
