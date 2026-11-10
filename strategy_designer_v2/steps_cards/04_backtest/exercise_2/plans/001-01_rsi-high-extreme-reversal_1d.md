---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: Take the 14-bar Wilder RSI on daily closes and form (50 − RSI). Standardise it: divide by the mean absolute value of its previous 60 daily readings and multiply by 10, capped at ±20. Clip at a maximum of 0, so only the overbought side (RSI above 50) trades. Then apply signed_power with exponent 2 and pivot 10. Readings near RSI 50 shrink smoothly towards 0, and high readings grow (standardised −15 becomes −22.5, and the combined forecast is clipped at −20). The forecast is never positive. It is zero whenever RSI is at or below 50 and negative (short) whenever RSI is above 50. It grows in size with the square of how far RSI sits above 50 compared with its recent typical distance, so the largest shorts sit at the highest RSI readings.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Confirm: The horizon is 5 bars. Take the bars where the forecast is −10 or lower (the strongest overbought readings), keeping only one per 5-bar block so that overlapping returns are counted once, and pool all coins and windows. Over those bars, the mean forward 5-bar close-to-close return, minus the mean forward 5-bar return over all bars of the same coin and window, is −1% or lower, from at least 30 such observations. The excess has the same sign in at least 2 of the 3 coins. Supporting check: the short-only strategy's pre-cost return, summed over all windows and coins, is positive.
Reject: With at least 30 non-overlapping observations, the pooled excess forward 5-bar return after forecast ≤ −10 is 0 or higher. That means price after high RSI does as well as or better than average. An excess of +1% or more would point to continuation instead.
Inconclusive: The pooled excess lies between −1% and 0. Or there are fewer than 30 non-overlapping strong-forecast observations. Or the excess is −1% or lower pooled, but the coins disagree in sign.
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50, sized by the square of how far above". No fixed extreme threshold is used. Mildly overbought bars also carry small short positions, and the position stays on for as long as RSI stays high instead of over a fixed number of bars after the extreme. The oversold side of the brief is not tested.
