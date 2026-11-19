---
brief: 016_grind-versus-jump-moves
source-idea: 016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls
line: 7.g patterns
backtest: 016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After a 24-hour fall, the more evenly the fall is spread across its hours (the smaller its largest single hour's share of the hourly moves), the more the coin rises over the next 24 hours.
Consequence: A trader would expect a day-long rebound after broad, many-hour selloffs, and refuse to short them, more than after falls made in a single hour.
Why:
- F4: Among 24-hour falls, how the fall was made matters beyond its size, but not the way the brief expects. Pooled over coins, a regression of the next-24-hour excess return on the fall's size, its log 24-hour/30-day volatility ratio and its largest single hour's share of the summed absolute hourly moves gives:
