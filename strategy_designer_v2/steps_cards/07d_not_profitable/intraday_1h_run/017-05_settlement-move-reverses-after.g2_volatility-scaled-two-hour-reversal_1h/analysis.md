---
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal_1h
idea tested: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.2886 USD
---
## Findings
- **F1:** The book loses because of fees, not because the forecast fails. Its gain before fees averages 0.00234 a day (per-bar t 11.0), while fees average 0.0104 a day. That leaves a mean daily book return of -0.00803 and a Sharpe of -8.68 over 2,898 days.
- **F2:** The book trades far more than its edge can pay for. It turns over 0.40 of the book every hour, at about 10.7 bps of fee per unit of turnover. The 2-hour fade it trades earns only 3.36 bps per 2 hours across all bars (t 10.06, n 196,182), less than the cost of one round trip.
- **F3:** The gain sits in the large moves, but the book trades the small ones nearly as heavily. Gain before fees per bar rises from 0.0000005 in the lowest |forecast| quintile to 0.000302 in the highest, while turnover only rises from 0.31 to 0.52. The 2-hour fade on the top |move| decile earns 11.75 bps (t 7.44, n 19,620).
- **F4:** Volatility decides whether there is any reversal at all. For top-decile 2-hour moves, the next-2-hour fade earns 29.70 bps (t 7.68, n 6,542) in the highest 7-day-volatility tercile, against only 3.16 and 2.36 bps in the lower two. Yet the book turns over most in the calmest quintile (0.52 per bar, against 0.30 in the most volatile).
- **F5:** The reversal is much larger and slower at the 1-day scale. Fading the top-decile 24-hour move over the next 24 hours earns 51.68 bps (t 3.20, n 1,626). In the highest volatility tercile it earns 198.95 bps (t 5.14, n 543), while in the low and middle terciles it loses 28.41 and 15.89 bps.
- **F6:** The fade weakens quickly beyond the shortest horizon. Hourly returns' autocorrelation is -0.031 at 1 hour and -0.021 at 2 hours but near zero from 3 to 12 hours. The 2-hour fade's top decile earns only 10.68 bps over 6 hours (t 2.49), less per hour than over 2 hours.

## Ideas
- `017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal.d1_high-volatility-two-hour-reversal` (from F1, F2, F3, F4): A coin's 2-hour move is reversed over the next 2 hours by an amount that grows with the size of the move relative to its usual 2-hour move, and grows with the coin's 7-day hourly volatility, only while the coin's 7-day hourly volatility is high against its past month's level, where the reversal of the largest moves is several times its size in calmer weeks.
- `017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal.d2_daily-reversal-in-volatile-weeks` (from F1, F2, F5): A coin's 1-day return is reversed over the next 1 day by an amount that grows with the size of that return relative to its usual 1-day move, while the coin's 7-day hourly volatility is high against its past month's level.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
