---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound
line: 7.d not profitable
backtest: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin falls far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, while the coin's 30-day return is negative, the price keeps falling over the next three days; the larger that hour's fall relative to its typical hourly move, the larger the further fall.
Consequence: A trader would sell, or refuse to buy, a sharp high-volume hourly drop in a coin that has fallen over the past month.
Why:
- F2: Calmar fails (0.1136) because the book rides the coins' long declines. Its deepest fall is -76.9 % over 277 days in windows w12 to w14, while the coins fell -79.5 % over the same days. In those windows the mean allocation was still 0.667, and 51.5 % of their bars had a negative 30-day return.
- F4: When the coin's 30-day return is negative, the same high-volume drops are followed by further falls. Cases on 30-day-down coins have a 72-hour excess of -0.41 % (t -2.28, n 1661, strength -0.053), and a 24-hour excess of -0.195 % (t -1.77, n 1712).
- F6: The book's bar gain follows the coin's 30-day state. In the second-lowest 30-day-return quintile (median -8 %) the book loses -1.46e-04 per bar at an allocation of 0.98. In the middle and upper quintiles it gains 1.08e-04 to 1.74e-04. Bars with a falling 30-day return average -5.3e-05, against +1.38e-04 on rising ones.
