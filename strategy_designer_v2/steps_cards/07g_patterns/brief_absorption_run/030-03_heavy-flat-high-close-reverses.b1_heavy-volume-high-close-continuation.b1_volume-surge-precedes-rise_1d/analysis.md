---
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise_1d
idea tested: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3523 USD
---
## Findings
- **F1:** The coin's own 10-day return scaled by its 20-day daily volatility predicts its excess return over the next 10 days. On the non-overlapping 10-day grid, the pooled slope of the standardised excess return on it is 0.092 with t 3.58 over 1403 independent cases. That is stronger than the tested volume-ratio slope measured the same way, 0.045 with t 1.75 over 1403 cases.
- **F2:** The continuation is specific to a 10-day lookback and a 10-day horizon, and it is monotonic at the top end.
- **F3:** The momentum effect is absent in calm conditions. In the lowest 20-day-volatility tercile the 10-day-return slope is 0.044 (t 1.14, n 468), against 0.124 (t 2.88, n 467) in the middle tercile and 0.103 (t 1.99, n 468) in the high tercile. It is positive for 5 of 6 coins (ZEC t 2.70, LTC -0.45), but it changes sign by year (2020 t 3.21, 2018 t -1.34).
- **F4:** The tested volume surge works only when the coin is calm. Its slope is 0.180 (t 3.04, n 468) in the lowest 20-day-volatility tercile, 0.095 (t 1.44) in the middle and -0.014 (t -0.19) in the high tercile. In the calm tercile it is positive for 5 of 6 coins (XRP t 2.27, ETH -0.17), but by year it rests largely on 2024 (t 3.93, n 92).
- **F5:** The book's best days come after the coin had already run up. On the top 1 % of book days (174 days) the coin's prior 10-day return averaged +9.1 %, against +2.8 % before the worst 1 % and +1.2 % over all 17380 coin-days. On those best days the coin itself moved +16.4 % on the day.
- **F6:** The brief's close-location effect does not appear.

## Ideas
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.g1_volatility-scaled-ten-day-continuation` (from F1, F2, F5): The larger a coin's 10-day return relative to its own recent daily volatility, the more the coin keeps moving the same way over the next 10 days.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.g2_calm-market-volume-surge-rise` (from F4): When a coin's 20-day volatility is low, the heavier its volume on a day relative to its prior 20-day average, the more it rises over the next 10 days.
- `030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.g3_active-market-ten-day-momentum` (from F3, F1): When a coin's 20-day volatility is middling to high, the larger its 10-day return, the more it keeps rising over the next 10 days, and the larger its 10-day fall, the more it keeps falling.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
