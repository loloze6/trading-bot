---
idea: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation
brief: 013_anchoring-to-recent-high
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 70a362722b07
---
Fidelity:
- Situation: the daily close's distance to the highest high of the prior 30 days, including closes that clear it -> kept
- Comparison: closer to the high (or further through it) against further below it -> kept
- Outcome: the next 10 days' return is larger the closer the close sits to the high, and it keeps growing above it -> kept
- Verdict transfer: yes: the forecast is a monotone graded reading of the same signed distance, and it is judged on the 10-day forward return.
Forecast: The signal is DistanceFromHighComponent with period 30, source "high" and exclude_current 1. It gives (close − highest high of the prior 30 bars) / that high × 100. It is negative below the high, 0 at it, and grows positive as the close clears it. Standardise uses window 60 and min_periods 20, which gives about −10 at the usual distance below the high. A standardised BuyAndHold constant (+10) is added at equal weight. The forecast is therefore (x + 10) / 2: - It is 0 when the close sits at its usual distance below the high. - It is positive and growing as the close nears the high and then breaks through it, up to the cap. - It is negative and growing as the close falls further below the high than usual. It is fully graded and has no regime.
Config: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d_config.json
Criterion:
- Horizon: 10 bars
- Main measure: Regress the coin's 10-bar forward return, minus that coin's mean 10-bar return over all windows, on the recorded forecast. Use non-overlapping samples at positions 0, 10, 20, ... of each window, pooled over coins and windows. Report the slope's t-statistic.
- Supporting check: The mean excess 10-bar return of the top forecast quintile minus that of the bottom quintile, on the same samples, must be above 0.
- Confirm: The slope's t is 2 or more, and the top-minus-bottom quintile difference is positive.
- Reject: The slope's t is −2 or less.
- Inconclusive: Any slope t between −2 and 2, or a t of 2 or more with a quintile difference of 0 or below. At least 300 independent 10-bar cases are required; with fewer, the result is inconclusive.
