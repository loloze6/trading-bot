---
line: 7.g patterns
backtest: 077-01.b1_swing-rise-carry-more-coins_1d
idea tested: 077-01.b1_swing-rise-carry-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4026 USD
---
## Findings
- **F1:** In choppy calm bars the coin's 14-day return in swing units predicts its unusual 7-day move: slope 0.050 per swing unit, t 3.48 (cases of one day together), over 143 non-overlapping cases on 61 days, with Spearman 0.30. In the other profiles the slope is 0.013, t 1.31, over 838 cases.
- **F2:** The carry in choppy calm is graded across the whole positive range, not only past the tested threshold. The mean unusual 7-day move is +0.66 % (t 0.45, 55 cases) for 0 to 1 swing units, +5.19 % (t 1.59, 18 cases) for 1 to 2, and +19.5 % (t 2.40, 6 cases) above 2.
- **F3:** The carry rests on the rising side. On positive 14-day moves alone the slope is 0.064, t 2.96 (79 cases, 37 days). On negative moves alone it is 0.032, t 0.79 (64 cases, 37 days). The brief's "both directions" is not shown.
- **F4:** The choppy calm carry also holds on a longer look-back. The 28-day swing-scaled return gives a slope of 0.050, t 2.72, on the 7-day horizon (143 cases, 61 days). The 14-day return gives 0.059, t 2.30, on the 14-day horizon (66 cases, 26 days). The 7-day look-back gives only t 1.18 at 7 days.
- **F5:** The choppy calm carry is concentrated in time and must be read as fragile:
- **F6:** Cost is not what keeps the tested book from paying. Its unusual move of +1.47 % per case is 6.6 times the 0.22 % cost of a trade. It fails on evidence (t 0.83 over 64 days) and on activity (trades per day 0.0046, 2 % of coin-days in a position), because the threshold of 2 swing units leaves only 0.5 % of bars active.
- **F7:** After a large one-day fall in swing units the next day rebounds, graded:
- **F8:** The weekday pattern is not stable enough to count. Wednesday's next day averages -0.49 % (t -2.62, 1,057 cases), but the per-year means are -0.29 %, -1.44 %, -0.06 % and +0.38 % for 2018 to 2021, an unstable sign among many angles looked at.

## Ideas
- `077-01.b1.g1_calm-chop-month-rise-carries` (from F1, F2, F3, F4, F6): In a choppy, calm market, the larger a coin's 28-day return is against its own daily swing over the past 30 days, the more the coin rises over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
