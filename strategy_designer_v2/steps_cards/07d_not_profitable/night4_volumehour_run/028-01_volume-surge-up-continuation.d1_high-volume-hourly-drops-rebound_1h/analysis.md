---
line: 7.d not profitable
backtest: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound_1h
idea tested: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3570 USD
---
## Findings
- **F1:** The book is a near copy of holding the coins, not a bet on the idea. It is long on 89.2 % of bars with a mean allocation of 0.924, and short on none. It stays long on 88.3 % of the bars where the forecast is 0, while the median positive forecast is only 0.09. Of its mean bar gain of 5.48e-05, 5.33e-05 comes from the market's own rise and 1.55e-06 from timing. Its Sharpe is therefore 0.488 against holding's 0.636.
- **F2:** Calmar fails (0.1136) because the book rides the coins' long declines. Its deepest fall is -76.9 % over 277 days in windows w12 to w14, while the coins fell -79.5 % over the same days. In those windows the mean allocation was still 0.667, and 51.5 % of their bars had a negative 30-day return.
- **F3:** The rebound exists only when the coin's 30-day return is positive, and it shows over three days rather than one. In that state, cases on 30-day-up coins have a 72-hour excess return of +0.405 % (t 2.89, n 1973, strength 0.057) and a total move of +0.78 %, about 7 times the 0.11 % cost of a trade. The 6-hour excess is +0.09 % (t 2.25).
- **F4:** When the coin's 30-day return is negative, the same high-volume drops are followed by further falls. Cases on 30-day-down coins have a 72-hour excess of -0.41 % (t -2.28, n 1661, strength -0.053), and a 24-hour excess of -0.195 % (t -1.77, n 1712).
- **F5:** The 24-hour horizon the plan used sits where the two states cancel. Pooled, the 24-hour excess is -0.099 % (t -1.67, n 4990) and the total move is +0.05 %, half the cost. The forecast is not graded at 24 hours: the forecast quintiles run from -0.22 % to -0.01 % with no order.
- **F6:** The book's bar gain follows the coin's 30-day state. In the second-lowest 30-day-return quintile (median -8 %) the book loses -1.46e-04 per bar at an allocation of 0.98. In the middle and upper quintiles it gains 1.08e-04 to 1.74e-04. Bars with a falling 30-day return average -5.3e-05, against +1.38e-04 on rising ones.

## Ideas
- `028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.d1_high-volume-drops-rebound-uptrend` (from F2, F3, F5, F6): After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price rises over the next three days, only while the coin's 30-day return is positive; the larger that hour's fall relative to its typical hourly move, the larger the rebound.
- `028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.d2_high-volume-drops-continue-downtrend` (from F2, F4, F6): After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, while the coin's 30-day return is negative, the price keeps falling over the next three days; the larger that hour's fall relative to its typical hourly move, the larger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
