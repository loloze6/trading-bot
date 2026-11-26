---
line: 7.b inconclusive
backtest: 031-03_up-streak-length-continuation_1d
idea tested: 031-03_up-streak-length-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.1954 USD
---
## Findings
- **F1:** The test's own slope is on the side the idea predicts but short of the bar: a slope of 5-day excess return on the forecast of +0.000489 per forecast unit, with t 1.43 (clustered by day), on 3326 grid bars; 1612 of them have a positive forecast, on 456 days. My recomputation gives the same slope and the same t, 1.43.
- **F2:** The effect is mixed across coins. On the 5-day grid the slope is positive in 4 of 6 coins and carried mostly by XRP (+0.00128, t 1.74, 523 cases) and ZEC (+0.00113, t 1.67, 547). It is near zero or negative in BTC (-0.00003, t -0.08, 569) and ETH (-0.00012, t -0.23, 570). Each coin has only about 550 cases, too few for any coin to show it alone.
- **F3:** The effect is mixed across years. The 5-day slope is positive in 2018, 2019, 2021 and 2023 (2019: +0.00254, t 2.56, 426 cases) and negative in 2020, 2022, 2024 and 2025 (2025: -0.00096, t -1.23, 426). No single regime carries it.
- **F4:** The 60-day trend barely changes the slope. After a 60-day rise it is +0.00074 (t 1.11, 842 cases); after a 60-day fall it is +0.00022 (t 0.37, 804 cases). So the effect cannot be amended to a clear regime where it shows.
- **F5:** The grading is not clean at 5 days. The mean 5-day excess return after an up streak of 2, 3 and 4 or more closes is +0.70 %, +1.41 % and -0.01 % (375, 164 and 191 cases). At 10 days it is +1.74 %, +4.07 % and +3.06 % (175, 77 and 98 cases). The streak bins are small, and the slope is about the same at 10 days (+0.00102, t 1.44, 1646 cases) as at 5.
- **F6:** At 1 day the slope turns slightly negative (-0.000113, t -1.59, 16904 cases), and an up streak of 1 close is followed by -0.31 % the next day (4545 cases). A short giveback dilutes the continuation over the horizon, which helps keep the per-case unusual move near zero (-0.29 %, t -0.97, 3153 cases).

## Ideas
- `031-03.b1_up-streak-continuation-more-coins` (from F1, F2, F3, F4): The more days in a row a coin has closed higher, measured against the lengths of its own up-close streaks over the past 365 days, the more it keeps rising over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
