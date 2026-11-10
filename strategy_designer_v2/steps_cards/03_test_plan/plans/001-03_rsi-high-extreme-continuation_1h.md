---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
---
Forecast: Take the 14-bar Wilder RSI of the hourly close and measure how far it sits above 50 (RSI − 50; the component outputs 50 − RSI, which is then sign-flipped). Divide that distance by its mean absolute value over the previous 60 bars and multiply by 10, capping the result at ±20. Drop the negative side, so the forecast is 0 whenever RSI is at or below 50. Then apply signed_power with exponent 2 and pivot 10. This shrinks moderate readings smoothly toward 0 and enlarges high ones, so the long position grows with the square of how high RSI is. Readings near neutral give almost no position, and the largest positions come at the highest RSI readings. The forecast is never negative, and the combined forecast is clipped at +20.
Config: 001-03_rsi-high-extreme-continuation_1h_config.json
Confirm: Horizon is 24 bars. Take the bars in the top decile of the recorded forecast, per coin and window, and keep only non-overlapping events at least 24 bars apart. Their mean forward 24-bar log return must exceed the mean forward 24-bar return after neutral bars (raw RSI component value between −2 and +2, i.e. RSI 45–55, also thinned to be 24 bars apart). The difference must be positive with a pooled t-statistic ≥ 2 across the 3 coins × 6 windows, and positive in at least 2 of the 3 coins. Supporting check, before costs: the strategy's return per unit of average exposure beats the coin's buy-and-hold return over the same windows.
Reject: The pooled difference is at or below zero, meaning returns after the highest RSI readings are no higher than after neutral readings. A t-statistic ≤ −2 additionally points to reversal, not continuation.
Inconclusive: The difference is positive but the t-statistic is below 2. Also inconclusive: a t-statistic ≥ 2 where fewer than 2 of the 3 coins show a positive difference.
Deviation: "After RSI reaches a high extreme" is tested as "while RSI is above 50", with position size growing with the square of the distance; there is no fixed extreme threshold such as 70. "Extreme" is measured relative to the RSI's own last 60 hourly readings, not on the absolute RSI scale. Only the upward side is tested; no short is taken at low readings. The comparison with neutral readings is made in the criterion, not in the forecast.
