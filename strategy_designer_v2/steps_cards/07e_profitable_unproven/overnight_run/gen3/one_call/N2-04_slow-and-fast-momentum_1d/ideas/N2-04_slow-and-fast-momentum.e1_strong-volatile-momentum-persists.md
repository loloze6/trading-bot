---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-04_slow-and-fast-momentum
line: 7.e profitable but not proven
backtest: N2-04_slow-and-fast-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin is up over both 20 and 60 days and its 20-day return is unusually large against its own recent history, while its 20-day volatility is in its upper range, its next days rise more than its average.
Consequence: Take momentum longs only when the trend is strong relative to the coin's own past and volatility is high, and pass on the weak, just-turned-up trends that carry little or no edge.
Why:
- F1: The book earns from timing, not only from the coins' drift: it held about 30–38% of bars, and its return while held beat drift × exposure on all six coins (timing excess ZEC 5.73, ETH 4.01, BTC 3.57, XRP 2.63, LTC 0.78, XMR 0.66). Held days returned 0.00176 per day above each coin's mean (t 2.56, n 5886 daily bars). Over non-overlapping 5-bar blocks, held blocks returned +0.0081 above the coin mean (t 2.21, n 1164) and flat blocks returned −0.0039 (t −1.80, n 2255).
- F2: The edge sits in the strongest third of the signal: held-day excess rises from 0.0005 (t 0.52, n 1962) in the lowest forecast tercile to 0.0016 (t 1.41, n 1960) in the middle and 0.0031 (t 2.31, n 1964) in the highest. The verdict's own slope of 20-bar excess on forecast is also positive (0.0040).
- F3: The edge is strongest in high volatility: held-day excess is 0.0035 (t 2.30, n 1689) in the coin's top 20-day-volatility tercile, against 0.0013 (t 1.34, n 1546) in the bottom tercile and 0.0016 (t 1.48, n 1799) in the middle.
