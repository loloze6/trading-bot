---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation
line: 7.g patterns
backtest: 016-05_up-even-volume-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Each day, the coin rises over the two hours after 20:00 UTC by more than in its other hours. The rise is larger the higher its realised hourly volatility over the past 7 days.
Consequence: A long position held through the 20:00–22:00 UTC hours collects a rise that the rest of the day does not offer, sized up when the coin is volatile.
Why:
- F1: Across all 24 hours of the day, the coins' next-hour return is clearly highest from the 20:00 and 21:00 UTC bars, with means of +0.000545 (t 6.75) and +0.000436 (t 5.66) against hourly means mostly within ±0.0003. On those two hours pooled, all six coins are positive (t 2.98 to 4.44). Seven of eight years are positive (t 1.90 to 5.66); 2022 is the exception at −0.000218 (t −1.44).
