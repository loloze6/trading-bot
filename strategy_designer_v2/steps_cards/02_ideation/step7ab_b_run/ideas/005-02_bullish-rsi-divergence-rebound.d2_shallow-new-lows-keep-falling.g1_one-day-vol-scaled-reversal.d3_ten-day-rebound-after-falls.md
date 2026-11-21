---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall relative to its own 20-day daily volatility, the more it rises over the next 10 days.
Consequence: A trader buying a sharp daily fall should hold the rebound for about ten days rather than one, so that the move per trade is much larger than its cost.
Why:
- F1: Per signal, the book captures less than one round trip costs, so it cannot pay. The idea's move per case is +0.15 % over 1 day, 0.9 times the 0.16 % cost. The book's mean gain before fees was 0.006 % per bar on BTC and 0.041 % on ETH, against fees of 0.037 % and 0.035 % per bar. Turnover was 0.38 to 0.50 of the book per bar. Its daily return was -0.032 % on BTC and +0.006 % on ETH, against +0.118 % and +0.137 % for holding.
- F5: The rebound after a large vol-scaled 1-day fall grows with the horizon, but the evidence is weak. Over all cases it is 0.35 % above drift over 1 day (t 1.9, 657 cases), 0.84 % over 5 days (t 1.2, 147 cases) and 1.79 % over 10 days (t 1.4, 83 cases).
