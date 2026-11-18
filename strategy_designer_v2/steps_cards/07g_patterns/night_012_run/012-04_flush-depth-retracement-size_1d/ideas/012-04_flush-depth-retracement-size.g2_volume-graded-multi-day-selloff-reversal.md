---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-04_flush-depth-retracement-size
line: 7.g patterns
backtest: 012-04_flush-depth-retracement-size_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day a coin closes lower, the higher that day's volume relative to its median over the prior 20 days, the larger the coin's rise over the next 3 days.
Consequence: The rebound after heavy-volume selling lasts several days, so a long taken at the close of such a day can be held through it.
Why:
- F2: The same down-day effect holds over the next 3 days: slope +0.0126 per log unit of volume ratio (t 4.72, n 2245), while up days show −0.0030 (t −1.35, n 2470).
- F3: Among down days, next-day excess return rises with the volume-ratio quintile: from −0.05% (bottom quintile, n 1391) to +0.70% (top quintile, n 1400); up days stay flat or negative in every quintile (−0.14% in the top quintile).
- F5: The tested flush filter adds little: sharp falls (z ≤ −2) with volume ≥ 2× and a lower wick ≥ 0.3 average +1.88% excess over 3 days (t 1.78, n 31) against +0.11% for other sharp falls (n 139), and −0.62% over the next day (t −1.06, n 85). The wick shape does not carry the rebound; the volume does.
