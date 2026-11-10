---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: The 14-bar Wilder RSI on daily closes, read as (50 - RSI). Only the high side counts, so the forecast is short only and zero whenever RSI is at or below 50. - Scaling: standardise the reading against the mean absolute value of its previous 60 bars, so a typical reading is about 10. - Short side only: clip the result at a maximum of 0. - Emphasising extremes: apply a signed square around pivot 10. Moderate readings (RSI just above 50) are damped smoothly towards 0, and extreme readings (RSI in the 70s and 80s) are amplified. - Size and sign: the short position grows continuously with how far RSI is above 50, and is largest at the highest RSI readings. The forecast is never positive.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Confirm: The test uses a 5-bar horizon. Take the bars in the top decile of short size (largest |forecast|), pooled over the 3 coins and 18 windows, sampled so that no two 5-bar forward returns overlap. On those bars, the coin's forward 5-bar close-to-close return, minus the coin's unconditional mean 5-bar return over the same windows, averages -1.0% or lower with a t-statistic of -2 or lower, before costs. Supporting check: the excess has the same negative sign on at least 2 of the 3 coins.
Reject: The same pooled, non-overlapping mean excess 5-bar return after top-decile short bars is 0 or higher (no reversal, or continuation).
Inconclusive: A pooled mean excess between -1.0% and 0. A mean of -1.0% or lower with a t-statistic between -2 and 0. A negative pooled excess that is negative on only 1 of the 3 coins.
Deviation: "After RSI reaches a high extreme" becomes "while RSI is above 50, sized up sharply as it rises". There is no fixed extreme threshold such as 70, and the position exists only while RSI stays elevated, not for a set number of bars after the extreme.
