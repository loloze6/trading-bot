---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift
line: 7.d not profitable
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: Each day, the coin rises over the four hours after 21:00 UTC by more than over its other four-hour stretches, and the rise is larger the higher its realised hourly volatility over the past 7 days.
Consequence: Holding the evening long for four hours instead of two lets a volatile coin's rise run further, about 45 bps against about 37, for the same single round trip.
Why:
- F1: The book loses because each round trip costs about four times what it captures. Trades averaged -6.4 bps before fees and -16.4 bps after fees (17,075 trades of 120 minutes, 47 % gaining before fees). Per bar the position earned 0.09 bps against 0.44 bps of fees. The book's mean daily return was -6 to -11 bps on every coin, while holding the coin earned +7 to +15 bps a day.
- F3: The evening rise only covers a round trip of about 22 bps when the coin's own 7-day hourly volatility is at its highest. In volatility quintiles, the 20:00–22:00 return is +2.2, +0.2, +0.3, +2.2 and +19.2 bps (top quintile t 4.38, about 3,280 cases each). Measured from the 21:00 close, the top decile rises 37.1 bps over 2 hours (t 5.91) and 45.2 bps over 4 hours. The other deciles rise 4 to 14 bps over 2 hours.
- F5: The volatility-target sizing puts the most capital where the effect is weakest.
