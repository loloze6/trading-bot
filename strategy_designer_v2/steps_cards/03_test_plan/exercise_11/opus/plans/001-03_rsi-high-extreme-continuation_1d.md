---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: Take RSI(14), the Wilder RSI on daily closes. The component outputs (50 − RSI) × 0.4, and this is flipped so it reads (RSI − 50) × 0.4. That value is standardised: divided by the mean absolute value of its previous 60 values and multiplied by 10, capped at ±20. It is then passed through signed_power with exponent 2 and pivot 10, so moderate readings shrink smoothly toward 0 and extreme readings grow. Finally it is clipped at a minimum of 0. The forecast is therefore zero whenever RSI ≤ 50. It is positive (long) when RSI > 50, and grows with the square of how far RSI sits above 50 compared with its recent typical distance. The largest long positions come when RSI is at a high extreme (about 70 and up). It is never negative.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Confirm: Horizon 5 bars. The main measure, before costs, uses all 3 coins × 6 windows pooled, taking non-overlapping samples (at most one sample every 5 bars per coin). From the recorded RSI component value it compares two groups: the mean 5-bar forward close-to-close return after high-extreme bars (raw value ≤ −8, i.e. RSI ≥ 70) and the mean after neutral bars (raw value between −4 and +4, i.e. RSI 40–60). The idea is confirmed if the high-extreme mean exceeds the neutral mean by at least +1.0%, with t ≥ 2. This needs at least 30 non-overlapping extreme samples, and the difference must be positive on at least 2 of the 3 coins. The supporting check is that the strategy's return per unit of average exposure exceeds the coin's buy-and-hold daily return.
Reject: The idea is rejected if the pooled difference (high-extreme minus neutral 5-bar forward return) is ≤ 0 with at least 30 non-overlapping extreme samples. A significantly negative difference (t ≤ −2) would further point to reversal rather than continuation.
Inconclusive: The test is inconclusive in any of these cases: a positive difference below +1.0%; a difference with t < 2; fewer than 30 non-overlapping extreme samples; or a positive result on only one coin.
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50". The position is sized by the squared distance of RSI above 50, relative to its last 60 bars, so a reading near 70 counts as extreme only relative to recent RSI behaviour. Low extremes are not traded.
