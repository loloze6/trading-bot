---
line: 7.g patterns
backtest: N2-03_deep-month-loss-rebound_1d
idea tested: N2-03_deep-month-loss-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.3980 USD
---
## Findings
- **F1:** After a day whose return is at least one 20-day standard deviation below zero, the next day's return beats the coin's mean by 0.0050 when the 20-day change is negative (n=1200, t=3.05, hit 59%). It beats it by 0.0064 when the 20-day change is positive (n=635, t=3.25, hit 60%). On days that are not down by one standard deviation, the excess is -0.0008 (n=12665, t=-1.93). The one-day rebound is local and independent of the month's fall that the idea uses.
- **F2:** This one-day rebound after a down day of one standard deviation or more grows with the coin's 20-day volatility. The next-day excess is -0.0020 in the lowest volatility tercile (n=683, t=-1.33), 0.0043 in the middle (n=610, t=2.15) and 0.0164 in the highest (n=542, t=5.31). With events spaced at least 5 bars apart, the high-volatility next-day mean is 0.0087 (n=377, t=2.58).
- **F3:** The rebound is spent within a day. In spaced events, the return from day 1 to day 5 after a down day of one standard deviation or more is not distinguishable from zero in any volatility tercile: 0.0034 (t=0.78), 0.0031 (t=0.69) and 0.0096 (t=1.55), with n of about 376 each.
- **F4:** When the down day follows another down day of one standard deviation or more, the next-day excess is 0.0144 (n=260, t=3.49, hit 64%). After a single down day it is 0.0039 (n=1534, t=2.92).
- **F5:** The rebound appears in all six coins (next-day excess 0.0021 to 0.0098; XMR t=3.54, n=314). It is strongest in 2020 and 2021 (0.0149 and 0.0144, t of about 3.4 each) and fades in 2024 and 2025 (-0.0014 and 0.0028, t below 1).
- **F6:** The book earns on short holds and loses on long ones. Trades held up to 1.5 days average +2.20% net (n=707, 74% wins) and trades held 1.5 to 5 days average +1.30% (n=1088). Trades held over 15 days average -6.48% (n=743, 29% wins) and sum to -4811% of net P&L, against +2794% for all shorter trades.
- **F7:** The month-fall rebound the idea tests depends on the year, not on the depth of the fall. The 20-day excess after the deepest-fall quintile is -0.070 in 2018 (n=42, t=-2.11) and +0.171 in 2021 (n=23, t=2.93). Pooled, it is 0.019 (n=138, t=1.03).

## Ideas
- `N2-03_deep-month-loss-rebound.g1_volatile-down-day-next-day-bounce` (from F1, F2, F4, F5): When a coin's daily close falls by at least one of its own 20-day standard deviations while its 20-day volatility is in its upper range, the next day's return is higher than the coin's usual daily return. The bounce is larger after two such down days in a row.
- `N2-03_deep-month-loss-rebound.g2_one-day-rebound-decay` (from F3, F6): After an unusually large daily fall, the coin's excess return is concentrated in the first following day, and the gain does not continue over the next four days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
