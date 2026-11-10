---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: Take the 14-bar Wilder RSI on daily closes and measure how far it sits above 50 as (50 − RSI). Put that on the scale of its own past values: divide by the mean absolute value of the previous 60 readings and multiply by 10, capped at ±20. Then apply a smooth dead zone, 10 × sign × (|v|/10)², so ordinary readings shrink toward 0 and high extremes are amplified. Finally cap the result at 0 from above. The forecast is therefore never positive. It is zero whenever RSI is at or below 50. It is negative (short) while RSI is above 50, and the short grows with the square of how far RSI is above 50: a reading twice as stretched as usual gives a short four times as large, up to the −20 combined cap.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Confirm: Pool all three coins and all six windows. Take the bars where the short position is in the largest decile, and count the coin's 5-bar forward return only once per non-overlapping 5-bar block. The mean of those returns must be below the mean 5-bar forward return over all bars, by a margin with t ≤ −2. Supporting check: the same sign holds on at least 2 of the 3 coins.
Reject: Under the same measure, the mean 5-bar forward return after the largest-decile shorts is at or above the all-bar mean (t ≥ 0). That would mean high RSI extremes are followed by no retracement, or by continuation.
Inconclusive: The difference is negative but with −2 < t < 0. Also inconclusive: it reaches t ≤ −2 pooled but holds on only one coin.
Deviation: The idea says the reversal comes after RSI reaches an extreme. The config tests something different: it holds a short while RSI is above 50, sized by how stretched the reading is, and the short shrinks as RSI falls back toward 50 rather than lasting a fixed number of bars. Moderate high readings also carry small shorts, damped by the squared dead zone rather than excluded.
