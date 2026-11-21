---
line: 7.g patterns
backtest: 018-05_hourly-plunge-loss-before-close_1h
idea tested: 018-05_hourly-plunge-loss-before-close
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3878 USD
---
## Findings
- **F1:** A large 24-hour drop is followed by a rebound over the next 24 hours, not by a further fall. The rebound grows with the drop's size in multiples of the coin's 30-day mean absolute 24-hour return (z):
- **F2:** The rebound after drops with z ≤ -2.5 is positive on all 6 coins, but it is uneven across time:
- **F3:** The book lost because it sat short on the wrong side of the rebound in F1.
- **F4:** Over the next 24 hours, the highest-volatility fifth of bars is the only quintile with a positive excess move: +33 bps, 3100 cases, t 2.9. The other four quintiles run from -6 to -13 bps. This is consistent with the rebound in F1 being concentrated after violent falls.
- **F5:** A large 7-day rise (7-day return at 2 or more times its 30-day mean absolute 7-day return) is followed by further rises, but not on every coin or window:
- **F6:** Returns by hour of day differ clearly, but are far smaller than a trade's cost.

## Ideas
- `018-05_hourly-plunge-loss-before-close.g1_rebound-after-outsized-daily-plunge` (from F1, F2, F3, F4): When a coin's 24-hour return, read at an hourly close, falls to a large multiple of its 30-day average absolute 24-hour return, the price rises over the next 24 hours, and the larger the drop in those multiples, the larger the rise.
- `018-05_hourly-plunge-loss-before-close.g2_outsized-weekly-rise-continues` (from F5): When a coin's 7-day return, read at an hourly close, rises to a large multiple of its 30-day average absolute 7-day return, the price keeps rising over the next 7 days, and the larger the rise in those multiples, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
