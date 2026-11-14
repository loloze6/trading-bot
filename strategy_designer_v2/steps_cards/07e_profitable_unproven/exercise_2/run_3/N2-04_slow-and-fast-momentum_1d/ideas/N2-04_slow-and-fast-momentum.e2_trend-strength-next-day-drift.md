---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-04_slow-and-fast-momentum
line: 7.e profitable but not proven
backtest: N2-04_slow-and-fast-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's medium and slow returns are both positive, the further those returns stand above their own usual size, the larger the coin's rise over the next day.
Consequence: In an established up-trend, a trader should size the next-day long by how unusually strong the trend's returns are.
Why:
- F2: The idea's excess return on active bars is real at short horizons and fades by the plan's 20 bars. Mean excess over the coin's mean, non-overlapping, by horizon:
- F6: The strength of the signal grades the 1-bar move. The 1-bar excess rises from 0.00056 (t 0.53) in the lowest forecast tercile to 0.00209 in the middle tercile and 0.00299 (t 2.15) in the highest, n about 1900 each. This grading is absent at 5 bars, where the Spearman correlation of the forecast with the excess is -0.003.
