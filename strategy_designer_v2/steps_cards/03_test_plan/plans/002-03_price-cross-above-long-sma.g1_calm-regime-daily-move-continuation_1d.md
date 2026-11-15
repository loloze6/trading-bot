---
idea: 002-03_price-cross-above-long-sma.g1_calm-regime-daily-move-continuation
brief: 002_moving-average-cross-trend-persistence
data-instruments: BTC, ETH, LTC, XMR, XRP, ZEC
data-bar: 1d
data-period: folds A, B, C, D
outcome: plan
fit: adapted
---
Fidelity:
- Situation: a day's return that is large against the coin's own 20-day volatility, when that volatility is low -> adapted: "large" becomes graded, using the vol-scaled one-day return with a squared dead zone; "low volatility" is a regime (20-day vol percentile at or below the median of 100 bars).
- Comparison: the effect weakens or reverses as 20-day volatility rises -> kept: same-direction follow-through compared between low-vol bars and high-vol bars.
- Outcome: price moves the same way as the strong day over the next 5 days, more after larger scaled moves -> adapted: the 5-day holding period is dropped in the config; the criterion measures the 5-bar forward return.
- Verdict transfer: yes: the forecast follows the scaled day only in calm markets, and the record shows whether the next 5 bars follow it more than holding does, and more than in volatile markets.
Forecast: The regime detector computes the 20-day volatility percentile, ranked over 100 bars and smoothed with span 5. When that percentile is at or below 0.5 (calm), the active regime holds one component. That component is the day's return divided by the 20-day standard deviation of daily returns. It is standardised over 60 bars, then passed through signed_power with exponent 2 and pivot 10. The forecast is positive after an up day and negative after a down day. It grows with the square of the scaled move, so ordinary days sit near 0 and strong days give large positions. It is 0 whenever volatility is above its median.
Config: 002-03_price-cross-above-long-sma.g1_calm-regime-daily-move-continuation_1d_config.json
Criterion:
- Horizon: 5 bars
- Main measure: Sample calm-regime bars on the non-overlapping 5-bar grid. For each, take (forecast / 10) x (the coin's next 5-bar return minus the coin's mean 5-bar return over all windows). Report the mean of this product and its t-statistic.
- Supporting check: Take high-vol bars (vol percentile above 0.5) on the same grid. Compute the same product from the recorded standardised scaled_day value. The calm-bar mean minus the high-vol mean must be above 0.
- Confirm: The main-measure mean is positive with t >= 2, and the supporting check difference is above 0.
- Reject: The main-measure mean is negative with t <= -2.
- Inconclusive: Any t between -2 and 2 is inconclusive. So is t >= 2 when the supporting check fails. At least 100 calm grid cases are needed across coins and windows; with fewer, the result is inconclusive.
