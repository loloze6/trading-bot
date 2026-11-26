---
line: 7.b inconclusive
backtest: 059-01.b1.b1.d1.b1.b1.d1.d1_raw-scaled-rise-four-weeks_1d
idea tested: 059-01.b1.b1.d1.b1.b1.d1.d1_raw-scaled-rise-four-weeks
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3683 USD
---
## Findings
- **F1:** The test's zero comes from folds A and D. In folds B and C, the same regression of the coin-demeaned 28-day return on the forecast has a positive slope (t 1.70, 33 grid cases; 0.989 correlation between forecast and raw multiple, the same sign on 100 % of cases). Step 5's t over all folds is -0.04 on 188 cases, so folds A and D must point the other way.
- **F2:** Over the cases step 5 counted, the effect is too small to pay. The unusual move per case is +0.13 % (t 0.08 over 321 days), which is 0.023 of a usual 28-day move. That is below the 0.22 % cost of a trade, and the total move per case is -1.86 %.
- **F3:** The effect is clearer over 14 days than over 28. In the profile in folds B and C, the slope on the forecast has t 2.24 at 14 days (80 cases), against 1.70 at 28 days (33 cases) and 1.48 at 7 days (169 cases).
- **F4:** The giveback the idea predicts after a small rise is the clearest part of the data. Rises of up to half a usual week end below the coin's mean by -5.6 % over 7 days (t -3.16, 28 cases) and -13.6 % over 14 days (t -3.27, 14 cases). Rises of 1.5 to 2.5 usual weeks end +12.7 % above it over 14 days (t 2.34, 12 cases).
- **F5:** The effect is mixed across periods, which explains how the folds can cancel. The 14-day slope on the raw multiple is negative in 2018 (t -2.12, 14 cases) and 2019 (t -1.34, 20), and positive in 2020 (t 0.61, 23) and 2021 (t 1.23, 23). The 7-day slopes show the same split: -0.76 and -1.04 against +0.43 and +1.21.
- **F6:** The cases are few because the choppy-calm profile is rare. It covers 10 % of the 28-day grid bars, and the 28-day cases in folds B and C are spread over 10 coins with 1 to 7 cases each. The only more data available is hourly bars, and they cover the same period.

## Ideas
- `059-01.b1.b1.d1.b1.b1.d1.d1.b1_raw-scaled-rise-two-weeks` (from F1, F3, F4, F5): In a choppy, calm market, the larger a coin's rise over the past 7 days in multiples of its usual 7-day swing over the past 30 days, the larger its further rise over the next 14 days. A rise of only a fraction of a usual week gives back over the same 14 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
