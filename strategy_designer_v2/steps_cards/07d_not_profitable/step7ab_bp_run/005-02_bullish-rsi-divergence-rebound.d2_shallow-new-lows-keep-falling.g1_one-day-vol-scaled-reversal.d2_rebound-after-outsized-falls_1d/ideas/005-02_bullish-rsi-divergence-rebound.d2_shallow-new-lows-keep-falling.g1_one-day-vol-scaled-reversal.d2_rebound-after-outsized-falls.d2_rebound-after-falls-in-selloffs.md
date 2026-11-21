---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall measured in its own 20-day daily volatility, the more it rises over the next 1 day, only while its 20-day return is negative, and the more negative that 20-day return, the larger the rebound.
Consequence: A trader should scale a one-day rebound bet by how much the coin has already lost over the past 20 days, and should not buy sharp falls that follow a flat or rising month.
Why:
- F1: The fall's size does not carry the rebound. Measured in 20-day volatility, the next day's excess return is not graded: +0.96 % (t 2.08, n 113) after falls of 2 to 3 sigma, -0.40 % (t -1.03, n 148) after falls of 1.5 to 2 sigma, and -0.29 % (n 28) after falls beyond 3 sigma. So the cube in the forecast gave the book a size per case (unusual move +0.06 %) of only 0.5 times the 0.11 % round-trip cost, and the convexity check failed (-0.0005).
- F4: A fall's 20-day return sorts the cases the same way. The lowest quintile of 20-day return (-17 % to -59 %) gives +1.12 % next day (t 1.95, n 120). The third quintile (-9 % to -2 %) gives -0.68 % (t -2.03, n 119).
- F5: The book carries almost nothing beyond the signal bar, and what it earns is mostly the coins' own rise.
- F6: The book's falls come from years when falls kept falling. Its gain per bar was -0.028 % in 2018 and -0.052 % in 2022, when the coins' excess next-day return was -0.42 % and -0.36 %. Its deepest fall was 53 % on BTC and 38 % on ETH, giving a Calmar of 0.009.
