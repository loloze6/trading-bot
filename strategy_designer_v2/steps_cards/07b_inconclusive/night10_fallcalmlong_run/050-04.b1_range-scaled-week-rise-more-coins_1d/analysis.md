---
line: 7.b inconclusive
backtest: 050-04.b1_range-scaled-week-rise-more-coins_1d
idea tested: 050-04.b1_range-scaled-week-rise-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3319 USD
---
## Findings
- **F1:** The verdict's main measure is on the side the idea predicts but short of the bar: +0.63 % unusual 3-day move (t 1.83, 496 cases on 342 days). The idea already uses all 19 coins and all four folds of daily data, so no more daily data is left to add. In the explore half the same cases give +0.72 % (t 1.06, 102 cases on 80 days).
- **F2:** The effect is not graded, though the idea and the brief both require it to be. In the verdict the slope of the 3-day unusual move on the forecast is negative (-0.00037). In the explore half it is -0.000065 (t -0.06). The strongest forecasts (top quarter, forecast 15 to 20) earn -0.29 % over 3 days (t -0.21), against +2.12 % (t 1.83) for the second quarter (forecast 5 to 8).
- **F3:** The raw scaled rise shows the same thing. Its quarters earn +0.19 %, +1.67 %, +1.01 % and -0.10 % over 3 days, a hump with no rise into the largest moves. The 3-day slope on the raw value is -0.0033 (t -0.40), and the slope on the plain 7-day return is t 0.06.
- **F4:** No other horizon shows the effect clearly. In the explore half the unusual move is +0.04 % at 1 day (t 0.11), +0.72 % at 3 days (t 1.06), +1.66 % at 5 days (t 1.70), +1.12 % at 7 days (t 0.86) and +0.96 % at 10 days (t 0.56). The 7-day slopes on the forecast (t 0.99) and the raw value (t 0.72) stay under 1.
- **F5:** The effect does not live in one part of the data. By year it is mixed: 2018 +1.07 % (t 0.50), 2019 -0.63 % (t -0.81), 2020 +0.62 % (t 0.38), 2021 +2.70 % (t 1.97). By coin it is weak everywhere: ETH +1.37 % (t 1.06), BCH +0.80 % (t 0.57), XMR +0.66 % (t 0.54), ZEC +0.04 % (t 0.04). The cases where the signal day itself rose (+0.74 %, 69 cases) and those where it fell (+0.67 %, 33 cases) earn about the same.

## Ideas
- No ideas: The small positive carry-on after a calm-downtrend weekly rise is already measured on all the data available (F1). It does not grow with the size of the rise (F2, F3), and it is not concentrated in a horizon, coin, year or kind of signal day (F4, F5), so no amendment would give a clear answer.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
