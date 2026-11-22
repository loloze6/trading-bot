---
line: 7.d not profitable
backtest: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins_1h
idea tested: 028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3635 USD
---
## Findings
- **F1:** The quiet-volume rise the book fades is too small to pay for a trade: the case's total move is +0.03 % over 2 hours against a cost of 0.19 % per trade, so every coin's trades lose before fees (mean gross per trade from -0.11 % on BTC to -0.52 % on ZEC, net -0.21 % to -0.62 %), and the mean daily book return is -0.08 % to -0.18 % per coin while holding gains +0.07 % to +0.16 %.
- **F2:** The fade has no gradient over most of its range: after quiet-volume rises (volume 0.8-1.25 times its 30-day mean), the short-direction 2-hour excess is +0.013 % (t 0.53, 3905 cases) for rises of 1-2 usual moves and +0.011 % (t 0.24, 1323 cases) for 2-3. It reaches +0.24 % (t 2.1, 371 cases) only at 3-4 usual moves, then turns to -0.09 % (t -0.47, 130 cases) at 4-6. Over 6 hours the 3-6 bands run against the short (-0.33 %, -0.99 %).
- **F3:** The book holds its positions well past the 2-hour horizon, with little gain: 30319 position-bars are more than 10 hours after opening, the forecast is flat on 93 % of them, and they earn +0.003 % per bar. Trades last 3.1-4.3 hours on average, and the first held hour earns only +0.010 %.
- **F4:** Large hourly falls on surging volume are followed by a rebound that grows with the fall and is several times the cost. For falls of more than 3 usual moves, the 2-hour excess return in the long direction is +0.48 % (t 5.73, 1529 cases) at volume above 4 times its 30-day mean and +0.15 % (t 2.46, 1526) at 2-4 times. It is +0.003 % (t 0.02, 465) on ordinary volume.
- **F5:** The rebound after surging-volume falls (volume above 2 times its mean) is graded by the fall's size and lasts beyond 2 hours:
- **F6:** The surging-volume fall rebound (falls beyond 3 usual moves, volume above 2 times its mean, 2-hour excess) holds on every coin and in every year:
- **F7:** Large falls on unusually thin volume also rebound: for falls beyond 3 usual moves at volume below 0.8 times its mean, the 2-hour long-direction excess is +0.37 % (t 4.56, 471 cases).

## Ideas
- `028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins.d1_surging-volume-hourly-fall-rebounds` (from F4, F5, F6, F1): After an hour in which the coin falls far more than its typical hourly move over the past 30 days on volume several times its average hourly volume over the past 30 days, the price recovers part of that fall over the next two to four hours; the larger that hour's fall in typical moves and the larger its volume surge, the larger the recovery.
- `028-03_low-volume-up-fade.b2_quiet-up-hour-two-hour-fade.b2_quiet-up-fade-more-coins.d2_thin-volume-hourly-fall-rebounds` (from F7, F4, F2): After an hour in which the coin falls far more than its typical hourly move over the past 30 days while its volume is well below its average hourly volume over the past 30 days, the price recovers part of that fall over the next two hours; the larger that hour's fall in typical moves, the larger the recovery.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
