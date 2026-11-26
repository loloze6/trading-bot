---
line: 7.g patterns
backtest: 031-01.b1_wide-day-extends-up-run_1d
idea tested: 031-01.b1_wide-day-extends-up-run
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3737 USD
---
## Findings
- **F1:** The book mostly carries the market's own rise rather than the idea. Its daily returns correlate 0.72 with holding the coins, with a slope of 0.265 and an intercept of 0.039 % a day. By quintile of the holding day, the book's mean goes from −1.45 % on the worst holding days to +1.60 % on the best, against −5.36 % and +5.34 % for holding.
- **F2:** The book's timing adds nothing measurable. On grid bars where a position was held, the mean 3-day excess return is −0.01 % (4051 cases), against +0.03 % when flat (1816 cases). By quintile of the entry forecast, mean net trade results are 2.39 %, 3.29 %, 3.64 %, 2.55 % and 2.92 % (about 1355 trades each), with no rise toward the widest days.
- **F3:** The book's yearly results follow holding's sign. Its Sharpe is −1.09 in 2022 (holding −0.19 % a day) and 2.27 in 2020 (holding +0.42 % a day). The mean 3-day excess also swings by year, from −1.34 % in 2018 to +0.83 % in 2020.
- **F4:** The brief's reversal does not appear. Across both run directions, wide-and-flat days are followed by a 3-day excess in the run's direction of +0.25 % in down runs (t 0.30, 210 cases) and −0.07 % in up runs (t −0.13, 262 cases). Narrow-and-flat days give −0.41 % (t −0.78) and −0.36 % (t −0.81).
- **F5:** The widest-range days are followed by a 3-day excess of +0.89 % (t 2.00, 942 cases, 382 days) over all bars, and +1.26 % (t 2.07, 475 cases) inside 5-day up-runs. The lower quintiles are not graded: +0.47 %, +0.21 %, −0.11 % and −0.50 % in up-runs.
- **F6:** In 5-day down-runs, the days with the largest 1-day gain are followed by a 3-day excess of −1.46 % (t −2.76, 539 cases, 238 days). Days closing nearest their high are followed by −1.03 % (t −2.28, 539 cases). Both are again ungraded: the lowest 1-day-return quintile gives +0.41 % and the second −0.82 %.
- **F7:** About 75 quintile cells were read across returns, range, close location, body, volatility, regime, weekday and year. The largest |t| is 2.76 (F6) and only three cells reach |t| ≥ 2. That is about what chance alone would give over this many cells, and none of the three effects rises steadily across its quintiles.

## Ideas
- No ideas: Of the angles examined (past 1-, 5- and 20-day returns, range ratio, close location, body, volatility, run direction with wide/flat days, weekday, year, positions, trades by forecast, and the book against holding), no pattern stands out beyond what about 75 cells would give by chance (largest |t| 2.76, none graded). The book's profit is explained by the market's rise (F1–F3), not by a separate effect that a new idea could take up.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
