---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 2-hour move relative to its usual 2-hour move, the more of it the coin gives back over the next 24 hours, with the give-back growing fastest for the most extreme moves, only for 2-hour moves that end in the first hours after midnight UTC.
Consequence: A trader would fade only the violent 2-hour moves into the UTC day's start, where the give-back is about twice a round trip, and refuse the same fade at other hours, where it is below cost.
Why:
- F2: Per case, the idea's move is too small to pay. The unusual move is +0.08 % over 24 hours, against a round trip of 0.19 % (0.4 times the cost), with strength 0.016, well below F10's usual 0.05.
- F3: The give-back exists only in the most extreme 2-hour moves. On 24-hour grids, the fade earns 25 bps (t 3.0) in the 4th quintile of |scaled 2-hour move| and 26 bps (t 3.0) in the 5th. Quintiles 1 to 3 earn -3 to 13 bps (t ≤ 1.4). Only the top quintiles cover the 19 bps cost, at about 1.4 times.
- F4: The give-back of the extreme 2-hour moves is concentrated in moves ending around midnight UTC. Moves closing at 00:00, 01:00 and 02:00 UTC give back 24, 46 and 19 bps (t 2.6, 4.9, 2.0); 01:00 alone is 2.4 times the cost. Moves closing at the other funding times, 08:00 and 16:00, give back 7 and -3 bps (t 0.7, -0.4). Most other hours lie within ±12 bps and are not significant.
