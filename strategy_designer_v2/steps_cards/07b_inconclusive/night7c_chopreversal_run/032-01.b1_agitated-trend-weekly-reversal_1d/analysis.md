---
line: 7.b inconclusive
backtest: 032-01.b1_agitated-trend-weekly-reversal_1d
idea tested: 032-01.b1_agitated-trend-weekly-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3834 USD
---
## Findings
- **F1:** The tested short bet came out on the wrong side, not just short of the bar: per case the unusual 7-day move was -1.17 % in the short direction (t -1.03 over 220 days, 298 cases), and the slope on |forecast| was negative (-0.0027), so the strongest short bets did worst.
- **F2:** In folds B and C, on non-overlapping 7-day grid points, the largest 7-day rises, more than 1.5 of the 30-day daily standard deviation × √7, were followed by a further rise rather than a giving-back: the reversal gain was -4.80 % (t -2.35, 94 cases). For rises between 0.5 and 1.5 it was -1.69 % (t -1.40, 177 cases), and for moves between -0.5 and 0.5 it was -0.42 % (t -0.60, 350 cases), so the continuation grows with the size of the rise.
- **F3:** Inside the tested regime (30-day volatility at or above its 60-day mean, efficiency ratio at least 0.3), the same largest rises also continued: the reversal gain was -1.43 % (24 cases). Only smaller moves showed a reversal, from +4.4 % to +5.7 % in the bins below 1.5. The larger the rise the bet scales on, the less it reverses, which is the inverse of the grading the idea needs and explains F1's negative slope.
- **F4:** Outside the regime, 7-day moves continued on both sides, the opposite of the brief's chop reversal: the reversal gain was -1.86 % for rises (t -2.23, 372) and -1.71 % for falls (t -2.39, 375). In chop (efficiency ratio below 0.3) it was negative on every coin (-0.9 % to -4.4 %, LTC t -2.90, XRP t -2.93) and in every year (2018 t -2.11, 2020 t -2.90). It was strongest in calm chop (-6.63 %, t -3.25, 74).
- **F5:** The reversal after rises inside the regime that the idea predicts is small and uneven: +2.26 % on grid points (t 1.31, 65 cases). It is carried by XMR (+12.8 %, 6 cases) and ZEC (+6.3 %, 11). BTC, ETH, LTC and XRP sit between -1.0 % and +0.4 %. By year it was 2019 -0.98 % and 2020 +0.35 % against 2018 +6.4 % and 2021 +8.4 %. The effect is mixed rather than present in one clear part of the data.

## Ideas
- `032-01.b1.b1_large-weekly-rise-continues` (from F2, F3, F4, F1): When a coin's price has risen over the past 7 days by a large amount compared with its typical daily swing over the past 30 days, it tends to keep rising over the next 7 days. The larger that 7-day rise counted in 30-day daily swings, the larger the further rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
