---
line: 7.d not profitable
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift_1h
idea tested: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3961 USD
---
## Findings
- **F1:** The book loses because each round trip costs about four times what it captures. Trades averaged -6.4 bps before fees and -16.4 bps after fees (17,075 trades of 120 minutes, 47 % gaining before fees). Per bar the position earned 0.09 bps against 0.44 bps of fees. The book's mean daily return was -6 to -11 bps on every coin, while holding the coin earned +7 to +15 bps a day.
- **F2:** The book holds one hour too early. The coin's hourly rise is concentrated from 21:00 to 23:00 UTC: +5.45 bps (t 6.75) for 21:00–22:00 and +4.36 bps (t 5.66) for 22:00–23:00. The 20:00–21:00 hour averages only +0.45 bps (t 0.55). The book holds 20:00–22:00 (position 0.49 on both bars), so it earns only 0.24 + 1.96 bps per bar and misses the 22:00–23:00 hour.
- **F3:** The evening rise only covers a round trip of about 22 bps when the coin's own 7-day hourly volatility is at its highest. In volatility quintiles, the 20:00–22:00 return is +2.2, +0.2, +0.3, +2.2 and +19.2 bps (top quintile t 4.38, about 3,280 cases each). Measured from the 21:00 close, the top decile rises 37.1 bps over 2 hours (t 5.91) and 45.2 bps over 4 hours. The other deciles rise 4 to 14 bps over 2 hours.
- **F4:** The forecast grades by volatility measured against its own recent past, and that measure carries no gradient. Quintiles of 7-day volatility relative to its 90-day median give +1.0, +4.3, +6.4, -1.0 and +7.6 bps, against the clear gradient in the volatility's own level (F3).
- **F5:** The volatility-target sizing puts the most capital where the effect is weakest.
- **F6:** The evening rise varies by year.

## Ideas
- `016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_late-evening-rise-in-volatile-coins` (from F1, F2, F3, F4, F5): Each day, the coin rises over the two hours after 21:00 UTC by more than in its other hours, and the rise is larger the higher its realised hourly volatility over the past 7 days, taken as its own level rather than against its recent past.
- `016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_four-hour-volatile-evening-rise` (from F1, F3, F5): Each day, the coin rises over the four hours after 21:00 UTC by more than over its other four-hour stretches, and the rise is larger the higher its realised hourly volatility over the past 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
