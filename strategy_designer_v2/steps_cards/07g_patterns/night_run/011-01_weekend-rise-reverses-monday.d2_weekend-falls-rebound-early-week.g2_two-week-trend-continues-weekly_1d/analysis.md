---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly_1d
idea tested: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3544 USD
---
## Findings
- **F1:** Falls reverse the next day, rises do not. On down days the slope of the next day's return on the day's return scaled by its 20-day volatility is -0.00308 (t -4.58, n 7056), against -0.00010 (t -0.18, n 7286) on up days.
- **F2:** The rebound after a fall is graded and holds widely. The next day's return rises steadily across the five down-day quintiles, from +0.14% after the smallest falls (z -0.10, t 1.23) to +0.67% after the largest (z -2.06, t 4.48, n 1412). After falls with z below -1 the next day is positive for all six coins (+0.33% for BTC to +1.06% for XMR, t 3.80) and in all eight years (t from 0.10 to 3.64).
- **F3:** The next-day reversal is stronger after weekend days. The slope on z is -0.00394 (t -5.03, n 4096) on weekend days, against -0.00117 (t -3.32, n 10260) on weekdays. A Saturday fall with z below -1 is followed by +1.47% the next day (t 3.57, n 118), but a Monday fall by -0.03% (t -0.10, n 334).
- **F4:** Saturday is the one day with a strong positive drift.
- **F5:** The 14-day trend's continuation is concentrated on bars with high volume relative to the coin's 30-day average.
- **F6:** The book's gain rests on a few years. Its Sharpe is 2.03 in 2020 and negative in 2022, 2023 and 2025 (-0.14, -0.25, -0.26). The 2020 year also carries the trend measure (t 3.00, against t 0.49 to 1.77 in every other year).

## Ideas
- `011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly.g1_sharp-falls-rebound-next-day` (from F1, F2): A coin's one-day fall, scaled by its 20-day volatility, is followed by a rise over the next 1 day, larger the larger the scaled fall.
- `011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly.g2_weekend-falls-rebound-sharper` (from F3, F2): A coin's one-day fall on a Saturday or Sunday, scaled by its 20-day volatility, is followed by a rise over the next 1 day, larger the larger the scaled fall.
- `011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g2_two-week-trend-continues-weekly.g3_volume-confirmed-trend-continuation` (from F5): A coin's 14-day return scaled by its 20-day volatility is followed by a move in the same direction over the next 7 days, larger the larger the scaled return times the day's volume relative to its 30-day average volume.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
