---
line: 7.d confirmed, not profitable
backtest: 031-01.g1.g1.g1_two-week-run-carries-weekend_1d
idea tested: 031-01.g1.g1.g1_two-week-run-carries-weekend
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5274 USD
---
## Findings
- **F1:** The Calmar failure comes from the short side. Split from the book's daily returns, the long-only part has Sharpe 1.20, a yearly return of +16.0 %, a deepest fall of −8.2 % and Calmar 1.95. The short-only part has Sharpe −0.36, a yearly return of −4.3 %, a deepest fall of −34.8 % and Calmar −0.12. The full book's deepest fall of −23.5 %, reached in 2023, is the two parts added together.
- **F2:** The real effect sits only on the long side. After a two-week rise, the weekend move in the forecast's direction is +1.11 % (t 6.59, 1215 cases). After a two-week fall it is +0.03 % (t 0.21, 1238 cases). The shorts lost in 2021 (−1.24 %, t −1.98) and 2023 (−0.49 %, t −1.99), the years of the book's deep falls.
- **F3:** The long side is graded. Fridays with a positive forecast, split into thirds by forecast, have weekend returns of +0.78 % (t 2.43), +1.12 % (t 4.35) and +1.44 % (t 4.89), with 405 cases each. Across all Fridays, the 14-day-return quintiles give −0.34 %, −0.36 %, +0.81 %, +1.41 % and the top one +1.41 % (t 4.58). The top quintile reads +1.41 %, roughly two percent above the bottom two.
- **F4:** The long-only part's gain does not rest on one year. Its yearly sums are positive in all 8 years (+0.6 % in 2018 to +32.2 % in 2024), with yearly deepest falls between −3.3 % and −8.2 %. The full book lost in 2022 (−0.8 %) and 2025 (−6.0 %).
- **F5:** The positive run alone is not the effect. On the non-overlapping 2-day grid, non-Friday bars after a two-week rise earn +0.44 % over 2 days (t 3.58, 3088 cases). Fridays after a two-week rise earn +1.15 % (t 6.52, 1005 cases). The weekend more than doubles the move of the same situation, so the long-only repair keeps the idea's own signal rather than adding a separate effect.
- **F6:** The weekend carry is strongest when the coin's Friday close (after a two-week rise) sits near its yearly high. In the top fifth of the past year's range, the weekend move is +2.05 % (t 4.78, 193 cases). It is +1.07 % (t 3.19, 198) in the 0.5–0.8 band and +0.91 % (t 3.46, 237) in the lower half. The same position without the Friday earns only +0.55 % (t 1.77, 583 cases) near the high, so the yearly-high position is a stronger case of the Friday signal, not an effect of its own.
- **F7:** Trades cost little against this move, so cost is not what failed. The Friday entry day loses −0.048 % a day on average on the book, the fee day. The long weekend move of +1.11 % is about 5.8 times the 0.19 % trade cost.

## Ideas
- `031-01.g1.g1.g1.d1_two-week-rise-carries-weekend` (from F1, F2, F3, F4, F5, F7): The higher a coin's 14-day rise, measured in its usual daily moves at Friday's close (UTC), the more it rises over the following Saturday and Sunday together.
- `031-01.g1.g1.g1.d2_weekend-carry-near-yearly-high` (from F2, F5, F6): After a two-week rise, the closer a coin's Friday close (UTC) is to its highest price of the past year, the more it rises over the following Saturday and Sunday together.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
