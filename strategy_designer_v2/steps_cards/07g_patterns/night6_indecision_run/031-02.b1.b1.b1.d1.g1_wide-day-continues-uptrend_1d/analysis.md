---
line: 7.g patterns
backtest: 031-02.b1.b1.b1.d1.g1_wide-day-continues-uptrend_1d
idea tested: 031-02.b1.b1.b1.d1.g1_wide-day-continues-uptrend
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4846 USD
---
## Findings
- **F1:** In coins whose 20-day return is positive, the unusual 3-day move rises with the day's range against its 20-day average. At or below 0.7 times the average it is -0.47 % (t -1.16). From 1.3 to 1.6 times it is +0.74 % (t 1.29), from 1.6 to 2.0 times +1.10 % (t 1.63), and above 2.0 times +2.97 % (t 2.57, 385 cases on 190 days). In coins whose 20-day return is negative there is no such grading: above 2.0 times the move is +0.32 % (t 0.18, 70 days).
- **F2:** In coins whose 20-day return is positive, the unusual 3-day move also rises with the day's volume against its 20-day average. It is -0.21 % (t -0.51) at or below 0.7 times the average and -0.22 % (t -0.59) from 0.7 to 1.0 times. It is +0.78 % (t 2.05, 444 days) from 1.0 to 1.5 times, +0.97 % (t 1.90, 315 days) from 1.5 to 2.5 times, and +1.90 % (t 1.24, 162 days) above 2.5 times.
- **F3:** The brief's reversal on a wide day that closes flat does not appear in coins whose 20-day return is positive; wide days there are followed by a rise wherever the close lands. On days with range at least 1.5 times the average, a close in the low third gives +1.25 % (t 1.13), the middle third +2.09 % (t 1.92) and the top third +2.06 % (t 2.21). A down day gives +2.43 % (t 2.23, 114 days) and an up day +1.57 % (t 2.03, 260 days).
- **F4:** The rise after wide days in up-trending coins depends on the year. It was negative in 2018 (-2.86 %, t -1.30) and 2022 (-2.15 %, t -1.08), the two years the coins fell (mean daily coin return -0.35 % and -0.26 %). The book also lost in those two years: -0.034 % and -0.013 % a day, against up to +0.149 % a day in 2020.
- **F5:** In coins whose 20-day return is positive, a close at a new 20-day high is followed by +1.05 % over 3 days (t 1.78, 332 days). Closes 2 % to 15 % below the high give between -0.14 % and +0.26 % (t under 0.7), so this does not stand apart from the range effect it overlaps with.
- **F6:** After a one-day fall of more than 10 %, all coins rose +3.43 % more than usual over 3 days (t 2.22, 65 days). A fall of 5 % to 10 % gives only +0.15 % (t 0.19). Because this is one ungraded cell among roughly fifty I looked at, I cannot tell it from chance.
- **F7:** The weekday of the bar shows no 1-day unusual move: all seven weekdays have t between -1.16 and +1.80. Volatility quintiles show no consistent pattern either: none reaches |t| 2.2.
- **F8:** The book's trades do not pay more the higher the forecast at entry. Mean net profit is +3.37 % between forecasts 7.5 and 10, +8.06 % between 10 and 13, +3.30 % between 13 and 16, and +6.29 % above 16. The size of the position adds little beyond being in the trade.

## Ideas
- `031-02.b1.b1.b1.d1.g1.g1_heavy-volume-continues-uptrend` (from F2, F1, F3): In a coin whose 20-day return is positive, a day whose traded volume is high compared with its average daily volume over the past 20 days is followed by a further rise over the next 3 days, and the higher the volume against that average, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
