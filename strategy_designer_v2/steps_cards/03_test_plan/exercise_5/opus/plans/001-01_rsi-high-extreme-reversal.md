---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: Use the 14-bar Wilder RSI on the daily close. Take 50 minus RSI, so the value is negative when RSI is above 50. Divide it by the mean absolute value of its own previous 60 readings and multiply by 10, capped at ±20 (standardise). Keep only the negative side, which covers readings above 50, so the forecast is zero whenever RSI is at or below 50. Then apply signed_power (exponent 2, pivot 10) so the short grows with the square of the reading's strength: a mild reading of -5 becomes -2.5, an average one of -10 stays -10, and an extreme one of -14 or beyond reaches the -20 cap. The forecast is never positive. It is zero when RSI ≤ 50 and grows more negative, smoothly, the further RSI sits above 50 relative to its recent typical distance from 50, so the largest shorts occur at the highest RSI extremes.
Config: 001-01_rsi-high-extreme-reversal_config.json
Confirm: Horizon is 5 bars. Take the bars where the forecast sits at the -20 cap and keep only those at least 5 bars apart, so each 5-bar window is counted once. The coin's 5-bar forward close-to-close return after those bars must be lower than its average 5-bar return over all bars of the same windows, which is the buy-and-hold drift. Pooled over BTC, ETH and BNB and all 6 windows, with at least 30 such observations, this excess must be negative with t ≤ -2, and it must be negative for at least 2 of the 3 coins. Supporting check: the mean excess after forecasts between -2 and -10 is less negative than after -20, so the retracement grows with the reading.
Reject: With at least 30 independent observations, the pooled excess 5-bar return after -20 forecasts is ≥ 0, meaning price keeps rising or matches its drift after high RSI extremes. The same holds if it is negative for fewer than 2 of the 3 coins with pooled t > -1.
Inconclusive: Any of the following: the pooled excess is negative with t between -2 and -1; fewer than 30 independent observations at -20; or the pooled t ≤ -2 but only one coin shows a negative excess.
Deviation: Four differences from the idea. (1) "After the RSI reaches a high extreme" becomes "while RSI is above 50", with the short sized by how far above. (2) "Extreme" is measured against RSI's own recent 60-bar typical distance from 50, not a fixed level such as 70, and it is judged at the -20 cap. (3) Mild above-50 readings carry small short positions instead of none. (4) Low (oversold) extremes are not tested.
