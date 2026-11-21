---
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after_1h
idea tested: 017-05_settlement-move-reverses-after
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3346 USD
---
## Findings
- **F1:** The book loses because the move it bets on is far smaller than a trade's cost. Its 62,957 trades are held a median of 2 hours and average −0.10 % before fees and −0.20 % after, with 41 % winning. Over all its bars it earns 1.03 bps per unit traded, against about 10.5 bps of cost per unit (findings F1 and F4). The idea's own size is +0.05 % per case, 0.2 times the 0.21 % round trip.
- **F2:** The reversal after settlement is real but small. Signed by the 2-hour move into settlement, the next 2 hours return 3.5 bps on average (t 5.57 over about 52,000 settlement bars). Even the largest tenth of pre-settlement moves (354 bps on average) gives back only 10.0 bps over 2 hours and 22.7 bps over 8 hours, at most about one round trip.
- **F3:** The effect is not tied to funding settlement. At non-settlement clock hours (bar starts 03, 11 and 19 UTC), the same signed 2-hour reversal is larger, 4.8 bps on average with t 8.23, against t 5.57 at settlement. In the top tenth of moves it is 23.0 bps against 10.0 bps. This meets the brief's own third falsification condition: the effect appears just as strongly when no funding is settled.
- **F4:** Among settlement times, only the one at 00 UTC shows a lasting give-back. It returns 6.8 bps over 2 hours and 12.0 bps over 8 hours. The 08 UTC settlement returns 0.8 and −2.8 bps, and the 16 UTC one 3.6 and 7.3 bps.
- **F5:** The reversal reaches a size that pays only for the most extreme moves, and it keeps growing for a day. This was measured at all hours on a non-overlapping 8-hour grid:
- **F6:** The same tail reversal holds for longer moves, and it is largest over a day:
- **F7:** The book's sizing also cuts it off where the move would pay. The forecast is capped at ±20, and its top fifth by forecast size (entries near 19.9) is the worst: −0.20 % before fees per trade, against about −0.08 % for the other fifths. The capped trades do not get a 24-hour hold, which is the horizon over which the large reversals of F5 build.

## Ideas
- `017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses` (from F1, F3, F5, F7): The larger a coin's 2-hour move relative to its usual 2-hour move, the more of it the coin gives back over the next 24 hours, with the give-back growing fastest for the most extreme moves.
- `017-05_settlement-move-reverses-after.d2_extreme-daily-run-reverses` (from F1, F5, F6): The larger a coin's 24-hour return relative to its usual 24-hour move, the larger its move in the opposite direction over the next 24 hours, with the reversal concentrated in the most extreme moves.
- `017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal` (from F2, F4, F5): The 2-hour return into the 00 UTC funding settlement runs opposite to the return over the 24 hours after it, and the larger the pre-settlement move relative to the coin's usual 2-hour move, the larger the move back.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
