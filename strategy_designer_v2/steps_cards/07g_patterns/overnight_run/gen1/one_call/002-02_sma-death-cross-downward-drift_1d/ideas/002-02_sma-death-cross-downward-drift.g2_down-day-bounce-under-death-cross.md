---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-02_sma-death-cross-downward-drift
line: 7.g patterns
backtest: 002-02_sma-death-cross-downward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 50-day SMA is below its 200-day SMA, a daily close that fell by more than half its recent daily volatility is followed by a next-day return above the coin's average.
Consequence: In death-cross regimes, take short-term longs after down days, or at least avoid adding shorts right after them.
Why:
- F3: After a down day (z-move below -0.5 of 20-day volatility), the next day's return beat the coin's mean by 0.41%, t = 3.89, 58.0% up, while the 50-day SMA was below the 200-day SMA. When it was not, the excess was 0.25%, t = 1.90. The bounce was positive in all six coins (t from 0.74 to 3.88), and up days were followed by slightly below-mean returns in four of six coins.
