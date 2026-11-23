---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3725 USD
---
## Findings
- **F1:** Over the next 1 day the signal reverses: on 14 644 coin-days, the day's range relative to its 30-day mean range, multiplied by where the close sits in that range (from −1 at the low to +1 at the high), predicts the next day's return with a slope of −0.24 % per standard deviation and a t of −6.04. This is the only pattern of all the angles examined that stands far above chance.
- **F2:** The tested 5-day effect of range expansion in rising coins depends on which bars the grid starts on, so it is not robust. Within positive 20-day returns its slope t is 1.35 on the grid starting at position 0 (n=1418) and 2.96 on the grid starting at position 2 (n=1416). The range-times-close-location signal turns from t 1.38 to t −0.15 between the same two grids.
- **F3:** On the 5-day grid, the 2×2×2 split (range above or below its median, up or down day, 20-day return positive or not) puts its two extremes at opposite ends. Wide-range up days in rising coins are followed by +1.47 % of excess return (t 2.39, n 462). Narrow-range down days in falling coins are followed by −1.36 % (t −2.78, n 448). The other six cells lie between −0.74 % and +0.62 %, with |t| ≤ 1.25. Across eight cells these extremes are only marginal.
- **F4:** The book's gain rests on its tails. Its 20 best days sum to +1.62 and its 20 worst to −1.63, against a total of +2.02 over all days. On those best and worst days the coins moved +9.5 % and −12.7 %, so the book is carried by large market days rather than by steady timing.
- **F5:** Rising coins beat falling coins only in some years. The 5-day excess return with a positive 20-day return is +3.0 % in 2020 and +3.5 % in 2021, but −2.9 % in 2018 and −2.0 % in 2022. The yearly slopes of the range-times-close signal change sign from year to year, ranging from −0.048 to +0.066 with no |t| above 1.6.
- **F6:** Across coins, the 5-day range-times-close signal reaches significance only in XRP (t 2.28, n 474). It is negative but not significant in BTC, ETH and LTC (t −0.24 to −0.38).

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends.g1_wide-day-close-reverses-next-day` (from F1, F2): The further a coin's close sits toward the high of its day, and the wider that day's high-low range is relative to its average range over the past 30 days, the lower the coin's return over the next 1 day. The further its close sits toward the low of a wide day, the higher that return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
