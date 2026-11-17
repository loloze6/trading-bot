---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's one-day fall on a Saturday or Sunday, scaled by its 20-day volatility, is followed by a rise over the next 1 day, larger the larger the scaled fall.
Consequence: Weekend selloffs are a reason to buy for the following day more than weekday selloffs are.
Why:
- F3: The next-day reversal is stronger after weekend days. The slope on z is -0.00394 (t -5.03, n 4096) on weekend days, against -0.00117 (t -3.32, n 10260) on weekdays. A Saturday fall with z below -1 is followed by +1.47% the next day (t 3.57, n 118), but a Monday fall by -0.03% (t -0.10, n 334).
- F2: The rebound after a fall is graded and holds widely. The next day's return rises steadily across the five down-day quintiles, from +0.14% after the smallest falls (z -0.10, t 1.23) to +0.67% after the largest (z -2.06, t 4.48, n 1412). After falls with z below -1 the next day is positive for all six coins (+0.33% for BTC to +1.06% for XMR, t 3.80) and in all eight years (t from 0.10 to 3.64).
