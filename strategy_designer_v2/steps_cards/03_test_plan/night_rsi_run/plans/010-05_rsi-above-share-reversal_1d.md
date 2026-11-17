---
idea: 010-05_rsi-above-share-reversal
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 70a362722b07
---
Fidelity:
- Situation: share of the past 30 days that the 14-day RSI spent above 50 -> kept
- Comparison: a larger share against a smaller share -> kept
- Outcome: the coin's return over the next 14 days is lower -> kept
- Verdict transfer: yes: the forecast is the negated 30-bar share of RSI(14) above 50, so its link to 14-bar forward returns is the idea's claim itself.
Forecast: The forecast uses one indicator. It is the share of the last 30 daily bars on which the 14-day RSI was above 50, minus 0.5 (RsiAboveMidlineShareComponent: period 14, window 30, rsi_window 100, side "above"). It is standardised against its own past 60 values (20 minimum) and then negated. It is negative (short) when RSI held above 50 on more than half of the 30 bars. It is positive (long) when it held above 50 on fewer than half. It is zero at an even split. The size grows steadily with how far the share is from one half, capped at ±20.
Config: 010-05_rsi-above-share-reversal_1d_config.json
Criterion:
- Horizon: 14 bars
- Main measure: Take the bars on a non-overlapping 14-bar grid in each window, pooled over coins and windows. Regress each bar's 14-bar forward return, minus that coin's mean 14-bar return over all windows, on the bar's forecast, and test the slope with its t.
- Supporting check: The book's mean daily return minus its gain from the market's own rise (the timing part) is above 0, before costs.
- Confirm: The slope is positive with t ≥ 2 on at least 300 independent cases, and the supporting check passes.
- Reject: The slope is negative with t ≤ -2 on at least 300 independent cases.
- Inconclusive: Any of these is inconclusive: a slope t between -2 and 2; a positive slope with t ≥ 2 whose timing gain is not above 0; or fewer than 300 independent cases.
