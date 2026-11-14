---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-01_breakout-drift-lasts
line: 7.d not profitable
backtest: N4-01_breakout-drift-lasts_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin's new 20-day closing high, its excess rise over the following days appears only while its close stays within a small distance of that high and above its 20-day average. Once the close falls below its 20-day average, the coin's following returns are at or below its average.
Consequence: Refuse to hold a breakout long once the coin has closed below its 20-day average, which removes the flat-to-losing held days inside the falls.
Why:
- F2: Held days whose close is below the 20-day mean earn nothing, while days well above it carry the gain. The two lowest quintiles of held coin-days by close/MA20 have next-day book returns of -0.0005 (t -0.48, n 2254) and -0.0005 (t -0.58, n 2254). The two highest quintiles have +0.0039 (t 2.97, n 2254) and +0.0070 (t 3.25, n 2254). These are pooled coin-days, not the book's daily mean over coins.
- F3: The drift lives only next to the high. On non-overlapping 10-bar samples of held bars, the excess return over the coin's all-window mean is +0.035 (t 2.73, n 266) when the close is within about 1.9% of its 20-day high. In the three quartiles further below the high it is -0.006 to -0.010 (t -0.73 to -1.19, n 266 to 267 each).
- F1: The book's Calmar of 0.44 fails because of long, deep falls while it stays long: the book was long on 73% of coin-bars. Its deepest fall reached -82.5%, measured over the windows run end to end. In w14 the book lost 68.9% with every coin down 41% to 84%. In w7 it lost 43.9% and in w9 47.1%, with five or six of the six coins losing.
