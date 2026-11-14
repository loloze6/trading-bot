---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: Short only, and only on the high side of the RSI. Compute the 14-bar Wilder RSI on daily closes and take (50 − RSI). This is 0 at RSI 50 and negative when RSI is above 50. Divide it by the mean absolute value of the 60 readings before the current bar and multiply by 10, capped at ±20; this puts it on the forecast scale. Set every positive value (RSI below 50) to 0, so the forecast is zero whenever the index is not elevated. Then apply a graded dead zone, 20 × sign × (|v|/20)²: - a mildly elevated RSI gives a small short (−10 becomes −5); - the largest readings give the largest short (−20 stays −20, a 200% short). The forecast is never positive and grows in size continuously as RSI rises further above 50 relative to its recent range.
Config: 001-01_rsi-high-extreme-reversal_config.json
Confirm: - Main measure, horizon 5 bars. Pool all 3 coins × 6 windows. Take bars where the forecast is ≤ −10, about the strongest RSI readings, sampled at most once per 5-bar block so overlapping returns count once. Their mean 5-bar forward close-to-close return, minus the mean 5-bar forward return of all bars in the same coin-window (the buy-and-hold drift), must be ≤ −1.0%, with a t-statistic ≤ −2. - Coin agreement. The excess must be negative in at least 2 of the 3 coins. - Supporting check. The strategy's summed before-cost return over the 18 coin-windows is positive.
Reject: The pooled excess 5-bar forward return after forecast ≤ −10 bars is ≥ 0 (price does not fall more than usual after high RSI). If it is positive with t ≥ +2, this is evidence for continuation instead.
Inconclusive: - The excess is negative but smaller than 1.0% in size, or its t-statistic lies between −2 and 0. - Fewer than 30 non-overlapping extreme samples exist. - The coins disagree in sign, with only 1 of 3 negative.
Deviation: - Timing. "After RSI reaches a high extreme" becomes "while RSI is above 50". The short is held and sized continuously by how far RSI is above 50, with no fixed extreme threshold; the dead zone only damps the moderate readings. - Relative scale. "Extreme" is measured relative to the mean absolute RSI deviation of the previous 60 bars, not as a fixed level such as 70. - Low side. The low-extreme (oversold) side of the brief is not tested by this idea.
