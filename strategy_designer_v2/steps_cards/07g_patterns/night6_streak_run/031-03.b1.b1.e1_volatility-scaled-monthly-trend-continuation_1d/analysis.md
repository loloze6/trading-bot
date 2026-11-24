---
line: 7.g patterns
backtest: 031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation_1d
idea tested: 031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.6652 USD
---
## Findings
- **F1:** After a down day of at least 3 times the coin's 60-day daily volatility, the excess return over the next 3 days was +5.6 % (t 3.06, 82 cases). But the same cases over 5 days gave −3.5 % (t −1.52, 30 cases). The graded slope of the 3-day excess return on the size of the down day was not significant on any of three grid offsets (t −1.57, −0.51, −1.54; about 9,800 cases and 850 days each). Among the dozens of cuts examined, this one isolated bucket does not stand out from chance.
- **F2:** When the coin's 30-day volatility-scaled return was not positive, the slope of the 10-day excess return on that ratio was −0.029 (t −1.99, 1,650 cases, 229 days) on grid offset 0. On offset 5 it shrank to −0.016 (t −0.83, 1,689 cases). The deciles of the ratio were not monotone either: the two most negative deciles showed +0.09 % and −0.18 % against −2.2 % (t −1.93) in the middle-negative decile. So there is no reliable graded effect on the down side.
- **F3:** The tested ratio's 10-day slope had the same sign and similar size in every volatility tercile of the coin: 0.008, 0.014 and 0.014 (t 1.15, 1.68, 1.59) on offset 0, and 0.006, 0.016 and 0.013 (t 0.71, 1.62, 1.31) on offset 5. Volatility level does not separate where the tested idea works.
- **F4:** Excess next-day returns by weekday, with cases of the same day taken together, ranged from −0.27 % to +0.29 % with every |t| ≤ 1.64 (about 5,150 cases each). Unclustered, these differences had looked large (t up to 6.3), but they do not survive pooling and are not consistent from year to year: the weekday-1 mean was −1.3 % in 2018 and +1.2 % in 2021.
- **F5:** The coin's 10-day excess return after a positive 30-day ratio varied by year from −10.4 % (2018, t −2.54, 58 cases) and −3.8 % (2022, t −1.24) to +6.2 % (2021) and +3.4 % (2020). This is the year-to-year variability of the tested effect, not a separate pattern with a graded condition.
- **F6:** The book's worst 5 % of coin-days (book −5.4 %, coin −7.3 %) and its best 5 % (book +7.1 %, coin +9.4 %) both followed a prior 5-day coin rise of about +7.4 % and +7.5 %. The book's extreme days are its long exposure after rises moving with the coin, not a distinct setup. Its gain is concentrated in the longest-held quartile of trades (mean +58.5 % against −1.3 % to −1.9 % in the two shortest quartiles, about 1,400 trades each), which is the tested idea's own persistence.

## Ideas
- No ideas: Across the forecast's deciles, streaks, last-day moves, volatility levels, volatility ratios, weekdays, years, trades and the book's extreme days, nothing beyond the tested idea stood out from chance once same-day cases were pooled and grid offsets compared. The one bucket with t above 3 reversed sign over a slightly longer horizon and was not graded.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
