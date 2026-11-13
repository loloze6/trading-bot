---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-03_deep-month-loss-rebound
line: 7.b inconclusive
backtest: N2-03_deep-month-loss-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin has fallen a moderate 10–20% over 20 days, it keeps falling over the next 20 days by more than its usual 20-day move.
Consequence: A trader should refuse to buy moderate monthly falls, and can treat them as a continuation of the down move rather than a dip to buy.
Why:
- F5: Raw depth splits the result in two directions: across all non-overlapping bars, 20-day falls deeper than 20% are followed by +3.5% (n 38) and +3.9% (n 65) excess, but falls of 10–20% are followed by −5.1% (hit 34%, t −2.36, n 88).
- F6: Among positive forecasts, forward excess rises steadily with forecast size: from −6.6% in the lowest quintile (hit 32%, t −2.94, n 85) to +3.7% in the top quintile (t 1.73, n 85). Small standardised declines therefore keep falling, and only large ones rebound. Because 24% of positive forecasts sit at the +20 cap, the top decile cannot separate the large declines from the extreme ones.
