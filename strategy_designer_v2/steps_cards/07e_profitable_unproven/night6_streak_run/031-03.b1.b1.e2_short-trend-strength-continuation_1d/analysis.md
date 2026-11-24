---
line: 7.e profitable but not proven
backtest: 031-03.b1.b1.e2_short-trend-strength-continuation_1d
idea tested: 031-03.b1.b1.e2_short-trend-strength-continuation
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4430 USD
---
## Findings
- **F1:** The book's gain is almost all earned after the largest volatility-scaled 10-day rises. Bars whose prior 10-day return was in the top fifth relative to 60-day volatility (median 4.43 daily standard deviations) carry 25.20 of the 28.56 summed position gain and 18.18 of its timing part. The other four fifths together add 3.36 in gain and -2.95 in timing.
- **F2:** The book's mean of 0.086 % a day splits into 0.045 % from the market's own rise and 0.048 % from timing. The timing t is 1.66 over 2898 days, so on its own it cannot be told from 0. Being in a position adds nothing on average: the coin's daily return is 0.148 % on days in a position and 0.142 % on days out (Welch t 0.09).
- **F3:** The move after rises is not graded across the whole range; it shows only at the extreme. On the non-overlapping 5-day grid, the unusual move is -1.09 %, -0.31 % and +0.53 % in the 7th to 9th deciles of the scaled 10-day return. In the top decile (median 6.36) it is +2.37 %, with day-grouped t 2.42 over 537 cases on 165 days.
- **F4:** The effect is larger over 10 days than over the plan's 5. The top decile's unusual move is +4.42 % over 10 days (day-grouped t 1.99, 265 cases, 84 days) against +2.37 % over 5. The OLS slope of excess return on the raw scaled rise, among rises only, has t 4.09 over 10 days (1309 cases) and 3.62 over 5 days (2720 cases). Neither slope t is clustered by day.
- **F5:** The plan's forecast standardised the scaled rise against its own past 61 values, and on that forecast the slope t was 1.98 and the cases' unusual move -0.01 %. On the raw scaled rise, the slope t over 5 days was 3.62 (F4), so the test measured a different quantity from the one the book's sizing effectively loads on.
- **F6:** The top-fifth continuation is broad across coins but depends on the year. Over 10 days its unusual move is positive for 17 of 19 coins (89 %) and for 13 of 19 over 5 days. By year it runs from +13.3 % (2021) and +6.6 % (2020) down to -6.5 % (2022) over 10 days.
- **F7:** The book's profit is concentrated in a few days: the top 1 % of days hold 87 % of the summed daily book returns.

## Ideas
- `031-03.b1.b1.e2.e1_extreme-scaled-rise-continues` (from F1, F3, F4, F5, F6): The larger a coin's 10-day return measured in its own 60-day daily volatility (not compared with that measure's own recent history), the more the coin rises over the next 10 days beyond its normal drift. The effect grows sharply for the most extreme rises.
- `031-03.b1.b1.e2.e2_raw-scaled-rise-continuation` (from F1, F3, F5, F7): The larger a coin's 10-day return in units of its own 60-day daily volatility, the larger its rise over the next 5 days beyond its normal drift. The move is concentrated in the coin's most extreme rises.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
