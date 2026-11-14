---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: Use the 14-bar RSI on daily bars, through RSIPullbackComponent (period 14, long_only false). Its raw value is (50 − RSI) × 0.4. This value is standardised against its own past 60 values (target 10, cap 20, min_periods 20) and then negated, so it rises with RSI above 50. It is then clipped at 0, so the forecast is zero whenever RSI ≤ 50. Finally it goes through signed_power with exponent 2 and pivot 10. That step damps readings just above 50 towards zero and amplifies high readings. The forecast is never negative. It is near 0 for neutral readings and grows smoothly, roughly with the square of how far RSI sits above 50 relative to its usual distance. Strong overbought readings (RSI around 70–80+) reach the cap of +20, which is a 200% long position.
Config: 001-03_rsi-high-extreme-continuation_config.json
Confirm: - Horizon: 5 bars, using the recorded RSI component value. Extreme bars have RSI ≥ 70 (raw ≤ −8); neutral bars have RSI 40–60 (|raw| ≤ 4). - Main measure: the mean 5-bar forward close-to-close return after extreme bars minus the mean after neutral bars. Returns are sampled non-overlapping, so each 5-bar block counts once, and pooled over the 3 coins and 6 windows, before costs. - Confirm if: the difference is positive with t ≥ 2, from at least 30 non-overlapping extreme observations, and is positive in at least 2 of the 3 coins. - Supporting check: the strategy's total return beats buy-and-hold scaled to the strategy's average exposure.
Reject: Reject if the pooled difference (extreme minus neutral 5-bar forward return) is ≤ 0. If it is negative with t ≤ −2, that points to reversal instead. Also reject if it is negative in at least 2 of the 3 coins.
Inconclusive: The result is inconclusive in these cases: - the difference is positive but t < 2; - there are fewer than 30 non-overlapping extreme observations; - the difference is positive in only one coin.
Deviation: - "After RSI reaches a high extreme" becomes "while RSI is above 50", with the position growing with the squared distance above 50. A small position is held on mildly elevated readings, not only on extremes. - The position follows RSI down instead of being held for a fixed number of bars after the extreme. - Low extremes are flat by design.
