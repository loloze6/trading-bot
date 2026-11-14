---
brief: 002_moving-average-cross-trend-persistence
source-idea: N4-02_new-high-not-shock
line: 7.b inconclusive
backtest: N4-02_new-high-not-shock_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's new 20-day closing high made on a small up day is followed by a rise over the next 10 days more often than after an average day of that coin.
Consequence: A trader would not require an outsized breakout day before going long; quiet new highs are at least as reliable in how often they work.
Why:
- F1: The size of the breakout day barely changes what follows. On the 381 independent breakouts (the first bar of each cluster), the excess 10-day return was +1.34 pp in the bottom half of the forecast (n=151, t=1.15) and +1.94 pp in the top half (n=230, t=1.65), a gap of about 0.6 pp. By forecast quintile the means were 3.42 / −0.46 / 2.44 / 1.82 / 1.28 pp, with no ordering.
- F5: The positive mean after outsized breakout days comes from a few large winners. The top half's mean was +1.94 pp but its median was −1.39 pp, with a hit rate of 49.6% (n=230). The smallest-quintile breakouts had a mean of +3.42 pp, a median of +1.50 pp and a hit rate of 59.7% (n=77, t=2.11).
