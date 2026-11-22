---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is positive, the higher its close sits within its 30-day closing range, the more it rises over the next 10 days beyond its normal drift.
Consequence: A trader who goes with a coin's position in its month's range after a 90-day rise could hold for about 10 days instead of 5, which spreads the cost of a trade over a larger move.
Why:
- F3: The same 90-day-rise slope holds over 10 days: +0.031, t 3.09 over 659 cases, against -0.009, t -1.03 over 600 cases after a 90-day fall.
- F1: Among bars where the 90-day return was positive (the `mean_reversion` regime), the close's position in its 30-day closing range predicts the next 5 days' unusual move upward, not downward: the slope is +0.018 per unit of position, t 3.70 over 1313 non-overlapping cases. Among bars with a negative 90-day return the slope is -0.001, t -0.27 over 1242 cases.
- F2: The 90-day-rise effect is graded by quintile of range position. The bottom quintile's unusual 5-day move is -2.09 % (t -1.90, n 126), rising to +1.73 % in the top quintile (t 2.42, n 372). Top minus bottom is +2.85 %, Welch t 2.56 (263 vs 263 cases). The top-quintile move is about 9 times the 0.19 % cost of a trade.
