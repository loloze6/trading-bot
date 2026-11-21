---
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses_1h
idea tested: 017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3977 USD
---
## Findings
- **F1:** The book's position does not follow its forecast. The position held has the forecast's sign on 49.9 % of bars, and its correlation with the forecast is 0.04. Sizing barely depends on the forecast: the mean |allocation| is 0.86 when |forecast| ≤ 0.5 and 0.91 when |forecast| > 14. Gain per bar is about 0 at every forecast level (-0.32 to +0.07 bps). The book's gross loss therefore comes before fees: -12.1 bps a day on BTC and -8.0 on ETH, against fees of 2.5 to 5.1 bps a day.
- **F2:** Per case, the idea's move is too small to pay. The unusual move is +0.08 % over 24 hours, against a round trip of 0.19 % (0.4 times the cost), with strength 0.016, well below F10's usual 0.05.
- **F3:** The give-back exists only in the most extreme 2-hour moves. On 24-hour grids, the fade earns 25 bps (t 3.0) in the 4th quintile of |scaled 2-hour move| and 26 bps (t 3.0) in the 5th. Quintiles 1 to 3 earn -3 to 13 bps (t ≤ 1.4). Only the top quintiles cover the 19 bps cost, at about 1.4 times.
- **F4:** The give-back of the extreme 2-hour moves is concentrated in moves ending around midnight UTC. Moves closing at 00:00, 01:00 and 02:00 UTC give back 24, 46 and 19 bps (t 2.6, 4.9, 2.0); 01:00 alone is 2.4 times the cost. Moves closing at the other funding times, 08:00 and 16:00, give back 7 and -3 bps (t 0.7, -0.4). Most other hours lie within ±12 bps and are not significant.
- **F5:** The give-back of extreme 2-hour moves grows with the coin's 30-day volatility. Off the settlement hours, it is -6.7 bps (t -2.8) in the lowest volatility tercile, 9.7 bps (t 3.2) in the middle and 16.6 bps (t 3.5) in the highest. On the 24-hour grid the top-quintile give-back is 52 bps (t 2.6) in the highest tercile against 6.6 bps in the lowest.
- **F6:** Whether the extreme move runs against the coin's 24-hour trend adds nothing, contrary to the brief. Moves against the trend give back 4.9 bps (t 1.3); moves with it give back 7.1 bps (t 2.9).
- **F7:** A slower situation carries a similar give-back. Scaled 24-hour moves in their 4th and 5th quintiles give back 33 and 22 bps over the next 24 hours (t 3.7, 2.5), but continue over 7 days (-84 and -132 bps). Scaled 72-hour moves do not reverse at all (-9 bps, t -1.0).

## Ideas
- `017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses.d1_midnight-extreme-move-reverses` (from F2, F3, F4): The larger a coin's 2-hour move relative to its usual 2-hour move, the more of it the coin gives back over the next 24 hours, with the give-back growing fastest for the most extreme moves, only for 2-hour moves that end in the first hours after midnight UTC.
- `017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses.d2_turbulent-extreme-move-reverses` (from F2, F3, F5): The larger a coin's 2-hour move relative to its usual 2-hour move, the more of it the coin gives back over the next 24 hours, with the give-back growing fastest for the most extreme moves, only while the coin's hourly volatility over the past 30 days is high, and more so the higher it is.
- `017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses.d3_extreme-daily-move-reverses` (from F1, F7): The larger a coin's 24-hour move relative to its usual 24-hour move, the more of it the coin gives back over the next 24 hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
