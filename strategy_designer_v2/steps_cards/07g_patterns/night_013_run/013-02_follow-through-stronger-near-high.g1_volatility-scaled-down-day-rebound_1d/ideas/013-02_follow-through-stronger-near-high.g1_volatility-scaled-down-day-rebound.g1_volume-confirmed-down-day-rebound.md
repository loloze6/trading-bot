---
brief: 013_anchoring-to-recent-high
source-idea: 013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound
line: 7.g patterns
backtest: 013-02_follow-through-stronger-near-high.g1_volatility-scaled-down-day-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's fall on a day on heavy volume, relative to its average daily volume over the previous 20 days, is followed by a rise over the next 1 day. The larger the fall multiplied by the volume surge, the larger the next day's rise.
Consequence: A trader has a reason to buy a high-volume sell-off day for a one-day rebound, and to give little weight to falls on thin volume.
Why:
- F1: The next-day rebound after a down day depends on volume as well as on the size of the fall. On down days (z<0), regressing the next-day excess return on the scaled fall, log volume ratio (day's volume over its prior 20-day mean) and their product gives an interaction slope of 0.00297 with t = 4.29. The fall alone then has t = −0.44.
- F2: The rebound is concentrated where both volatility and volume are high. Down days in a coin's top 20-day-volatility tercile and top volume-ratio tercile are followed by a mean next-day excess return of +0.0138 (t = 4.80, n = 649). In the bottom tercile of both the mean is −0.0021 (t = −1.21, n = 622).
