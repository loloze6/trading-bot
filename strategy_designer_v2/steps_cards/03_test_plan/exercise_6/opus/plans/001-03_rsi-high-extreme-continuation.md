---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: Use the 14-bar Wilder RSI on daily closes, through RSIPullbackComponent (period 14, long_only false). Its raw value is (50 − RSI) × 0.4. Standardise it: the latest value times 10, divided by the mean absolute value of the 60 stored values before it (min_periods 20), capped at ±20. Negate it, so it is positive when RSI is above 50. Clip it at a minimum of 0, so it is zero whenever RSI is 50 or below. Then apply signed_power with exponent 2 and pivot 10: small readings are damped smoothly towards 0 and extreme readings are amplified. The forecast is long only and graded. It is zero at RSI ≤ 50 and grows with the square of how far RSI sits above 50, measured against the coin's own recent RSI swings. A typical high extreme (RSI around 65–70) takes it near or to the +20 cap. Readings near 55 give about +2. The forecast is never negative. There is no regime gate.
Config: 001-03_rsi-high-extreme-continuation_config.json
Confirm: Horizon is 5 bars, using the forward 5-bar close-to-close return. - Extreme bars: forecast ≥ 10. - Neutral bars: RSI between 40 and 60, which is a raw rsi_strength value between −4 and +4. - Sampling: each side keeps only one bar per 5 bars (no overlapping returns), pooled over the 3 coins and 6 windows. - Main measure: extreme-bar mean forward return minus neutral-bar mean forward return. - Confirmation: that difference is above 0 with t ≥ 2, and it is positive for at least 2 of the 3 coins. - Supporting check: the strategy's before-cost return beats an exposure-matched hold, which is the bar-by-bar mean allocation times the coin's return over each window.
Reject: The idea is rejected if the pooled difference (extreme minus neutral) is ≤ 0 with at least 30 non-overlapping extreme observations. A significantly negative difference (t ≤ −2) would point to reversal instead.
Inconclusive: These results neither confirm nor reject: - a positive difference with t below 2; - a positive pooled difference carried by only one coin; - fewer than 30 non-overlapping extreme observations pooled.
Deviation: - "After RSI reaches a high extreme" becomes "while RSI is above 50", sized by the squared distance above 50. - Mildly strong readings therefore hold small positions instead of none. - "Extreme" is judged against the coin's own last 60 bars of RSI swings, not a fixed 70 level. - Low extremes are left flat, because the idea concerns only high readings.
