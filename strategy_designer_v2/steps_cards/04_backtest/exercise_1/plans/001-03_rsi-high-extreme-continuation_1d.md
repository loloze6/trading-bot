---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: Compute the 14-bar Wilder RSI on daily closes. The raw component value is (50 − RSI) × 0.4. Standardise it against the mean absolute value of its previous 60 values (target 10, cap 20). Negate it, so the reading is positive when RSI is above 50. Clip it at 0, so the forecast is zero whenever RSI ≤ 50. Then apply signed_power with exponent 2 and pivot 10: a mild reading is damped smoothly towards 0 and a strong one is amplified. The result is a long-only forecast. It is zero at or below RSI 50 and grows continuously as RSI rises above its usual distance from 50. The largest positions come at the highest RSI extremes, and the combined forecast is capped at +20.
Config: 001-03_rsi-high-extreme-continuation_1d_config.json
Confirm: Horizon is 5 bars. Take non-overlapping 5-bar blocks, sampling every 5th bar, so overlapping returns are counted once. Pool the three coins and six windows. The main measure is the coin's mean forward 5-bar return after "extreme" bars minus its mean after "neutral" bars: - "Extreme" bars are those whose forecast is in the top 20% of that coin's bars. - "Neutral" bars are those where the recorded raw indicator has |value| ≤ 4, which means RSI is between 40 and 60. The idea is confirmed if this difference is positive with a t-statistic ≥ 2 and is positive for at least 2 of the 3 coins. The supporting check is that the Spearman correlation between the forecast and the forward 5-bar return, on bars with forecast > 0, is positive. All of this is judged before costs.
Reject: The idea is rejected if the pooled extreme-minus-neutral 5-bar forward return difference is zero or negative. This covers the reversal case, a significantly negative difference with t ≤ −2, as well as no difference at all.
Inconclusive: The result is inconclusive if the difference is positive but its t-statistic is below 2. It is also inconclusive if the difference is significant pooled but positive in only one of the three coins.
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50, sized by how far above it is". There is no fixed 70 threshold. Instead, "extreme" is measured against the RSI's own distance from 50 over the previous 60 bars and emphasised by the squaring. The low-extreme (short) side of the brief is not traded.
