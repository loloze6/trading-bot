---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.d not profitable
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's close sits below its 200-day average, and the more it has fallen over the past weeks, the more it rises over the following days. Its distance below the long average marks exhaustion of the fall, not the continuation of a trend.
Consequence: A trader should refuse to short a coin that is deep below its long average after a sharp fall, and can look to buy it for a rebound that grows with the depth of the fall.
Why:
- F2: The short loses most where the forecast is strongest. Short days in the lowest 20-bar momentum quintile (the coin fell most over the prior 20 bars) earn -0.001288 a day (t -1.91, n 1669) at a mean allocation of -0.44. The upper two quintiles earn +0.000058 and -0.000009, so even the short's best states only break even.
- F3: The deepest distances below the 200-day average are where the coin rebounds. In the deepest distance quartile, the excess 10-bar return after short blocks is +0.0074 (n 233), and the block gain is -0.0040. The shallower quartiles show excess returns of -0.0071 and -0.0072.
- F4: The forecast's grading points the wrong way. The slope of excess 10-bar return on allocation is -0.0126, and the deepest forecast quartile (mean allocation -0.75) has a block gain of -0.0067 (t -0.92). The Spearman correlations of daily gross gain with distance, 20-bar momentum and 5-bar momentum are only 0.010, 0.036 and 0.050.
- F5: The book's worst days come from shorting after a crash. The worst 5% of short days (418) sum to -21.56, against a total of -3.77 over all short days. On those days the coin had fallen -14.0% over 20 bars (against -2.0% on all short days) and sat -34.2 below its average (against -15.3).
- F6: The losses cluster in rebound years. Short-block gains are t -3.26 in 2020, -2.65 in 2021 and -2.13 in 2023, against +1.59 in 2018, +2.02 in 2019 and +1.42 in 2022. That is why the Sharpe with one window left out stays negative (-0.70).
