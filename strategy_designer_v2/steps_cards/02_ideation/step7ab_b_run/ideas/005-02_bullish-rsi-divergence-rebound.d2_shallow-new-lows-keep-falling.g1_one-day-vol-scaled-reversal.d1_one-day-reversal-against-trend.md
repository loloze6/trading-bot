---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall relative to its own 20-day daily volatility, and the nearer its close to the day's low, the more it rises over the next 1 day, only while its close is above its 50-day average. The larger its vol-scaled 1-day rise, the more it gives back over the next 1 day, only while its close is below its 50-day average.
Consequence: A trader should fade a sharp daily move only when it runs against the coin's 50-day trend: buy outsized down days in an uptrend, sell outsized up days in a downtrend.
Why:
- F1: Per signal, the book captures less than one round trip costs, so it cannot pay. The idea's move per case is +0.15 % over 1 day, 0.9 times the 0.16 % cost. The book's mean gain before fees was 0.006 % per bar on BTC and 0.041 % on ETH, against fees of 0.037 % and 0.035 % per bar. Turnover was 0.38 to 0.50 of the book per bar. Its daily return was -0.032 % on BTC and +0.006 % on ETH, against +0.118 % and +0.137 % for holding.
- F2: The short half loses outright. On bars with a negative forecast the position earned -0.028 % per bar before fees and paid 0.036 % in fees (2962 bars). That is because the coin's raw next-day return there was still +0.018 % against a drift of about +0.12 % a day. The long half earned +0.077 % per bar before 0.037 % of fees (2832 bars).
- F4: The reversal holds only against the coin's slower trend, and there it is several times the cost.
