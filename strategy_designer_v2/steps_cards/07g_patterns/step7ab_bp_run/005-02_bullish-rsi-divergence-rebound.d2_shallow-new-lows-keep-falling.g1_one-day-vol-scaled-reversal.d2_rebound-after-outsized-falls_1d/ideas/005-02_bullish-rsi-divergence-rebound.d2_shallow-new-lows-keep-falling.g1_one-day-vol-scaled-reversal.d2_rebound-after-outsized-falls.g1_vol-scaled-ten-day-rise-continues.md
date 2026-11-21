---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls
line: 7.g patterns
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's rise over the past 10 days measured in its own 20-day daily volatility, the more the coin rises beyond its normal drift over the next 10 days.
Consequence: A trader should lean long for about ten days in proportion to how strong a coin's vol-scaled 10-day rise has been, a move per case many times the cost of a trade, and refuse such a trade after weak or no rises.
Why:
- F1: Over 10 days, a coin's 10-day rise measured in its own 20-day daily volatility is followed by more rise. The top quintile of that vol-scaled 10-day return (mean 1.71 volatility units) earns +2.74 % above drift over the next 10 days (t 2.26, 94 independent cases). That is 0.22 of the coin's usual 10-day move, about 25 times the 0.11 % cost of a trade. It shows on both coins alike: BTC +2.78 %, ETH +2.71 %. Across all quintiles the slope t is 1.94.
- F2: The same continuation shows with a 5-day vol-scaled return. Restricted to rises, the slope t is 2.58. The top quintile's 10-day excess return is positive on 9 of 10 grid offsets, with t from 1.32 to 2.95 on the positive ones, and t at or above 2 on 4 of them (offsets 1, 7, 8, 9). The lowest quintile's results scatter around zero (t from -1.13 to +1.21).
- F3: The continuation is not steady over time. The top z10 quintile's 10-day excess is +0.17 % in windows w1-12 against +5.21 % in w13-24. By year it runs from +9.9 % (2020) to -7.3 % (2022), with 6 of 8 years positive.
