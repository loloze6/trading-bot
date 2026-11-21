---
line: 7.g patterns
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h
idea tested: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3583 USD
---
## Findings
- **F1:** The coins' own hourly bars rise strongly in the bars starting 20:00 and 21:00 UTC: +5.45 bp (t 6.75, n 17403) and +4.36 bp (t 5.66, n 17417). After 20:00 the 2-hour return is positive in every 24-hour-return quintile, from +2.1 to +19.5 bp. The middle quintile alone gives +10.1 bp (t 5.1, n 3394). It is also positive in every coin (t 2.9 to 4.6) and in both halves of the windows (w1-12: +3.8 bp, t 2.8; w13-24: +15.1 bp, t 9.0). So the evening rise is mostly not explained by a prior fall; the fall adds only in the most-fallen quintile (+19.5 bp, t 6.6).
- **F2:** The book loses even though the evening hours carry its whole gain. Per coin-day, positions in hours 20 and 21 earn +1.87 and +1.25 bp, while fees in hours 20, 21 and 22 cost 2.24, 0.54 and 2.23 bp, about 5.0 bp against 3.1 bp of gain. The 2-hour hold is too short to pay a round trip.
- **F3:** The 24-hour fall measured in units of 7-day hourly volatility predicts a rebound over the next 24 hours, on a non-overlapping daily grid. The most-fallen quintile then returns +54.6 bp (t 5.63, n 3334), against +1.4 to +5.9 bp for the middle quintiles and -8.6 bp for the top quintile. The rebound holds in every coin (t 1.5 to 3.1) and in both halves (+45 and +64 bp). It persists to 48 hours (+55.6 bp, t 4.6, n 3306). Across all days the slope of the next 24-hour return on the scaled 24-hour return is -27 bp per unit (t -4.07).
- **F4:** Opposite to the brief, the rebound after a fall is largest when the day's volume was spread evenly. In the most-fallen quintile, the next 24 hours return +85.0 bp (t 4.5, n 1102) in the tercile where the busiest hour holds the smallest share of 24-hour volume. They return +43.5 bp (t 2.8) in the middle tercile and +35.0 bp (t 2.2) in the most concentrated tercile. Across all days, the interaction of the scaled return with volume concentration is +146 bp (t 3.6), so concentrated volume weakens the reversal.
- **F5:** Among large moves (|scaled 24h return| > 1), the most efficient, grind-like moves (net move over summed absolute hourly moves, top tercile) reverse by -39.6 bp over the next 24 hours, signed in the move's direction (t -4.6, n 3904). Grinds do not continue, which goes against the brief's continuation leg.
- **F6:** Smaller calendar effects in hourly returns: hour 13 UTC returns -3.56 bp (t -3.8) and hour 2 returns -2.77 bp (t -3.8). Friday returns +2.64 bp (t 5.8) and Thursday -1.46 bp (t -3.2).

## Ideas
- `016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops.g1_daily-rebound-after-scaled-falls` (from F3, F2): Each coin rises over the next 1 day after a fall over the past 24 hours, and the larger that 24-hour fall in units of its 7-day hourly volatility, the larger the rise.
- `016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops.g2_even-volume-falls-rebound-more` (from F4, F5, F3): After a coin's 24-hour fall, the more evenly its volume was spread across those 24 hours (the smaller the share of the busiest hour), the larger its rise over the next 1 day.
- `016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops.g3_efficient-moves-partly-reverse` (from F5, F3): The more efficiently a coin moved over the past 24 hours (its net move large relative to the sum of its absolute hourly moves), the more of that move it gives back over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
