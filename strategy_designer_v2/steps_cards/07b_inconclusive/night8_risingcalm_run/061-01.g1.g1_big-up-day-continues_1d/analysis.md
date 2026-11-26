---
line: 7.b inconclusive
backtest: 061-01.g1.g1_big-up-day-continues_1d
idea tested: 061-01.g1.g1_big-up-day-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3623 USD
---
## Findings
- **F1:** The tested idea dropped the brief's calm-market restriction, and its result is diluted by that. On the 5-day grid in folds B–C, up days in calm markets have a graded slope of the unusual move on the day's size in swing units of +0.024 (t 2.75, 305 cases) and a mean unusual move of +1.48 % (day-pooled t 1.38, strength 0.12). Up days in agitated markets have a slope of +0.010 (t 0.79, 280 cases) and a mean of +0.46 % (t 0.40, strength 0.03).
- **F2:** The step-5 cases have the sign the idea predicts in calm markets and the opposite sign in agitated ones. Replicated in folds B–C, calm cases average +0.12 % (t 0.29, 545 cases) and agitated cases −0.53 % (t −1.02, 551). Choppy agitated cases alone fall −4.2 % (t −3.11, 31).
- **F3:** The effect is clearest in rising calm markets and absent or reversed in falling ones. Step-5 cases in rising calm markets average +1.83 % (t 2.19, 162 cases) against −2.22 % in falling calm (t −2.32, 116). On the grid, calm up days in a rising trend average +4.23 % (day-pooled t 1.92, strength 0.35, 94 cases) against −0.23 % in a falling trend (t −0.13, 71).
- **F4:** The overall mean is pulled below zero by the small and middling forecasts, while the largest ones go the predicted way. The two lower forecast quartiles average −1.50 % (t −2.80) and −1.68 % (t −2.78), the top quartile +1.17 % (t 1.69), 371 cases each. Calm grid up days above 2 swing units average +7.9 % (day-pooled t 1.66, strength 0.59, 24 cases).
- **F5:** The effect shifts with the period. Step-5 cases average −3.04 % in 2018 (t −4.31) and +1.12 % in 2020 (t 2.27). Calm grid up days are negative in 2018 (−4.4 %, t −1.52) and positive in 2019–2021 (+1.5 %, +2.1 %, +4.9 %; t up to 2.08). Most of the market's own moves land on the calm up days of a falling year.
- **F6:** Calm down days show no mirror continuation. Their unusual move is −0.89 % (day-pooled t −1.18, 335 cases) and the graded slope +0.007 (t 0.84), so the long-only side the test chose is the right one.

## Ideas
- `061-01.g1.g1.b1_calm-big-up-day-continues` (from F1, F2, F4, F6): In a calm market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the further it keeps rising over the next 5 days.
- `061-01.g1.g1.b2_rising-calm-up-day-continuation` (from F3, F5, F1): In a rising, calm market, the larger a coin's one-day rise against the standard deviation of its daily returns over the past 30 days, the further it keeps rising over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
