---
line: 7.g patterns
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising_1h
idea tested: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4216 USD
---
## Findings
- **F1:** Among 3-day rises, the coin's excess return over the next 3 days is carried almost entirely by the most efficient fifth. Those cases have a raw efficiency ratio averaging 0.27 and earn +1.13 % above the coin's normal drift (t 2.78, 574 cases), about 6 times the backtest's 0.19 % round trip; the other four fifths range from -0.44 % to +0.33 %, none with |t| above 1.3.
- **F2:** The same top fifth of efficient 3-day rises keeps outperforming at twice the horizon: over the next 6 days its excess return is +0.167 of the coin's usual move (t 3.42, 562 cases), while the other fifths range from -0.050 to +0.016, all with |t| below 1.2.
- **F3:** The tested forecast blurs this effect. It standardises efficiency against its recent month and correlates only 0.72 with the raw ratio. Its top fifth earns +0.68 % in excess over 3 days (t 1.76), against +1.13 % (t 2.78) for the raw ratio's top fifth on the same cases.
- **F4:** Across all 3-day moves, the next 3 days' return in the move's direction, in units of the coin's usual move, rises with efficiency and falls with size and jumpiness. A regression on about 5,540 grid cases gives coefficients of +0.71 on efficiency (t 3.17), -0.067 on the move's size in standard deviations (t -2.36) and -0.86 on the largest hour's share of absolute moves (t -1.91). For a given size, steadier moves continue more, and larger or jump-made moves continue less.
- **F5:** The continuation of efficient rises is not stable across the record. The top-efficiency fifth earns +0.259 of a usual move in windows 13 to 24 (t 3.45, 295 cases) but only +0.017 in windows 1 to 12 (t 0.33, 280 cases). Five of six coins show a positive efficiency slope after controlling for size (t 1.0 to 1.7); ZEC is negative (t -0.41).
- **F6:** Some patterns did not stand out from the roughly 30 tables examined. These include the high short-term volatility ratio (top fifth +0.092 of a usual move, t 2.37, but t 3.0 in windows 1 to 12 and t 0.78 in windows 13 to 24), weekday and year groupings, volume concentration (|t| ≤ 1.97), and flat 3-day moves (middle return fifth -0.085 of a usual move, t -3.39, with no direction to trade).
- **F7:** The book's daily return moves with the coins' average by a beta of 0.48. It falls 8.4 % on its worst 1 % of days, when the coins fall 10.7 %, so the Calmar failure comes from shared market falls rather than from the signal's timing.

## Ideas
- `016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising.g1_steady-rise-six-day-continuation` (from F1, F2, F3, F5): The more efficiently a coin has risen over its past 3 days (its 3-day rise large relative to the sum of its absolute hourly moves, judged against that coin's whole history rather than its recent month), the more it keeps rising over the next 6 days.
- `016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising.g2_modest-steady-rise-continues` (from F4, F1): For 3-day rises of the same efficiency, the smaller the rise relative to the coin's usual 3-day move, the more the coin keeps rising over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
