---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-01_breakout-drift-lasts
line: 7.d not profitable
backtest: N4-01_breakout-drift-lasts_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The rise after a new 20-day closing high is larger when the coin's 50-day average is rising at that bar's close than when it is falling.
Consequence: Take breakout longs only when the 50-day average is rising, and stay flat through the falling-average stretches that make up the deep windows.
Why:
- F4: Held days with a falling 50-day average carry almost none of the book's gain. These 3695 held coin-days have a mean next-day book return of 0.0001 and contribute 0.08 of summed per-coin book return. The 5456 held days with a rising 50-day average have a mean of 0.0042 and contribute 3.84. This split is pooled coin-days, not the book's daily mean over coins.
- F6: Entries made with the close below the 50-day average lose. These trades average -5.7% (median -7.4%, 27.5% winners, n 305), against +3.0% to +6.4% for the other quintiles.
- F1: The book's Calmar of 0.44 fails because of long, deep falls while it stays long: the book was long on 73% of coin-bars. Its deepest fall reached -82.5%, measured over the windows run end to end. In w14 the book lost 68.9% with every coin down 41% to 84%. In w7 it lost 43.9% and in w9 47.1%, with five or six of the six coins losing.
