---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall measured in its own 20-day daily volatility, the more it rises over the next 1 day, and this rise grows faster than the size of the fall itself, so the largest falls carry most of the rebound.
Consequence: A trader should buy only after the rare outsized vol-scaled down days, for one day, because ordinary down days give a rebound smaller than the cost of trading it.
Why:
- F1: The book loses because its trades cost more than its forecast earns. Before fees the position earns 2.31 bps a day, the fees take 3.59 bps a day, and the book ends at -1.31 bps a day on 0.44 of the book turned over each bar. This matches the stated size: the total move per case is 0.9 times the 0.17 % cost of a buy and a sell.
- F4: The one-day rebound is concentrated in the largest falls and is larger when the coin's 50-day return is positive. After falls beyond 1.5 usual moves, the next-day excess is +0.71 % with t 1.86 (83 cases) when the 50-day return is positive, and +0.29 % with t 0.57 (127 cases) when it is negative.
- F6: Small daily moves carry no edge but still pay fees.
- F7: Holding the rebound longer does not help. After falls beyond one usual move, the excess return is +0.32 % over 1 day, +0.15 % over 2 days, +0.07 % over 3 days and -0.16 % over 5 days.
