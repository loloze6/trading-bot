---
line: 7.g patterns
backtest: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1h
idea tested: 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3966 USD
---
## Findings
- **F1:** Inside the `trending` regime, on the 240-bar grid, the coin's 5-day return carries the whole forecast and the tested 20-day return adds nothing once both are in the same regression: 5-day slope 0.362 with t 7.36, 20-day slope 0.017 with t 0.92, n 1285.
- **F2:** The 5-day return grades the next 10 days' excess return in `trending`, but mostly at the extremes: the top 5-day quintile is followed by +6.44% (t 3.40, n 284), the bottom by -3.52% (t -4.49), and the middle three sit between -1.3% and -0.8%.
- **F3:** The 20-day momentum the idea uses works only inside the regime: outside `trending` its slope on 10-day excess return is -0.0020 (t -0.11, n 1305), and the 5-day slope drops from 0.35 (t 8.59, n 1421) in `trending` to 0.081 (t 2.37, n 1437) outside it.
- **F4:** The 5-day effect in `trending` is not steady across years: slopes are positive in 2020 (t 2.20), 2021 (t 5.10), 2024 (t 5.04) and 2025 (t 3.83), but negative or near zero in 2018 (t -0.83), 2019 (t -0.00), 2022 (t -1.68) and 2023 (t -0.63), so it rests on the bull years.
- **F5:** The next day's return, scaled by volatility, rises with the size of the past day's move whichever way it went: by quintile of the absolute 1-day z it goes 0.013 (t 0.93), 0.019, 0.019, 0.048 (t 2.40), 0.059 (t 3.60), with about 6056 daily cases per quintile; the largest falls (0.057, t 2.72) and the largest rises (0.050, t 3.23) are both followed by gains.
- **F6:** The 21:00–22:00 UTC hours earn 4.72 bps per hour against 0.36 bps for the other hours, t 4.2 to 10.5 in 7 of 8 years (2022: t -6.69); all 15 coins are positive (t 1.08 to 4.50); it is stronger in `trending` (t 9.60) than outside (t 4.72); but it does not grow with the past 24-hour return (quintile t from 1.45 to 7.94, not in order), so I give it no graded idea.
- **F7:** The book's daily gain sits on the days the coins rise: Wednesday, Friday and Saturday earn 0.00099, 0.00125 and 0.00124 (t 3.75, 4.97, 5.02), where the coins earn 0.0037 to 0.0040; the other days are near zero.

## Ideas
- `002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins.g1_five-day-momentum-inside-uptrends` (from F1, F2, F3, F4): While a coin's 50-day SMA is above its 200-day SMA, the higher its own 5-day return, the larger its return over the next 10 days.
- `002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins.g2_large-move-next-day-rebound-drift` (from F5): The larger a coin's 1-day move, in either direction, measured against its own 7-day hourly volatility, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
