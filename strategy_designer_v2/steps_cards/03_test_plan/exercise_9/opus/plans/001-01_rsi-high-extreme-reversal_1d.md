---
idea: 001-01_rsi-high-extreme-reversal
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Forecast: Uses the 14-bar Wilder RSI on daily closes (the standard setting). The raw reading is (50 - RSI) x 0.4. Each value is divided by the mean absolute value of the 60 readings before it and multiplied by 10, capped at +/-20. All positive values are then removed (clip at a maximum of 0), so the forecast is zero whenever RSI is at or below 50. It is negative (short) when RSI is above 50. A signed power with exponent 2 and pivot 10 is applied next. This keeps moderate readings small (a standardised -5 becomes -2.5). It makes extreme readings large (-15 becomes -22.5), and the combined forecast is clipped at -20. The short position therefore grows smoothly with how far RSI is above 50, and most of it sits at the high extremes. It never goes long.
Config: 001-01_rsi-high-extreme-reversal_1d_config.json
Confirm: The test uses the 5-bar forward close-to-close return of the coin, before costs. Only bars where the forecast is -10 or lower (the high-RSI extremes) count, sampled at most once every 5 bars so overlapping returns are counted once. Their mean return minus the mean 5-bar return of all bars in the same window is the main measure. The idea is confirmed if this excess is negative, has a pooled t-stat of -2 or lower across all coins and windows, and is negative for at least 2 of the 3 coins. The supporting check is that the strategy's portfolio value, before costs, ends the windows above a portfolio that holds a short of the same average size in the coin.
Reject: The idea is rejected if the pooled excess 5-bar return after forecasts of -10 or lower is positive with a t-stat of +2 or higher (continuation). It is also rejected if it is positive for at least 2 of the 3 coins.
Inconclusive: A pooled t-stat between -2 and +2 is inconclusive. So is fewer than 30 non-overlapping extreme bars in total. So is a negative pooled excess that holds in only one coin.
Deviation: "After RSI reaches a high extreme" is tested as "while RSI is above 50, sized by how far above". The short is held only while the reading stays elevated, and it shrinks as RSI falls back. A reversal that happens after RSI has dropped back below 50 is therefore not captured in the portfolio. It is still captured in the 5-bar forward-return measure. Moderate readings above 50 also carry a small short.
