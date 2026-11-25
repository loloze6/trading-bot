---
line: 7.g patterns
backtest: 032-03_deep-fall-low-exhaustion-rebound_1d
idea tested: 032-03_deep-fall-low-exhaustion-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3665 USD
---
## Findings
- **F1:** How near a coin's close sits to its highest close of the prior 30 days, measured in units of its 30-day mean daily range, grades the next 5 days' unusual move almost in order. By quintile it runs -1.68 %, -0.94 %, -1.11 %, +0.91 % and +2.73 % (about 245 non-overlapping cases each). The raw distance's top quintile gives +3.20 % (t 2.73 with the cases of one day together, 91 days), and its Spearman is 0.115 (p < 0.001, 1226 cases).
- **F2:** That near-the-high effect is positive in all 6 coins (rho 0.046 for LTC up to 0.188 for ETH) and in 2019, 2020 and 2021 (0.018, 0.126, 0.177), but it turns negative in 2018 (-0.109). It is stronger in rising years.
- **F3:** A long lower wick (the distance from the day's low up to the body, as a share of price) is followed by a weaker 5 days. Its top quintile has an unusual move of -2.89 % (t -2.11, 132 days), while the other four quintiles range from +0.13 % to +1.07 %. Its Spearman is -0.071 (p 0.004), and it is negative in every year from 2018 to 2021 and in all 6 coins.
- **F4:** The long-wick weakness is deepest after a 30-day fall. A big wick gives -2.08 % after a fall and -2.84 % in the middle third, against -0.37 % after a rise. A small wick after a 30-day rise gives +2.31 %.
- **F5:** Daily moves partly reverse the next day. The day's return against the next day's unusual return has a Spearman of -0.103 (p < 0.001, 8262 days). The reversal is strongest on wide-range days, where the weakest-return quintile gains +1.04 % the next day, against -0.24 % on narrow-range days.
- **F6:** The tested regime itself is rare and flat on the 5-day grid. It covers 52 grid cases with a mean unusual move of +0.17 % (t 0.08), so the book's small positive Sharpe of 0.28 comes from very few, undistinguished bets.
- **F7:** Weekdays differ on one-day unusual returns: Wednesday -0.50 % (t -2.78) and Thursday +0.41 % (t 2.80), out of 7 weekdays tested. With that many angles looked at, this does not stand out enough to count as a finding to build an idea on.

## Ideas
- `032-03.g1_near-monthly-high-continuation` (from F1, F2): The closer a coin's daily close is to its highest close of the past 30 days, measured against its typical daily range over those 30 days, the larger its rise over the next 5 days.
- `032-03.g2_long-lower-wick-weakness` (from F3, F4): The longer a coin's lower wick on a day (the drop from the body down to the day's low, as a share of price), the lower its return over the next 5 days. The effect is largest when the coin has fallen over the past 30 days.
- `032-03.g3_wide-day-fall-next-day-rebound` (from F5): On a day whose high-low range is wide compared with the coin's past 20 days, the larger the coin's fall that day, the larger its rise over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
