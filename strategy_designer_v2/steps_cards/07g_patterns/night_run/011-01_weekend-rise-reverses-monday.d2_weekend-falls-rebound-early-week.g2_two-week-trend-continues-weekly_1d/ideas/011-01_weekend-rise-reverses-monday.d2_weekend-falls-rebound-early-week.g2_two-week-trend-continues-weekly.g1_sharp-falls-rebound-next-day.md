---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's one-day fall, scaled by its 20-day volatility, is followed by a rise over the next 1 day, larger the larger the scaled fall.
Consequence: After a sharp daily drop, lean long for the next day rather than shorting the move.
Why:
- F1: Falls reverse the next day, rises do not. On down days the slope of the next day's return on the day's return scaled by its 20-day volatility is -0.00308 (t -4.58, n 7056), against -0.00010 (t -0.18, n 7286) on up days.
- F2: The rebound after a fall is graded and holds widely. The next day's return rises steadily across the five down-day quintiles, from +0.14% after the smallest falls (z -0.10, t 1.23) to +0.67% after the largest (z -2.06, t 4.48, n 1412). After falls with z below -1 the next day is positive for all six coins (+0.33% for BTC to +1.06% for XMR, t 3.80) and in all eight years (t from 0.10 to 3.64).
