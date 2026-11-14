---
idea: 001-03_rsi-high-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1d
data-period: fold A
---
Config: 001-03_rsi-high-extreme-continuation_config.json
Confirm: On the daily record for each of BTC, ETH and BNB, the mean 5-bar forward return after the bars with the largest long forecasts (top decile of the forecast, i.e. high RSI) is clearly above the mean 5-bar forward return after bars with small positive forecasts (neutral RSI). Mean 5-bar gains also rise with the size of the position across forecast buckets. The before-cost portfolio return per unit of average exposure beats buy-and-hold of the same coin, in all three coins or in a clear majority.
Reject: The mean 5-bar forward return after top-decile forecasts is at or below that after neutral bars, or is negative, so that gains do not rise with position size. Alternatively the before-cost portfolio does not beat buy-and-hold per unit of exposure, in most of the coins.
Inconclusive: Top-decile bars beat neutral bars in only one or two coins, or by a margin within sampling noise (the top decile has few, heavily overlapping 5-bar windows). The idea is also inconclusive if the portfolio beats buy-and-hold only because it is flat in falling markets while the high-RSI forward returns show no difference.
Deviation: "Reaches a high extreme" becomes "while RSI (14) is above 50, the position grows with the square of the RSI excess", i.e. a level and not an event, with no reference to the first touch of an extreme. The forecast is zero when RSI is at or below 50, so that there is no short side. Because the position is also nonzero at mild readings, "neutral" is read as small positive forecasts.
