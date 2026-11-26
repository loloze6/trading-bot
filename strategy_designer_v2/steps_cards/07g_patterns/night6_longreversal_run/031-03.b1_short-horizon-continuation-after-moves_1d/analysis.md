---
line: 7.g patterns
backtest: 031-03.b1_short-horizon-continuation-after-moves_1d
idea tested: 031-03.b1_short-horizon-continuation-after-moves
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5804 USD
---
## Findings
- **F1:** Every gain of the book came from its long side and from the coins' own rise. Long bars earned a mean of +0.147 % per bar (8650 bars, sum +12.67), while short bars lost −0.042 % per bar (8704 bars, sum −3.65). The book's mean daily return was below holding the coin for all six coins (for example XMR −0.001 % against +0.107 %, and ZEC +0.003 % against +0.155 %).
- **F2:** The tested continuation is not graded in the bars. The clustered slope of the 10-day move beyond drift (in usual-move units) on the 20-day z was t 1.17 (1403 cases, 255 days), and on the 60-day z it was t 1.04 (827 cases, 151 days). At 20 days the slopes were t 0.46 and t 0.82. The forecast's quintiles were not monotone over 10 days (+0.066, −0.085, −0.062, −0.017, +0.095, no |t| above 1.72).
- **F3:** The size of the 20-day move, whatever its sign, did not reliably predict a larger move in its own direction.
- **F4:** The brief's own reversal did not appear at this horizon either. The 60-day-move quintiles over the next 20 days were not monotone (+0.038, −0.278, +0.060, +0.080, +0.075 usual moves). Their only |t| above 2, the second quintile at −3.6, was unclustered and on 78 cases. Per-coin Spearman correlations of the 60-day return with the next 20 days ran from −0.078 to +0.145, with no p below 0.25.
- **F5:** The strong unclustered rebound after a large down day did not hold up when cases on the same day were taken together.
- **F6:** The next-day reversal after daily moves larger than 1.5 usual moves did not stand out once the number of cuts I looked at is weighed.
- **F7:** Saturday's excess return (+0.066 usual moves, clustered t 2.18 over 414 days) was the only weekday above 2 of seven. It weakened in the second half of the windows (t 2.06 in w1–12, t 1.16 in w13–24), which does not survive the seven weekdays tested.

## Ideas
- No ideas: Across the forecast, the 5-, 20- and 60-day moves, volatility levels, volatility ratios, weekdays, the day after large moves, coins, years, halves and the book's sides, no pattern stood out from chance once same-day cases were taken together and the many angles weighed (F2–F7). The book's only steady gain was the coins' own rise on its long bars (F1), which is holding the coins, not a new idea.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
