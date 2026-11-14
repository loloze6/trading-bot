---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.g patterns
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close sits far below its 200-day simple moving average, its price rises over the following ten days rather than continuing down.
Consequence: Deep distance below the long average should be read as a place to stop shorting, not to add to shorts.
Why:
- F3: While the close is below its 200-day SMA, the 10-bar forward return is positive in every distance decile. It is +1.26% to +1.66% (t 3.0 to 4.8) in the three deepest deciles, down to 72.9% below the average. At the strongest forecast (below -10) it is +1.54% (up 54.7%, t 5.45). Only 2018 (-2.6%, t -5.2) and 2022 (-1.0%, t -3.2) are negative years, so the short book sits against a rebound rather than a downtrend.
- F4: All 2,471 trades were shorts, with a mean net result of -4.0%. Shorts lasting up to 20 days average -6.3% to -6.6% (n 1,764, medians around -5%). Only shorts lasting more than 20 days gain, +1.95% (n 707).
- F6: The book's worst 5% of days came after a coin down day averaging -2.2% (59% of them down days). Its best 5% came after a flat day (+0.09%). At both tails the short was about equally deep (allocation about -1.5, distance about -37%), which matches F1: shorts held into a fresh drop lose on the rebound.
