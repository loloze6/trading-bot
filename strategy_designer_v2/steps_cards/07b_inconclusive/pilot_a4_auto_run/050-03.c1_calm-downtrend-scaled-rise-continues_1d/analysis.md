---
line: 7.b inconclusive
backtest: 050-03.c1_calm-downtrend-scaled-rise-continues_1d
idea tested: 050-03.c1_calm-downtrend-scaled-rise-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4598 USD
---
## Findings
- **F1:** Step 5's main measure is on the side the idea predicts but short of the bar: a mean 7-day excess return of +2.08 % with a day-clustered t of 1.697 over only 78 independent days (148 cases), with a positive slope (0.00148). The idea's size is +1.96 % per case (t 2.45, 192 days, 267 cases), a strength of 0.146, and its total move of +2.47 % is 7.4 times the 0.33 % a trade costs.
- **F2:** The cases are few. In the explore half the 7-day grid gives only 28 cases on 23 days (+2.51 %, t 1.23), and the record holds only BTC, DOGE and XMR, not the plan's six coins (step 6 lists BTC, DOT, XMR, INJ, GRT, TAO, DOGE, FIL), so the test ran on a small, partly different set of coins.
- **F3:** The effect is carried mostly by DOGE. Across all seven grid offsets, DOGE gives +12.6 % (t 5.76, 37 days) while BTC gives +0.81 % (t 0.80, 64 days) and XMR gives −0.44 % (t −0.42, 88 days). Without DOGE the mean is +0.09 % (t 0.11, 132 days).
- **F4:** The effect sits in the largest forecasts. The top third of scaled rises gives +5.53 % (t 3.58, 58 days, 70 % positive) against +1.01 % (t 0.80) for the bottom third and +1.05 % (t 0.69) for the middle third. Without DOGE the top third is still the best at +1.58 % (t 1.31), and in BTC it is +3.35 % (t 2.37, 20 days) while its lower two thirds are about 0.
- **F5:** The effect varies by period. The years 2020 (+8.0 %, t 4.72, 9 days) and 2021 (+10.3 %, t 5.00, 40 days) carry it. In 2018 it is −0.5 % (t −0.38, 61 days) and in 2019 −2.1 % (t −2.09, 46 days).
- **F6:** Inside the profile, bars with a positive forecast beat bars with a zero forecast on every one of the seven grid offsets. Positive-forecast bars give +1.2 % to +4.0 %; zero-forecast bars, where the coin did not rise, give −1.0 % to −2.9 % (offset 0: +2.51 %, t 1.23, against −1.83 %, t −0.96). This is the direction the idea predicts, without enough cases to be sure.
- **F7:** Other horizons do not do clearly better than the plan's 7 days. At 3 days the result is +1.52 % (t 1.88, 56 days), at 14 days +2.24 % (t 0.45, 12 days) and at 21 days −11.1 % (t −1.97, 9 days). The plan's horizon is not misplaced; it is under-sampled.

## Ideas
- `050-03.c1.b1_calm-downtrend-rise-continues-all-coins` (from F1, F2, F6): In a falling, calm market, a coin that has risen over the last 14 days keeps rising over the next 7 days, and rises further the larger its 14-day rise is in units of its 30-day average daily high-low range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
