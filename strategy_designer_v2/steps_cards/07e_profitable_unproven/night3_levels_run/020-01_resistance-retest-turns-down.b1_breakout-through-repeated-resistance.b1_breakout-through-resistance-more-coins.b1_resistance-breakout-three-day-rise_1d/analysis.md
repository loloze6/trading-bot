---
line: 7.e profitable but not proven
backtest: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b1_resistance-breakout-three-day-rise_1d
idea tested: 020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b1_resistance-breakout-three-day-rise
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4852 USD
---
## Findings
- **F1:** The book's mean daily return is 0.069 %, of which 0.045 % (66 %) comes from the market's own rise (mean position 0.34, in the market on 42 % of coin-days) and only 0.024 % from timing, while holding the coins averages 0.134 % a day.
- **F2:** The gain sits in a few periods and trades: windows w6, w10, w11, w17 and w21 together carry 102 % of the summed book return, the years 2018, 2022 and 2025 lose (-0.036 %, -0.010 % and -0.045 % a day), and the top 1 % of the 7509 trades makes 42 % of their summed net result.
- **F3:** The book earns in rising coins. When in a position, it makes -0.048 % a day in the quartile of coin-days whose prior 30-day return is lowest (mean -20 %), +0.128 % in the second, +0.361 % in the third (+12 %) and +0.244 % in the top quartile (+52 %), over 2834 coin-days each.
- **F4:** The tested signal splits in two on whether the break's close is also the coin's highest close of the past 90 days.
- **F5:** Among the breaks at a new 90-day high, the move grows with the level's turn-count-times-margin value.
- **F6:** Over all breaks, the move grows with the horizon, not the plan's 3 days: excess +0.13 % over 3 days (t 0.97, 5078 cases), +0.37 % over 10 days (t 1.31, 4770 cases) and +0.60 % over 20 days (t 1.31, 4369 cases).
- **F7:** The 10-day excess of the new-high breaks (+6.4 %) is about 29 times the 0.22 % cost of a buy and a sell. The plan's 3-day excess over all breaks (+0.19 %) is 0.8 times that cost.
- **F8:** On every bar, not only on breaks (non-overlapping 10-day grid, 1728 cases), nearness to the 90-day high carries the move, though not monotonically.
- **F9:** On the same grid, the top quintile of 30-day return (mean +55 %) gains +3.2 % over 10 days (t 2.27) and the middle quintile loses -1.9 % (t -2.52). The slope is positive in 14 of 17 coins.

## Ideas
- `020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b1_resistance-breakout-three-day-rise.e1_resistance-break-at-new-high` (from F4, F5, F6, F7, F2): When a coin's daily close breaks above a price where it turned down several times in the past 90 days and that close is also its highest close of the past 90 days, it rises over the next 10 days. The more times the level turned it down and the more clearly the close cleared it, the larger the rise.
- `020-01_resistance-retest-turns-down.b1_breakout-through-repeated-resistance.b1_breakout-through-resistance-more-coins.b1_resistance-breakout-three-day-rise.e2_nearness-to-90-day-high` (from F8, F3, F1, F9): The nearer a coin's daily close is to its highest close of the past 90 days, the larger its rise over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
