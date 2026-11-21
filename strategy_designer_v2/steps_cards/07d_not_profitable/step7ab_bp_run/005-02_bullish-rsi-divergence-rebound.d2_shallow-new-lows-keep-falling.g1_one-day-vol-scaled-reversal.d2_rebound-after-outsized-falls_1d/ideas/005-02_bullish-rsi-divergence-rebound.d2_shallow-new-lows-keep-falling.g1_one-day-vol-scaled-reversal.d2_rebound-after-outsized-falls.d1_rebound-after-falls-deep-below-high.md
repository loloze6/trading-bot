---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall measured in its own 20-day daily volatility, the more it rises over the next 1 day, only while the coin already stands far below its 20-day high, and the deeper it stands below that high at the fall's close, the larger the rebound.
Consequence: A trader should buy a sharp down day for one day only when it comes deep into a selloff, and should refuse to buy sharp down days that are only shallow pullbacks from a recent high.
Why:
- F1: The fall's size does not carry the rebound. Measured in 20-day volatility, the next day's excess return is not graded: +0.96 % (t 2.08, n 113) after falls of 2 to 3 sigma, -0.40 % (t -1.03, n 148) after falls of 1.5 to 2 sigma, and -0.29 % (n 28) after falls beyond 3 sigma. So the cube in the forecast gave the book a size per case (unusual move +0.06 %) of only 0.5 times the 0.11 % round-trip cost, and the convexity check failed (-0.0005).
- F2: Where the coin stands when it falls does carry the rebound. Among falls beyond 1 sigma, split into quintiles by distance below the 20-day high, the next-day excess return is +1.56 % (t 2.59, n 120) in the deepest quintile (22 % to 61 % below the high) and +0.62 % (t 1.33) in the next. It is -0.18 % and -0.73 % (t -1.91) in the middle quintiles (6 % to 14 % below) and +0.30 % (t 1.02) nearest the high. The deepest quintile's move is about 14 times the cost of a trade.
- F3: The same holds on the book's own signal bars (forecast of 1 or more). In the deepest tercile of distance below the 20-day high, the excess next-day return is +0.71 % (t 2.46, n 383) and the position earned 0.45 % per bar. In the middle tercile these are -0.39 % (t -1.95, n 382) and -0.19 % per bar. So the book's gain is cancelled by its bets on falls that come in shallow pullbacks.
- F5: The book carries almost nothing beyond the signal bar, and what it earns is mostly the coins' own rise.
- F6: The book's falls come from years when falls kept falling. Its gain per bar was -0.028 % in 2018 and -0.052 % in 2022, when the coins' excess next-day return was -0.42 % and -0.36 %. Its deepest fall was 53 % on BTC and 38 % on ETH, giving a Calmar of 0.009.
