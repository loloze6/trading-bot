---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift
line: 7.g patterns
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: After a fall over the past 24 hours, the coin rises over the next 24 hours, and the rise is larger the larger that fall is relative to its realised hourly volatility over the past 7 days.
Consequence: A sharp fall that is large next to the coin's recent volatility is a reason to buy for a one-day rebound rather than to sell into it.
Why:
- F5: After a 24-hour fall that is large next to the coin's 7-day hourly volatility, the coin rebounds over the next 24 hours, and the rebound grows with the size of the fall. On non-overlapping 24-hour cases, the lowest decile of z (mean −1.72) is followed by +82.3 bp (t 5.43, n 1,624) and the second-lowest by +27.7 bp (t 2.20), against +12.2 bp for all cases. The slope on falls has t −4.88 (n 7,974), while rises show no slope (t −0.66).
- F6: The rebound after large falls in F5 holds in every coin, from +35 bp to +77 bp in the two lowest z deciles, and is positive in all 8 years, from +5.9 bp to +132 bp, with t of at least 1.8 in 6 of them.
