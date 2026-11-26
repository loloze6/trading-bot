---
line: 7.b inconclusive
backtest: 031-02.b1.b1_strong-failed-rally-near-low_1d
idea tested: 031-02.b1.b1_strong-failed-rally-near-low
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3530 USD
---
## Findings
- **F1:** The tested shorts earned nothing beyond the coins' own drift: across 167 to 196 cases the mean unusual short move is -0.08 % at 5 days (t -0.11), -1.20 % at 10 days (t -0.83), -0.65 % at 20 days (t -0.20, 176 cases) and -9.4 % at 40 days (t -1.32), so no horizon shows the fall the idea predicts.
- **F2:** The effect does not grow with the rally: by forecast tercile the 20-day unusual short move is +1.47 % (small), -2.46 % (mid) and -1.10 % (large), all with |t| under 0.65. By raw 60-day-rise tercile (means 10, 22 and 70) it is -0.78 %, +0.13 % and -1.29 %, all with |t| under 0.23, and the Spearman correlation is only 0.15, against the graded effect the idea states.
- **F3:** The result is mixed across periods rather than weak everywhere: the short earned +6.0 % per case over 20 days in 2018-2022 (t 2.13, 110 cases), carried by 2018 (+22.5 %, t 3.78, 11 cases) and 2022 (+15.5 %, t 6.90, 26 cases), and lost -11.8 % in 2023-2025 (t -1.67, 66 cases), so the effect's sign flips with the year.
- **F4:** The year split follows no condition visible in a coin's own recent bars: by 10-day return, 20-day return, 20-day volatility and distance from the 20-day high, every tercile has |t| under 1.9, and no Spearman correlation exceeds 0.07 in size.
- **F5:** The effect is not concentrated in particular coins either: the 20-day unusual short move ranges from +5.7 % for XMR (t 1.42, 25 cases) to -15.0 % for ZEC (t -0.71, 21 cases), with no coin reaching |t| 2.
- **F6:** Moving the test inside the regime does not reveal the effect: on the 20-day grid, in-regime bars with a rally give +3.6 % (t 1.15, 87 bars), in-regime bars without a rally give +0.3 % (t 0.13, 232 bars), and out-of-regime bars give -1.0 % (t -0.44, 394 bars), so the near-low-rally situation is not clearly different from other bars.

## Ideas
- No ideas: The tested result is essentially zero (t -0.01), so more data is not called for. The only clear pocket is two bear years (F3), which no condition in a coin's own bars reproduces (F4, F5), so there is no part of the data where an amended idea could honestly be placed.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
