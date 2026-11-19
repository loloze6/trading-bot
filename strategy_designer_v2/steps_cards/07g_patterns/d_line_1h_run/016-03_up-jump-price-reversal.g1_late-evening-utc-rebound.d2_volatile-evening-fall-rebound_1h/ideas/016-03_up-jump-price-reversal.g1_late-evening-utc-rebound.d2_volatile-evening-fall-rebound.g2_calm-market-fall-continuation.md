---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: While a coin's 10-day hourly volatility ranks low against its past 30 days, the more it has fallen over its last 24 hours, the more it keeps falling over the next 24 hours.
Consequence: In calm markets a trader should refuse to buy 24-hour dips and can lean short in the direction of the fall, more so the larger the fall.
Why:
- F3: At the 20:00 close the 24-hour response to a 24-hour fall rises steadily with the 10-day volatility rank across five bins: -42.3 bp (t -5.01, n 4,624) in the calmest fifth, -2.9 (t -0.28), +20.4 (t 2.06), +29.2 (t 2.89), and +43.1 bp (t 5.63, n 2,938) in the most volatile fifth.
- F4: In calm regimes (volatility rank < 0.5) a 24-hour fall continues rather than reverses at closes 08:00–19:00 UTC, with slopes of -11 to -27 bp per standard deviation of fall (t -2.3 to -5.8, about 8,150 cases per hour); at the 20:00 close the slope is negative for all six coins (-11 to -49 bp) and in 6 of 8 years (2022 -60 bp, t -4.22; 2024 -47 bp, t -2.43).
