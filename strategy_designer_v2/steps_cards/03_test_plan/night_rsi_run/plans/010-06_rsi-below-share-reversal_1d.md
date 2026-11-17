---
idea: 010-06_rsi-below-share-reversal
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 70a362722b07
---
Fidelity:
- Situation: share of the past 30 days that the 14-day RSI spent below 50 -> kept
- Comparison: a larger share against a smaller share -> kept: the forecast grows with the share, centred at half the window
- Outcome: a higher return over the next 14 days -> kept: the forward 14-bar return is compared with the forecast's size
- Verdict transfer: yes: the forecast is the idea's own graded measure and the outcome is the idea's own horizon, so a confirm or a reject carries over to the idea.
Forecast: The forecast uses one component, RsiAboveMidlineShareComponent with RSI period 14, window 30, rsi_window 100 and side "below". Its raw value is the share of the last 30 daily bars on which RSI(14) was below 50, minus 0.5. The value is standardised over its last 130 values. The forecast is positive and long when RSI spent more than half of the last 30 days below 50, and the position grows as that share approaches 100 percent. It is negative and short when RSI spent less than half below 50. It is zero at exactly half. It moves in steps of 1/30 of the share, which keeps it graded.
Config: 010-06_rsi-below-share-reversal_1d_config.json
Criterion:
- Horizon: 14 bars
- Main measure: The slope of the coin's forward 14-bar return, minus that coin's mean 14-bar return over all windows, regressed on the forecast. Samples are pooled over coins on the non-overlapping 14-bar grid of each window, using only bars with a non-zero forecast. The slope is tested with its t-statistic.
- Supporting check: The book's timing gain is positive before costs. This is its mean daily return minus the part due to the market's own rise, which is the position held times the coin's mean daily return.
- Confirm: The slope is positive with t ≥ 2, and the timing gain is above 0.
- Reject: The slope is negative with t ≤ -2.
- Inconclusive: Any t between -2 and 2 is inconclusive, as is a slope with t ≥ 2 whose timing gain is not above 0. At least 100 non-overlapping cases with a non-zero forecast are required; about 600 are expected.
