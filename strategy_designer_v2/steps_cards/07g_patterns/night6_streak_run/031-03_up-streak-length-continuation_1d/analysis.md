---
line: 7.g patterns
backtest: 031-03_up-streak-length-continuation_1d
idea tested: 031-03_up-streak-length-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3493 USD
---
## Findings
- **F1:** A coin's own 1-day return, scaled by its past 20-day daily volatility, predicts its 5-day excess return on the upside only. Pooled over the six coins on the non-overlapping 5-day grid (3046 cases, 569 days, clustered by day), the slope on the positive part is 0.207 vol-units per unit of z with t 3.06; the slope on the negative part is 0.025 with t 0.39.
- **F2:** The grading is visible in the buckets. After days with a 1-day z between 1 and 2, the mean 5-day excess return is +1.42 % (301 cases, 164 days, t 1.73). After a z above 2 it is +3.75 % (103 cases, 58 days, t 2.20). Days with z between 0 and 1 give −0.18 % and days with z between −1 and 0 give −0.57 %.
- **F3:** The upside slope has the same sign in five of six coins:
- **F4:** The effect is weaker in the later years. The full 1-day z slope is 0.141 with t 2.20 up to 2021 (1481 cases) and 0.048 with t 0.92 after 2021 (1565 cases).
- **F5:** Streak length itself carries no graded follow-on move, so the size of the move matters more than the count of closes.
- **F6:** The book is mostly the coins' own drift, not timing. It holds a mean allocation of 0.78, its daily beta to the coins is 0.61, it is in a position on 96 % of coin-days, and its Sharpe is 0.0014 below holding's.
- **F7:** No other angle stands out given how many I looked at:

## Ideas
- `031-03.g1_large-up-day-continuation` (from F1, F2, F3, F5): The larger a coin's 1-day rise relative to its own daily volatility over the past 20 days, the more it keeps rising over the next 5 days, beyond its normal drift.
- `031-03.g2_fast-large-up-day-drift` (from F1, F2, F4): The larger a coin's 1-day rise relative to its own daily volatility over the past 20 days, the more its return over the next 2 days exceeds its normal drift, with most of the 5-day continuation arriving in those first 2 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
