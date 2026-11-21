---
line: 7.d not profitable
backtest: 018-06_hourly-plunge-multiday-continuation_1h
idea tested: 018-06_hourly-plunge-multiday-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4057 USD
---
## Findings
- **F1:** The book loses by being short almost all the time against coins that rise. It was short on 95.8 % of bars with a mean allocation of -0.78, and it lost 0.42 bps per bar: -0.47 bps came from the coins' own rise and only +0.05 bps from timing. It closed 8287 short trades with a mean of -5.7 % before fees. Its forecast is non-zero on any negative 24-hour return, so 202702 bars were active.
- **F2:** The book's result is a mirror of the coin's. It gained in the windows where the coins fell (w14: book +0.45 % a day, coin -0.43 %; w7: +0.30 % against -0.47 %). It lost in the windows where they rose (w11: -0.55 % against +1.26 %; w21: -0.74 % against +0.57 %). It lost on all 6 coins, from -0.08 % to -0.22 % a day.
- **F3:** Over the 5-day horizon there is no continuation after a large 24-hour drop.
- **F4:** Over the next day a large 24-hour drop is followed by a rebound, and the rebound grows with the drop.
- **F5:** The rebound is concentrated in coins standing 30 % or more below their 30-day high.
- **F6:** In coins 30 % or more below their 30-day high, a 24-hour rise of more than 1 times the 30-day average daily move is followed by a fall the next day: strength -0.26, t -3.5, 279 cases, unusual move -1.3 %.
- **F7:** The continuation of large drops appears only around 10 days, after the rebound.

## Ideas
- `018-06_hourly-plunge-multiday-continuation.d1_hourly-plunge-next-day-rebound` (from F1, F3, F4): When a coin's 24-hour return, read at an hourly close, is a drop of several times its 30-day average absolute daily return, the price rises over the next 1 day by more than the coin's usual 1-day move. The larger the drop in those multiples, the larger the rise.
- `018-06_hourly-plunge-multiday-continuation.d2_deep-drawdown-plunge-rebound` (from F4, F5): While a coin stands far below its 30-day high, the larger its 24-hour drop in multiples of its 30-day average absolute daily return, the larger its rise over the next 3 days. The deeper the coin stands below that high, the larger the rise.
- `018-06_hourly-plunge-multiday-continuation.d3_deep-drawdown-bounce-fades` (from F5, F6): While a coin stands far below its 30-day high, the larger its 24-hour rise in multiples of its 30-day average absolute daily return, the larger its fall over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
