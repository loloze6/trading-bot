---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion
line: 7.c rejected
backtest: 023-03_flatter-range-stronger-reversion_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits to the top of its 30-day closing range, the more the coin rises over the next 10 days.
Consequence: A close pressed against the top of the past month's range is a reason to be long the following days, not to sell it back toward the middle.
Why:
- F3: The continuation was carried by closes far above the middle. In the highest quintile of signed distance, the 10-day return net of drift was +2.98 % (t 2.32, n 252). The other four quintiles ranged from -0.43 % to -1.02 % (all |t| ≤ 1.1). Distance alone ranked the 10-day move only weakly (Spearman 0.038; OLS slope on distance t 0.93).
- F1: The market did the opposite of the idea: on the 5-day grid, the coin's 5-day return net of its drift, signed away from the middle of its 30-day range, was +0.61 % (t 2.91, n 2555). It was +0.30 % at 1 day (t 3.11), +0.50 % at 3 days (t 3.01), +1.26 % at 10 days (t 3.97, overlapping on the 5-day grid), and on a non-overlapping 10-day grid +1.09 % (t 2.53, n 1259). So moves away from the middle continued instead of reverting.
- F7: The tested reversion lost -0.40 % per case over 5 days (strength -0.039, 2912 cases), against a trade cost of 0.19 %. The opposite move, continuation, is about +0.61 % per case over 5 days and about +1.1 % over 10 days. That is roughly 3 to 6 times the cost.
