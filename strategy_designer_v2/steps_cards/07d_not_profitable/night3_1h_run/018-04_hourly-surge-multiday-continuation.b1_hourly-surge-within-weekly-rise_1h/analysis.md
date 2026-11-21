---
line: 7.d not profitable
backtest: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise_1h
idea tested: 018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5600 USD
---
## Findings
- **F1:** The Calmar fails because of one long fall across the first three windows: the book's deepest fall is 58.5 % over 271 days from w1 to w3, while the coins' average chain fell 62.4 % over the same days. The book lost 16 %, 32 % and 21 % in w1, w2 and w3, against a yearly return of 35.2 %. The next falls are 38 % (w16), 38 % (w19) and 35 % (w21).
- **F2:** The idea is too small to pay on its own. Its unusual move is +0.12 % per case over 5 days, a strength of 0.007, which is 0.6 times the 0.19 % round-trip cost. The total move (+0.76 %) is 3.9 times the cost, so almost all of the book's gain is the coin's normal drift.
- **F3:** The book earns almost nothing while a coin's 30-day return is negative. Long bars in that state earn 0.145 bps per hour (t 0.9, 116,284 bars), against 1.121 bps (t 5.0, 147,459 bars) when the 30-day return is positive. On the coin itself, the next hour returns 0.37 bps after a falling 30 days and 1.04 bps after a rising one.
- **F4:** The gain grows with the 30-day return:
- **F5:** Trades show the same split. Trades entered after a 30-day return below −4.4 % net 1.45 % and 1.94 % on average, with a 10th percentile of −14.9 % in the lowest quintile. Trades in the middle and upper quintiles net 6.09 %, 4.45 % and 2.33 %.
- **F6:** The tested idea's own gradients are absent:
- **F7:** Trades are carried by a fat right tail. Over 5,216 long trades, the median net is −0.80 %, 43 % win, and 15 % lose more than 10 %, while the mean is +3.65 %. Trades whose first 24 hours fall more than 2.3 % net −1.85 % on average. Those that rise more than 2.7 % in that time net +11.1 %.
- **F8:** The book also gains when the coin's 3-day return is strongest. Bars with a 3-day return above 5.2 % earn 1.45 bps per hour, with +0.96 bps of timing. Bars with a 3-day return between −4.8 % and +1.4 % have −0.49 and −0.40 bps of timing.

## Ideas
- `018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.d1_surge-within-monthly-uptrend` (from F1, F3, F4, F5, F6): When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 5 days by more than the coin's usual 5-day return, only while its 30-day return is positive. The larger that 30-day return, the larger the rise.
- `018-04_hourly-surge-multiday-continuation.b1_hourly-surge-within-weekly-rise.d2_monthly-return-predicts-five-days` (from F2, F3, F4, F8): The larger a coin's 30-day return, read at an hourly close, the more its price rises over the next 5 days compared with its usual 5-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
