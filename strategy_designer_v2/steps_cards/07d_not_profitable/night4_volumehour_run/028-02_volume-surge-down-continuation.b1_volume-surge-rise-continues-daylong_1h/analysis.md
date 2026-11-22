---
line: 7.d not profitable
backtest: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong_1h
idea tested: 028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3585 USD
---
## Findings
- **F1:** The book is in effect holding the coin: it is positioned on 92.4 % of bars with a mean allocation of 1.00 when in, although the forecast is positive on only 49.3 % of bars (trades last 103 hours on average against a 24-hour bet), and of its mean gain of 0.0062 % per bar, 0.0054 % comes from the market's own rise and only 0.0009 % from timing.
- **F2:** The book therefore fails both measures in the same way holding fails them. Its Sharpe is 0.596 against holding's 0.636. Its deepest fall is -71 % against holding's -80 %, giving a Calmar of 0.25 against 0.27. On the 1482 of 2898 days spent more than 30 % below its peak, it lost 0.12 % a day while the coins lost 0.10 %.
- **F3:** The idea's own move is too small to pay. At the book's 5792 entries the unusual 24-hour move is +0.026 % (t 0.49), and at step 5's 5008 cases it is +0.06 %, which is half the 0.11 % cost of a trade. The larger-forecast half did worse than the smaller half (-0.079 %), and among up-hour grid cells the product of rise and relative volume shows no grading in either the 7-day-up or the 7-day-down group.
- **F4:** What does separate the entries is the trend before them. Entries in the top quintile of the prior 7-day return gain +0.32 % unusual over 24 hours (t 2.55, n 1091), while the middle quintiles lose -0.15 % and -0.14 %. By prior 30-day return, the second quintile loses -0.30 % (t -2.48) and the top two quintiles gain +0.19 % and +0.21 %.
- **F5:** The trend carries the effect on any bar, not only after a volume surge. Over all 24-hour grid cells, the top prior-7-day quintile gains +0.25 % unusual (t 1.96, n 1072) and the second and third quintiles lose -0.14 % and -0.16 %. While in position, the book earns +0.0153 % per bar when the 30-day return is positive and -0.0052 % when it is negative (52975 and 44419 bars).
- **F6:** Within the surge itself, volume matters more than the size of the hour's move. Entries in the top quintile of volume against its 30-day mean gain +0.36 % unusual (t 2.44, n 1072), while entries in the top quintile of the hour's scaled rise gain -0.05 % (t -0.32).

## Ideas
- `028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.d1_volume-surge-within-uptrend` (from F1, F2, F4, F5): After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next 24 hours, only while the coin's 30-day return is positive. The larger that hour's rise times its relative volume, and the larger the 30-day return, the larger the further rise.
- `028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.d2_seven-day-momentum-continues-daily` (from F4, F5, F2): The higher a coin's 7-day return, the more it keeps rising over the next 24 hours, beyond its normal drift.
- `028-02_volume-surge-down-continuation.b1_volume-surge-rise-continues-daylong.d3_extreme-volume-up-hour-continuation` (from F3, F6): After an hour whose volume is several times its 30-day hourly average and whose return is positive, the price keeps rising over the next 24 hours. The larger the volume relative to its 30-day average, the larger the rise, whatever the size of that hour's move.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
