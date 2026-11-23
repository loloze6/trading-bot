---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall, measured in its usual daily moves and weighted by how high its 20-day volatility stands against its 120-day level, the more it rises over the next day, only after a large 20-day move in either direction. The rebound grows with the size of that 20-day move.
Consequence: A trader buys volatility-scaled sharp falls after a strong 20-day run-up or sell-off, and refuses them when the coin's last 20 days were ordinary.
Why:
- F6: The signal earns nothing when the coin's 20-day return is in its middle quartiles (+0.00 %, t 0.04; and -0.03 %, t -0.29). It pays after extreme 20-day moves: +0.25 % (t 1.95) in the lowest quartile and +0.52 % (t 3.86) in the highest. No-signal bars in the highest quartile earn +0.00 % (t 0.04), so the extreme move alone does not carry it.
- F2: The rebound exists only when volatility is elevated: on held bars, the next-day excess return is -0.36 % (t -2.79, n 1310) when the 20-day volatility is at or below 0.8 of its 120-day mean, +0.68 % (t 2.50, n 453) between 1.2 and 1.4, and +0.90 % (t 4.04, n 694) above 1.4. Signal bars with a ratio of at least 1.1 earn +0.59 % (t 3.99, n 1506), against -0.07 % (t -0.89, n 2872) below 1.1.
