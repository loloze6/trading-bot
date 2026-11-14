---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When the 50-day average is wide above the 200-day average, the coin's forward return is lower than when the spread is narrow, so a stretched spread marks a mature, exhausting move.
Consequence: A trader should size a long position larger when the spread is narrow and smaller when it is stretched, which is the reverse of the current forecast.
Why:
- F1: The forecast's size does not grade the coin's next-day return: the coin's mean next return rises only from 0.000942 (forecast 0–5, t 0.90) to 0.001549 (forecast 15–20, t 1.37), and across quintiles of the raw 50/200 spread it is highest in the lowest quintile (0.002726) and only 0.001443 in the highest. This matches the verdict's slope t of 0.37 and its share-positive gap of −0.021.
- F5: Trades opened at a high forecast lose and those opened at a low one win. The 774 trades entered with forecast 10–20 average −1.42% gross with a 30.6% win rate. The 150 trades entered at forecast 2–5 average +9.15% gross and are held longer (56.7 against 38.6 days).
