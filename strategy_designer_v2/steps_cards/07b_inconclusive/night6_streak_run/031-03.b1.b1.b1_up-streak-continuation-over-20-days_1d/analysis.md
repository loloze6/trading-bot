---
line: 7.b inconclusive
backtest: 031-03.b1.b1.b1_up-streak-continuation-over-20-days_1d
idea tested: 031-03.b1.b1.b1_up-streak-continuation-over-20-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4019 USD
---
## Findings
- **F1:** The 20-day result is on the predicted side but rests on a few large moves: the mean unusual move is +1.81 % (t 1.30, 1071 cases on 449 days), yet the median is −2.63 %, only 44.9 % of cases are positive, and with the tails clipped at 2.5 % the mean falls to +0.89 % (t 0.73).
- **F2:** The same cases show the effect clearly over shorter horizons: the unusual move is +1.24 % over 5 days (t 2.40) and +2.00 % over 10 days (t 2.38), on the same 1071 cases and 449 days, with medians of +0.03 % and +0.18 % against −2.63 % at 20 days.
- **F3:** Over 20 days the market's own swings drown the effect: the case means by year follow the plain up-month grid (2018 −15.5 % vs −9.7 %, 2022 −5.5 % vs −11.1 %, 2023 +4.5 % vs +5.8 %), while the 18 coins all have t below 1.3 (BTC +0.04 %, LTC −0.14 %, ZEC +6.8 %).
- **F4:** The grading the idea claims does not show at 20 days: the Spearman correlation of forecast with unusual move is −0.04; the lowest forecast third earns +3.09 % (t 1.70) against +1.67 % (t 0.81) for the highest third and +0.66 % for the middle third; streaks longer than 4 days earn −4.6 % (19 cases) and −3.2 % (22 cases).
- **F5:** The cases still beat plain up-month timing: the 20-day grid bars with a positive 30-day return have an unusual move of only +0.72 % (t 0.33, 503 cases on 76 days), against +1.81 % for the streak cases.
- **F6:** The cases come from all 19 coins over all four folds (1071 cases, 449 days), which is all the data available, so more data cannot raise the 20-day t.

## Ideas
- `031-03.b1.b1.b1.b1_up-streak-continuation-over-10-days` (from F2, F1, F3, F5, F6): The more days in a row a coin has closed higher, measured against the lengths of its own up-close streaks over the past 365 days, the more it keeps rising over the next 10 days, only while its 30-day return is positive.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
