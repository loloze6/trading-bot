---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 50-day SMA is above its 200-day SMA, its return over the next 10 days is larger the larger its own 20-day return, so the uptrend persists only where price is still climbing and reverses where it has stalled.
Consequence: Inside a golden-cross regime, a trader would size long exposure by the coin's recent 20-day climb rather than by the width of the averages' spread, and would stay out of uptrends whose price has stopped rising.
Why:
- F2: While the 50-day SMA is above the 200-day SMA, the next 10-day excess return splits by the coin's own 20-day return, so the two sides cancel in the pooled slope. In the top tercile of 20-day return it is +0.032 (t 2.22, n 242). In the bottom tercile it is -0.021 (t -2.15, n 225). Below the 200-day average, no tercile reaches |t| 1.2.
- F3: The forecast does not grade the move. Excess 10-day return across forecast quartiles runs -0.0094, +0.0049, +0.0060, +0.0006 (n 208 each). The spread within each quartile is 0.15 to 0.22, about 20 times the gaps between quartiles. On-bars against off-bars differ by only +0.0011 (Welch t 0.14, 832 vs 825 blocks).
- F1: The forecast's slope on excess forward returns is flat at every horizon tried: t is 0.20, 0.37, 0.55 and -0.06 at 5, 10, 20 and 40 days (n = 3349, 1657, 811, 388), and the raw 50/200 spread gives t between -0.76 and 0.02. The plan's 10-day horizon is not hiding an effect that shows at another horizon.
