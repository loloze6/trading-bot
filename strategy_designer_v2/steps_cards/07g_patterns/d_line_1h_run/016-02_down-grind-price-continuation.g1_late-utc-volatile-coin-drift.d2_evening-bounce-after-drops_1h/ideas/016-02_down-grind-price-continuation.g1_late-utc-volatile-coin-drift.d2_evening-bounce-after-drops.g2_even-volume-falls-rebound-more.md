---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops
line: 7.g patterns
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After a coin's 24-hour fall, the more evenly its volume was spread across those 24 hours (the smaller the share of the busiest hour), the larger its rise over the next 1 day.
Consequence: A trader would favour buying the day after evenly-traded, grinding declines and scale down after declines driven by one high-volume hour.
Why:
- F4: Opposite to the brief, the rebound after a fall is largest when the day's volume was spread evenly. In the most-fallen quintile, the next 24 hours return +85.0 bp (t 4.5, n 1102) in the tercile where the busiest hour holds the smallest share of 24-hour volume. They return +43.5 bp (t 2.8) in the middle tercile and +35.0 bp (t 2.2) in the most concentrated tercile. Across all days, the interaction of the scaled return with volume concentration is +146 bp (t 3.6), so concentrated volume weakens the reversal.
- F5: Among large moves (|scaled 24h return| > 1), the most efficient, grind-like moves (net move over summed absolute hourly moves, top tercile) reverse by -39.6 bp over the next 24 hours, signed in the move's direction (t -4.6, n 3904). Grinds do not continue, which goes against the brief's continuation leg.
- F3: The 24-hour fall measured in units of 7-day hourly volatility predicts a rebound over the next 24 hours, on a non-overlapping daily grid. The most-fallen quintile then returns +54.6 bp (t 5.63, n 3334), against +1.4 to +5.9 bp for the middle quintiles and -8.6 bp for the top quintile. The rebound holds in every coin (t 1.5 to 3.1) and in both halves (+45 and +64 bp). It persists to 48 hours (+55.6 bp, t 4.6, n 3306). Across all days the slope of the next 24-hour return on the scaled 24-hour return is -27 bp per unit (t -4.07).
