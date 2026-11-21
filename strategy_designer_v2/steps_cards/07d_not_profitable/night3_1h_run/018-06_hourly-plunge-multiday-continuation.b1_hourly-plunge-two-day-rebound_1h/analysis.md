---
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound_1h
idea tested: 018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3665 USD
---
## Findings
- **F1:** The book is long on 84 % of all bars (81 % in w12 to w16), so its falls are mostly the coins' own falls. Its deepest fall is -57.8 % over 480 days from w12 to w16, while holding the coins fell -80.5 % over the same stretch. That gives a Calmar of 0.21 and a Sharpe below holding's.
- **F2:** The rebound after a plunge depends on how violent the coin's last week has been against its last month. The measure is the 7-day to 30-day hourly-volatility ratio at the case bar; 6118 cases over 48 hours.
- **F3:** The book's gain sits almost entirely in high-ratio bars.
- **F4:** Outside w12 to w16 the volatility gradient is steep. Mean excess return rises from -0.17 % to -0.30 %, +0.07 %, +0.84 % (t 3.59) and +1.37 % (t 5.20, n 740) across the ratio fifths, and the Spearman of forecast against outcome rises from 0.01 to 0.10.
- **F5:** Inside w12 to w16 the rebound is absent at every ratio.
- **F6:** Among high-ratio cases (ratio above 1), the rebound grows with the drop: +0.01 %, +0.73 % (t 3.49), +0.42 % and +1.98 % (t 4.22, n 331) across the forecast bands. For the full-size forecast band over all cases it is +0.88 % (n 678).
- **F7:** The past week's move shows the same split. Plunges after the largest 7-day falls rebound +0.75 % (t 2.94), and after the largest 7-day rises +1.02 % (t 3.98). Plunges after middling weeks lose -0.39 % (t -2.15) and -0.28 % (t -1.71). The 30-day return shows the same U shape (+0.55 % and +0.61 % at the ends, -0.58 % at t -3.07 just below zero).
- **F8:** Taken unconditionally, the idea is about the size of one trade's cost.

## Ideas
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.d1_plunge-rebound-in-turbulent-weeks` (from F2, F3, F4, F6, F8): When a coin's 24-hour return, read at an hourly close, falls by a large multiple of its 30-day average absolute daily return, the price rises over the next 2 days by more than the coin's usual 2-day drift. The larger the 24-hour drop in those multiples, and the higher the coin's hourly volatility over the past 7 days against its past 30 days, the larger the rise.
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.d2_plunge-after-an-extreme-week` (from F7, F2, F8): When a coin's 24-hour return, read at an hourly close, falls by a large multiple of its 30-day average absolute daily return, the price rises over the next 2 days by more than the coin's usual 2-day drift. The larger the 24-hour drop in those multiples, and the larger the coin's 7-day return in either direction against its usual 7-day move, the larger the rise.
- `018-06_hourly-plunge-multiday-continuation.b1_hourly-plunge-two-day-rebound.d3_turbulence-graded-capitulation-rebound` (from F1, F2, F3, F4): After a coin's 24-hour return falls by a large multiple of its 30-day average absolute daily return, read at an hourly close, the price rises over the next 2 days by more than the coin's usual 2-day drift. The rise is larger the higher the coin's 7-day hourly volatility against its 30-day hourly volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
