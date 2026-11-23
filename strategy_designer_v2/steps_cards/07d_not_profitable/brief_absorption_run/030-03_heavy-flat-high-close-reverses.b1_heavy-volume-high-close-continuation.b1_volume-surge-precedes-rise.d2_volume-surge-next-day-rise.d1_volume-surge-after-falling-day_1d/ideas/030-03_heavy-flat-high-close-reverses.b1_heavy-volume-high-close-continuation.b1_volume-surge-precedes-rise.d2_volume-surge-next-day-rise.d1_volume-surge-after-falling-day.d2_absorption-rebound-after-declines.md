---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day
line: 7.d confirmed, not profitable
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The heavier a coin's volume on a down day relative to its own prior 20-day average, and the larger the fall, the more the coin rises over the next day. The rise is larger the more the coin has fallen over the previous 20 days.
Consequence: A trader weights the next-day long after a heavy-volume fall toward coins already in a 20-day decline, where the absorbing buyer's effect is strongest.
Why:
- F2: The effect lives only when the coin's recent volatility is high against its own longer volatility (20-day standard deviation of daily returns over the 120-day one, cut in thirds).
- F7: After a 20-day fall (lowest quarter of the 20-day return), signal bars give +0.27 % next-day excess return. Non-signal bars in the same quarter give -0.52 %. The signal works where selling is heavy, which agrees with F2.
