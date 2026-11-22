---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 10-day return, the more it rises over the next 5 days beyond its normal drift.
Consequence: A trader would lean with a coin's recent 10-day move rather than fade it.
Why:
- F6: Across all cases, the 10-day past return shows a weaker version of the same continuation. Its top quintile is followed by a +1.03 % unusual 5-day move, t 2.14 (n 626). The 30-day past return's top quintile gives +1.04 %, t 1.82.
- F1: Among bars where the 90-day return was positive (the `mean_reversion` regime), the close's position in its 30-day closing range predicts the next 5 days' unusual move upward, not downward: the slope is +0.018 per unit of position, t 3.70 over 1313 non-overlapping cases. Among bars with a negative 90-day return the slope is -0.001, t -0.27 over 1242 cases.
