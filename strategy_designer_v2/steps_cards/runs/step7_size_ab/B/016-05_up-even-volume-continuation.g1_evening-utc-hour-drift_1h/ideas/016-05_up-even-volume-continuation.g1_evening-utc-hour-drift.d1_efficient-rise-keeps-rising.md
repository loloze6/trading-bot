---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift
line: 7.d not profitable
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more efficiently a coin has risen over its past 3 days (its 3-day rise large relative to the sum of its absolute hourly moves), the more it keeps rising over the next 3 days.
Consequence: A steady, efficient 3-day rise is a reason to be long for the following days, larger the steadier the rise, with a move several times a round trip.
Why:
- F5: Three-day moves made efficiently tend to continue (efficiency is the net 3-day return over the sum of its absolute hourly returns). In the most efficient fifth, the move continues by +91.6 bps over the next 3 days (t 3.3, 1,108 non-overlapping cases) and +104 bps over 7 days (t 2.3). That is 4.4 times a round trip.
- F6: The F5 effect is not graded across the middle fifths. Fifths 1 to 4 give +22, +0.3, +0.7 and −15.7 bps over 3 days, all |t| < 0.9. So the effect sits in the most efficient moves only.
- F7: The continuation of efficient moves is upward. After the most efficient rises, the coin gains +162 bps over 3 days. After the most efficient falls, it gains +9.6 bps, so a falling grind does not continue. The coin's normal 3-day drift is about +16 to +52 bps across volatility fifths.
- F2: The evening rise is too small to pay for a trade. The 20:00–22:00 move is 1.4 to 8.7 bps per case by coin, against a round trip of about 21 bps. Per case, the total move is 0.3 times the cost and the unusual move 0.2 times, in line with findings F2 and F11 of earlier runs.
