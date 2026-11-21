---
brief: 016_grind-versus-jump-moves
source-idea: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops
line: 7.g patterns
backtest: 016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Each coin rises over the next 1 day after a fall over the past 24 hours, and the larger that 24-hour fall in units of its 7-day hourly volatility, the larger the rise.
Consequence: A trader would buy a coin after a steep volatility-adjusted daily drop and hold it about a day, a hold long enough to pay a round trip, and would refuse the trade when the coin has not fallen.
Why:
- F3: The 24-hour fall measured in units of 7-day hourly volatility predicts a rebound over the next 24 hours, on a non-overlapping daily grid. The most-fallen quintile then returns +54.6 bp (t 5.63, n 3334), against +1.4 to +5.9 bp for the middle quintiles and -8.6 bp for the top quintile. The rebound holds in every coin (t 1.5 to 3.1) and in both halves (+45 and +64 bp). It persists to 48 hours (+55.6 bp, t 4.6, n 3306). Across all days the slope of the next 24-hour return on the scaled 24-hour return is -27 bp per unit (t -4.07).
- F2: The book loses even though the evening hours carry its whole gain. Per coin-day, positions in hours 20 and 21 earn +1.87 and +1.25 bp, while fees in hours 20, 21 and 22 cost 2.24, 0.54 and 2.23 bp, about 5.0 bp against 3.1 bp of gain. The 2-hour hold is too short to pay a round trip.
