---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While the 50-day average is above the 200-day average and the coin's recent volatility is in its upper range, the coin's forward return is higher than when volatility is in its calm range.
Consequence: A trader should hold the trend long mainly when volatility is high and cut it back in calm stretches.
Why:
- F9: Invested bars in the calmest third of volatility earn the coin only 0.000469, against 0.002037 in the most volatile third (book sums +2.91 against +6.03).
- F8: The losses cluster in falling-market years. The book summed −1.92 in 2018 and −1.08 in 2022 while invested 25% and 36% of bars, with the coin returning −0.0020 and −0.0022 per invested bar. In 2021 it earned +7.65 while invested 83% of bars.
