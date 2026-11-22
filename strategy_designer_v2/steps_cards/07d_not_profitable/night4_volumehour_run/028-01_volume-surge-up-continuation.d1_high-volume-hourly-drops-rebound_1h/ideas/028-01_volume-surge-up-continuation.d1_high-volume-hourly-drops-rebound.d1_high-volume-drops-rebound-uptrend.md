---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound
line: 7.d not profitable
backtest: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price rises over the next three days, only while the coin's 30-day return is positive; the larger that hour's fall relative to its typical hourly move, the larger the rebound.
Consequence: A trader would buy a sharp high-volume hourly drop only in a coin that has risen over the past month, hold it about three days, and stay out of such drops in a falling coin.
Why:
- F2: Calmar fails (0.1136) because the book rides the coins' long declines. Its deepest fall is -76.9 % over 277 days in windows w12 to w14, while the coins fell -79.5 % over the same days. In those windows the mean allocation was still 0.667, and 51.5 % of their bars had a negative 30-day return.
- F3: The rebound exists only when the coin's 30-day return is positive, and it shows over three days rather than one. In that state, cases on 30-day-up coins have a 72-hour excess return of +0.405 % (t 2.89, n 1973, strength 0.057) and a total move of +0.78 %, about 7 times the 0.11 % cost of a trade. The 6-hour excess is +0.09 % (t 2.25).
- F5: The 24-hour horizon the plan used sits where the two states cancel. Pooled, the 24-hour excess is -0.099 % (t -1.67, n 4990) and the total move is +0.05 %, half the cost. The forecast is not graded at 24 hours: the forecast quintiles run from -0.22 % to -0.01 % with no order.
- F6: The book's bar gain follows the coin's 30-day state. In the second-lowest 30-day-return quintile (median -8 %) the book loses -1.46e-04 per bar at an allocation of 0.98. In the middle and upper quintiles it gains 1.08e-04 to 1.74e-04. Bars with a falling 30-day return average -5.3e-05, against +1.38e-04 on rising ones.
