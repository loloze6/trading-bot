---
idea: 001-04_rsi-low-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: Compute the 14-bar Wilder RSI on daily closes. The forecast is short only and is graded by how far the RSI sits below 50. Raw value: (50 - RSI) x 0.4. Standardise it against the mean absolute value of its previous 60 values, using at least 20 of them; this puts it near 10 at an average deviation and caps it at 20. Negate it, so it is negative when RSI is below 50. Apply signed_power with exponent 2 and pivot 10, so mild readings shrink smoothly toward 0 and extreme low readings are amplified. Finally clip at a maximum of 0. The result is zero whenever RSI is 50 or above, and grows smoothly more negative the lower the RSI. A very low RSI therefore gives the largest short position.
Config: 001-04_rsi-low-extreme-continuation_1d_config.json
Confirm: The horizon is 5 bars. Pool all coins and windows and take non-overlapping 5-bar forward close-to-close returns, before costs. Compare returns after bars with RSI at or below 30 (the largest short positions) with returns after neutral bars (RSI between 40 and 60). The idea is confirmed if the mean return after low-extreme bars is lower by at least 1 percentage point, with a t-stat of -2 or lower, over at least 30 non-overlapping low-extreme samples. As a supporting check, the difference must be negative on at least 2 of the 3 coins.
Reject: The idea is rejected if, with at least 30 non-overlapping low-extreme samples, the mean 5-bar return after RSI ≤ 30 is equal to or higher than that after neutral readings (difference ≥ 0). A difference of +1 point or more with a t-stat of +2 or higher would point to reversal instead of continuation.
Inconclusive: Any of these neither confirms nor rejects the idea: - fewer than 30 non-overlapping low-extreme samples; - a negative difference smaller than 1 point, or with a t-stat between -2 and 0; - a pooled difference that meets the threshold while only 1 of the 3 coins shows it.
Deviation: "After RSI reaches a low extreme" becomes "while RSI is below 50, sized by the squared, standardised depth below 50". The config therefore also holds small shorts on mild sub-50 readings, and its position follows the RSI bar by bar rather than being a fixed hold after the extreme. The comparison of extreme against neutral readings is made in the criterion, not in the forecast.
