---
line: 7.b inconclusive
backtest: 060-01.b1.d1_bounce-inside-fresh-slide-fades_1d
idea tested: 060-01.b1.d1_bounce-inside-fresh-slide-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4237 USD
---
## Findings
- **F1:** The tested cases' unusual move in the short direction is clearest over the next 1 day, at +1.77 % (t 2.97, 304 cases on 141 days, folds B and C), and it fades with the horizon: +1.44 % over 2 days (t 1.60), +1.31 % over 3 days (t 1.48, the plan's horizon) and +0.33 % over 5 days (t 0.34). The test measured the idea at 3 days, past where it shows.
- **F2:** Over 1 day the cases' total move, drift included, is +1.59 % (t 2.68), about 7 times the 0.22 % cost of a trade. Over the plan's 3 days it is only +0.84 % (t 0.94) in folds B and C, and +0.12 % over all folds (0.5 times the cost).
- **F3:** The 5-day fall adds to the 1-day giveback. Up days in the profile with no prior 5-day fall give back +1.19 % over 1 day (t 1.90, 152 cases), against +1.77 % for the tested cases. Over 3 days, up days after a fall give +1.40 % (t 1.13, 143 cases) and up days without one give -0.67 % (t -0.42, 82 cases).
- **F4:** The 1-day giveback is spread across coins and years, not carried by one part of the data. It is positive in 9 of 10 coins (BTC +1.19 %, LTC +2.29 %, ZEC +1.34 %, ETH +1.23 % at 3 days; at 1 day over all up days, BTC t 2.06 and LTC t 2.15) and in every year from 2018 to 2021 (1-day means over all up days +1.56 %, +0.77 %, +0.39 %, +0.79 %).
- **F5:** The grading by the size of the rise is weak and mixed.
- **F6:** The test already used every coin and every fold the data holds (19 coins, folds A to D), so no more data is available. The answer is the idea amended to the horizon where the effect shows (F1, F2), not the same idea on more data.

## Ideas
- `060-01.b1.d1.b1_fresh-slide-bounce-fades-overnight` (from F1, F2, F3, F4, F5): In a falling, agitated market, a coin's one-day rise that comes after a fall over its last 5 days is followed by a fall over the next day that grows with the size of the rise against the standard deviation of its daily returns over the past 30 days and with the depth of that 5-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
