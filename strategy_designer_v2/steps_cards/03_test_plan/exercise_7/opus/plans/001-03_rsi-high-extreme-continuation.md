---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: Take the 14-bar Wilder RSI on daily closes and use how far it sits above 50 (RSI − 50) as the signal. This is RSIPullbackComponent(14), which outputs (50 − RSI) × 0.4, with its sign flipped. Standardise it against its own previous 60 values (min_periods 20). Then clip it at 0, so only RSI above 50 is held. Then apply signed_power with exponent 2 (pivot 10): readings near 50 are pushed towards 0 and high readings are amplified. The forecast is 0 whenever RSI ≤ 50 and never negative. Above 50 it is positive and grows with the square of the standardised distance, reaching the +20 cap (200% long) at strongly overbought readings such as RSI ≈ 70 or above. Low-RSI extremes are not part of this idea and give no position.
Config: 001-03_rsi-high-extreme-continuation_config.json
Confirm: The horizon is 5 bars, measured before costs. Recover RSI from the recorded indicator value as 50 − value / 0.4, and sample every 5th bar so no 5-bar return is counted twice. Pool all coins and windows. The idea is confirmed if the mean 5-bar forward return of the coin after extreme bars (RSI ≥ 70, where the forecast is largest) exceeds the mean after neutral bars (RSI 40–60) by a positive amount with a t-statistic ≥ 2. This needs at least 30 non-overlapping extreme observations, and the difference must be positive in at least 2 of the 3 coins. Supporting check: the portfolio's return must exceed (average allocation × the coin's buy-and-hold return) over the same windows.
Reject: The idea is rejected if the pooled difference (extreme minus neutral 5-bar forward return) is zero or negative. It is also rejected if the difference is negative in 2 or more of the 3 coins.
Inconclusive: A positive pooled difference with a t-statistic below 2. Also inconclusive: fewer than 30 non-overlapping extreme observations, or a positive pooled difference carried by a single coin.
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50, sized by how far above". Moderate readings (RSI just above 50) also take small long positions, and the position is held for as long as RSI stays high rather than for a fixed number of bars after the extreme. Low-RSI extremes are left flat.
