---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.d not profitable
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's next 20-day return rises with the number of days its close has spent above its 200-day average, more than with how far the close sits above it.
Consequence: Size a long by how long the coin has held above its average, not by its distance from it.
Why:
- F4: A larger forecast does not earn steadily more per unit of risk.
- F6: Bars 5-20 days into an above-SMA run have negative gross return (-0.00080 per day) and a 20-bar forward return of only 0.75%. Bars 60-120 days in earn 0.0045 per day and 6.0% over 20 bars.
- F3: Being above the SMA picks better bars only weakly. Coin daily return is 0.00162 on active bars and 0.00087 on flat bars, with t = 1.03. Flat bars (forecast 0) still earn a mean 20-bar return of 2.6%, against 2.4% for forecast 5-10. The 20-bar hit rate is below 50% in every bucket, from 0.39 to 0.43.
