---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops
line: 7.g patterns
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more efficiently a coin moved over the past 24 hours (its net move large relative to the sum of its absolute hourly moves), the more of that move it gives back over the next 1 day.
Consequence: A trader would lean against smooth, one-directional daily moves for about a day rather than follow them.
Why:
- F5: Among large moves (|scaled 24h return| > 1), the most efficient, grind-like moves (net move over summed absolute hourly moves, top tercile) reverse by -39.6 bp over the next 24 hours, signed in the move's direction (t -4.6, n 3904). Grinds do not continue, which goes against the brief's continuation leg.
- F3: The 24-hour fall measured in units of 7-day hourly volatility predicts a rebound over the next 24 hours, on a non-overlapping daily grid. The most-fallen quintile then returns +54.6 bp (t 5.63, n 3334), against +1.4 to +5.9 bp for the middle quintiles and -8.6 bp for the top quintile. The rebound holds in every coin (t 1.5 to 3.1) and in both halves (+45 and +64 bp). It persists to 48 hours (+55.6 bp, t 4.6, n 3306). Across all days the slope of the next 24-hour return on the scaled 24-hour return is -27 bp per unit (t -4.07).
