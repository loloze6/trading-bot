---
line: 7.b inconclusive
backtest: 031-03.b1.b1_up-streak-continuation-in-uptrend_1d
idea tested: 031-03.b1.b1_up-streak-continuation-in-uptrend
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 3
cost: 0.6120 USD
---
## Findings
- **F1:** The tested move is on the predicted side but small at the plan's 5-day horizon: +0.38 % per case (t 1.04, 3360 cases on 1136 days), with a strength of 0.026. It grows steadily with the horizon: −0.06 % over 1 day (t −0.44), +1.08 % over 10 days (t 2.00, 3222 cases, 1089 days) and +1.92 % over 20 days (t 2.16, 2931 cases, 997 days), where the strength reaches 0.068. The test therefore measured the idea at a horizon shorter than the one where it shows.
- **F2:** The 20-day move is not just the 30-day-up regime itself. All non-overlapping grid points with a positive 30-day return earn only +0.72 % unusual over 20 days (t 0.32, 503 points) and +0.87 % over 10 days (t 0.80), against +1.92 % and +1.08 % after the streak cases.
- **F3:** The effect shows only when the coin's 60-day return is also positive. There the cases earn +4.41 % unusual over 20 days (t 2.63, 927 cases, 325 days) and +1.95 % over 10 days (t 2.05, 1149 cases, 400 days). With a negative 60-day return they earn −1.50 % over 20 days (t −0.79, 328 cases) and +0.44 % over 10 days (t 0.41).
- **F4:** The grading on streak length is weak at every horizon tested. The day-clustered slope of the unusual move on the forecast has t 1.32 at 5 days, 0.65 at 10 days and −0.18 at 20 days, and stays at t 0.95 over 20 days inside the 60-day-up cases. The 5-day forecast quintiles rise only loosely, from −0.03 % to +0.90 % (top quintile t 1.38). The raw streak-ratio terciles over 10 days read −0.23 %, +2.08 % (t 2.76) and +1.38 % (t 1.74).
- **F5:** Much of what drowns the effect is the market's own years. The 20-day unusual move after cases is −17.1 % in 2018 (t −6.64) and −5.7 % in 2022 (t −3.35), the bear years. It is positive in 2020 (+8.1 %, t 3.19), 2023 (+4.4 %, t 2.86) and 2024 (+4.6 %, t 2.05). It is positive on 16 of 18 coins with cases.
- **F6:** The test already used all available data: all 19 coins and folds A–D. So a rerun on more data is not possible, and the answer is to move the test to where the effect shows. Over 20 days a case's unusual move of +1.92 % (+4.41 % with a rising 60-day trend) is many times the 0.22 % cost of a trade.

## Ideas
- `031-03.b1.b1.b1_up-streak-continuation-over-20-days` (from F1, F2, F6): The more days in a row a coin has closed higher, measured against the lengths of its own up-close streaks over the past 365 days, the more it keeps rising over the next 20 days, only while its 30-day return is positive.
- `031-03.b1.b1.b2_up-streak-continuation-in-two-month-uptrend` (from F3, F4, F5, F6): The more days in a row a coin has closed higher, measured against the lengths of its own up-close streaks over the past 365 days, the more it keeps rising over the next 20 days, only while its 30-day return is positive and its 60-day return is positive.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
