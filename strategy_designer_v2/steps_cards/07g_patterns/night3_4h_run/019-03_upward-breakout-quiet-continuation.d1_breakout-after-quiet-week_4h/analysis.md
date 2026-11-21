---
line: 7.g patterns
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week_4h
idea tested: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4370 USD
---
## Findings
- **F1:** A coin's sharp one-day fall is followed by a rebound over the next three days. On the 3-day grid (4,128 cases), the fifth of cases with the deepest 1-day return measured in units of the coin's 30-day volatility rises +0.84 % above its normal drift (t 3.07, strength 0.095, total move +1.25 %, which is 6.5 times the 0.19 % cost of a trade). The other four fifths range from -0.51 % to +0.21 %. The rebound is positive in all 6 coins (strength 0.03 to 0.15) and in 6 of 8 years, carried mostly by 2020 (t 4.97) and 2025 (t 3.41), with 2018 negative (t -1.41).
- **F2:** A quiet past week is followed by underperformance, the opposite of the brief. The fifth of grid cases whose 7-day average 4h range is smallest against its 30-day average ends the next 3 days -0.77 % below the normal drift (t -3.13, strength -0.084). The loudest fifth ends +0.60 % above it (t 1.95). The quiet fifth is below drift in all 6 coins (t -0.29 to -2.27) and in 7 of 8 years (2024 t -5.54).
- **F3:** A narrow preceding two-day stretch is also followed by underperformance. On the grid, the narrowest fifth (stretch range against the 30-day mean 4h range) ends the next 3 days -0.70 % below drift (t -2.65). The widest two fifths end +0.41 % and +0.40 % above it. The per-coin Spearman correlation of narrowness with the next 3 days' excess return is negative in all 6 coins (-0.038 to -0.084).
- **F4:** Quiet weeks do not lead to larger moves. The mean absolute 3-day move after the quietest fifth of weeks is 5.55 %, against 6.57 % after the loudest fifth.
- **F5:** The breakout's size predicts the next 3 days only at its largest, and the down-break result does not hold up.
- **F6:** Timing by hour and weekday is real but too small to trade.
- **F7:** The book is close to holding the coin.

## Ideas
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.g1_sharp-fall-three-day-rebound` (from F1, F5): The deeper a coin's fall over the past day, measured against its usual one-day move over the past 30 days, the more it rises over the next three days.
- `019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week.g2_quiet-stretch-three-day-underperformance` (from F2, F3, F4): The narrower a coin's past two days of price range and the quieter its average four-hour range over the past 7 days, both compared with its past 30 days, the lower its return over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
