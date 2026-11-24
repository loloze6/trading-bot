---
line: 7.b inconclusive
backtest: 031-03.g1.b1.d2.e2.g1.g1.d2_three-day-rebound-after-falls_1d
idea tested: 031-03.g1.b1.d2.e2.g1.g1.d2_three-day-rebound-after-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3463 USD
---
## Findings
- **F1:** The rebound shows over the next day, not over three. The forecast's correlation with the excess next-day return has t 5.30 on 2,897 grid bars, and falls are followed by +0.42 % excess (t 3.15, 1,355 cases). Over 2 and 3 days the t drops to 1.80 and 1.83. Over 5, 7 and 10 days it is -0.08, -1.15 and +0.35. So the plan's 3-day horizon adds the noise of days two and three to a move that is mostly done after one day.
- **F2:** The next-day effect holds across years and the 3-day effect does not. Over the next day the correlation is positive in 7 of 8 years and has t ≥ 2 in five: 2018 3.17, 2020 3.13, 2021 2.27, 2023 2.48, 2024 2.83. The one negative year is 2025 (-0.73). Over 3 days no year exceeds t 1.83, and 2018 is -0.69.
- **F3:** The next-day move is graded on both sides. The mean excess next-day return by the day's return over its 30-day volatility runs evenly from +1.43 % (below -2, 69 cases) and +1.00 % (-2 to -1, 235) through +0.22 %, +0.02 %, -0.25 %, -0.36 % and -0.29 %, to -0.61 % (above +2, 65). The scaled day return taken on both sides has t 4.91 against the next day's excess return.
- **F4:** The volatility-ratio part of the idea adds nothing over the next day. Falls split into terciles of 30-day volatility against its 6-month mean give next-day t 1.46, 0.93 and 1.44 (excess +0.38 %, +0.28 %, +0.62 %). The product of fall and ratio has t 4.16 against 5.17 for the scaled fall alone.
- **F5:** Over the 3-day horizon the effect is uneven across forecast sizes. By forecast quintile the excess returns are +0.47 %, +0.52 %, -2.43 %, +1.48 % and +1.51 % (about 87 cases each). Only the deepest falls (below -2 volatilities, 27 cases) show a large +3.23 %. This is why the test's correlation stays short of t 2 although its sign is the predicted one.
- **F6:** The step-5 result is on the idea's side but short of the bar: t 1.83 on 954 grid bars. The test already used all of XMR's folds A-D (2,921 bars), so no more XMR data is available. The next-day rebound after falls (+0.42 % excess, F1) is larger than the 0.31 % cost of a trade.

## Ideas
- `031-03.g1.b1.d2.e2.g1.g1.d2.b1_xmr-next-day-fall-rebound` (from F1, F2, F3, F4, F6): The larger XMR's one-day fall against its 30-day daily volatility, the more its price rises back over the next day.
- `031-03.g1.b1.d2.e2.g1.g1.d2.b2_xmr-next-day-scaled-reversal` (from F1, F2, F3): The larger XMR's one-day move against its 30-day daily volatility, the more its price moves back the other way over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
