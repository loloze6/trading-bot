---
idea: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets
brief: 010_rsi-midline-regime-direction
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: exact
catalogue: 69355866607f
---
Fidelity:
- Situation: the share of the past 30 days that the 14-day RSI spent above 50 -> kept
- Comparison: the coin's 30-day volatility of daily returns is low against its own history -> kept: a regime where the volatility rank (30-bar volatility within its last 100 values) is at or below 0.5; flat elsewhere
- Outcome: a larger share gives a higher return over the next 14 days -> kept
- Verdict transfer: yes: the forecast is the RSI share itself, active only in low-volatility bars and scored on 14-day forward returns, so a confirm or a reject carries over to the idea.
Forecast: The forecast is the share of the last 30 daily bars on which the 14-day RSI was above 50, minus 0.5. It is scaled by its own past 60 values to an average size of about 10, capped at ±20. It is positive when RSI spent more than half the 30 days above 50, negative when less, and grows with that share. It is active only while the 30-day return volatility ranks at or below the median of its last 100 values (unsmoothed rank). On every other bar it is zero (flat).
Config: 010-01_rsi-above-share-continuation.g1_rsi-share-continuation-calm-markets_1d_config.json
Criterion:
- Horizon: 14 bars
- Main measure: On the non-overlapping 14-bar grid of each window, take the bars in the trending regime with a non-zero forecast. Regress the coin's 14-bar forward return minus that coin's mean 14-bar return over all windows on the forecast, pooled across coins. Measure the t of the slope.
- Supporting check: Over the trending-regime bars, the book's mean daily return minus its gain from the market's own rise (the timing part) is above 0.
- Confirm: The slope's t is 2 or more and the timing part is above 0.
- Reject: The slope's t is -2 or less.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is a t of 2 or more with a timing part of 0 or less. At least 100 independent grid cases are needed, otherwise the result is inconclusive.
