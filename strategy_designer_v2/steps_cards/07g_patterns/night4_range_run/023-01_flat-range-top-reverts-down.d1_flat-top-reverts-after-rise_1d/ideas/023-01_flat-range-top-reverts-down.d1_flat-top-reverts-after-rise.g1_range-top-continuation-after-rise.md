---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is positive, the higher its close sits within its 30-day closing range, the more it rises over the next 5 days beyond its normal drift, and the lower it sits, the more it falls.
Consequence: After a 90-day rise, a trader would buy a coin near the top of its month's range rather than short it, and would refuse to buy one near the bottom.
Why:
- F1: Among bars where the 90-day return was positive (the `mean_reversion` regime), the close's position in its 30-day closing range predicts the next 5 days' unusual move upward, not downward: the slope is +0.018 per unit of position, t 3.70 over 1313 non-overlapping cases. Among bars with a negative 90-day return the slope is -0.001, t -0.27 over 1242 cases.
- F2: The 90-day-rise effect is graded by quintile of range position. The bottom quintile's unusual 5-day move is -2.09 % (t -1.90, n 126), rising to +1.73 % in the top quintile (t 2.42, n 372). Top minus bottom is +2.85 %, Welch t 2.56 (263 vs 263 cases). The top-quintile move is about 9 times the 0.19 % cost of a trade.
- F4: The slope is positive in both halves of the windows and in 5 of 6 coins:
- F5: The slope is uneven over time. It is concentrated in 2020 (+0.056, t 4.80) and 2021 (+0.030, t 2.01) and near zero in 2022-2025, with every |t| at or below 0.53. It is strongest in the middle tercile of flatness (+0.036, t 4.54) and absent in the flattest tercile (-0.002, t -0.24).
- F7: The book lost because it shorted the very bars that kept rising. Its daily returns correlate -0.52 with the coins' daily returns over 17380 coin-days, with a mean of -0.058 % a day.
