---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 5-day return relative to its own 20-day daily volatility, the more it keeps rising over the next 3 days.
Consequence: A trader should hold with, not against, a strong vol-scaled 5-day rise for about three days.
Why:
- F1: Per signal, the book captures less than one round trip costs, so it cannot pay. The idea's move per case is +0.15 % over 1 day, 0.9 times the 0.16 % cost. The book's mean gain before fees was 0.006 % per bar on BTC and 0.041 % on ETH, against fees of 0.037 % and 0.035 % per bar. Turnover was 0.38 to 0.50 of the book per bar. Its daily return was -0.032 % on BTC and +0.006 % on ETH, against +0.118 % and +0.137 % for holding.
- F3: After a large vol-scaled rise the coin keeps rising rather than giving back. Over all regimes, after a 1-day rise of more than one 20-day usual move the next day ends 0.22 % above drift (t 1.6, 762 cases). After a 5-day rise of more than one usual 5-day move the coin keeps rising: 0.43 % above drift over 1 day (t 3.4, 902 cases), 0.80 % over 2 days (t 3.2, 450 cases), and 1.55 % over 3 days (t 4.1, 296 cases, strength 0.23). The 3-day continuation is about 10 times the cost.
