---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising
line: 7.g patterns
backtest: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound.b1_heavy-volume-rises-keep-rising_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: Over the next 24 hours the coin moves against its past 24-hour return: the further its 24-hour return has fallen below its typical daily move, the larger its rise over the next 24 hours.
Consequence: A trader would buy after a coin's day of unusually large fall and refuse to sell into it, expecting a partial rebound the next day.
Why:
- F3: A day's move partly reverses the next day. On non-overlapping 24-hour cells, the lowest quintile of the past 24-hour return (scaled by the typical move) is followed by an unusual 24-hour move of +38.7 bp (t 2.53, n 1063). The fourth and fifth quintiles are followed by -24.1 bp (t -2.09) and -18.6 bp (t -1.59). The correlation of past and next 24-hour move is -0.048 for BTC and -0.066 for ETH (about 2,650 cases each). The lowest quintile's rebound is positive in 7 of 8 years.
- F4: The tested signal adds little beyond these patterns. Across the 28 hourly-move by volume-ratio cells, only one reaches |t| above 2.5: hours falling more than 3 typical moves on volume above 4 times average, followed by +35.9 bp over 2 hours (t 2.58, n 353). That is a rebound, not a continuation, and at 24 hours no cell passes |t| 2.
