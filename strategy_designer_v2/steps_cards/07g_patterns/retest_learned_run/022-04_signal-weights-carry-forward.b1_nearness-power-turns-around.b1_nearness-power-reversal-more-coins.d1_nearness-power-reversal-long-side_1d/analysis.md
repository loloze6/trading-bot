---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4067 USD
---
## Findings
- **F1:** Closes moderately below the 90-day high do worst. On the 5-day grid, the second quintile of nearness to the 90-day high (per coin) has a mean excess 5-day return of -1.89 % (t -4.13, 466 cases). It is negative in 2018–2021 (-2.70 %, t -2.61, 125 cases) and in 2022–2025 (-1.59 %, t -3.20, 341 cases), and in 14 of 15 coins (93 %).
- **F2:** Closes furthest below the 90-day high recover. The deepest quintile has an excess 5-day return of +0.96 % (t 1.96, 475 cases), and it is positive in both periods (+1.01 % and +0.91 %). Inside the lower two quintiles, the rank correlation between nearness to the high and the excess 5-day return is -0.081 (p 0.013): the further below its high a coin closes, the higher its next 5 days.
- **F3:** In the upper four quintiles, nearness to the 90-day high rises with the excess 5-day return (Spearman +0.095, p 4e-5). This comes from 2018–2021 only (top two quintiles +3.23 % and +4.06 %, t 2.42 and 3.20). In 2022–2025 those quintiles are flat (-0.01 % and +0.03 %, t near 0), so it does not carry forward.
- **F4:** The tested reversal signal carries almost nothing.
- **F5:** Saturday has the highest mean excess daily return of the week, +0.30 % (t 4.47, 3442 coin-days). It is positive in 7 of 8 years, and 0.00 % in 2023. The book has only 25 of its worst 2 % coin-days on Saturdays, against 67 to 82 on every other weekday. This is a calendar condition with no grade, and the t is inflated because coins move together on the same days, so no idea is written from it.
- **F6:** Other cuts look like noise among the many angles tried.

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.b1_nearness-power-reversal-more-coins.d1_nearness-power-reversal-long-side.g1_deep-drawdown-rebound-graded` (from F1, F2, F4): When a coin closes in the lower part of its 90-day range, the further below its 90-day high it closes, the higher its return over the next 5 days. The coins sitting only moderately below their high do worst, and the deepest ones rebound.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
