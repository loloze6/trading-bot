---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls
line: 7.b inconclusive
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal.d2_rebound-after-outsized-falls_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall measured in its own 20-day daily volatility, the more it rises over the next 1 day, and this rise grows faster than the size of the fall itself, so the largest falls carry most of the rebound.
Consequence: A trader should buy only after the rare outsized vol-scaled down days, for one day, because ordinary down days give a rebound smaller than the cost of trading it.
Why:
- F1: The test's main measure is on the side the idea predicts but short of the bar: bars with forecast ≥ 5 rose 0.25 % more than the coin's normal next day (t 1.51, 780 cases). The data held only BTC and ETH, because BNB has no data, so the test ran on 2 coins.
