---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after.d1_extreme-two-hour-move-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 2-hour move relative to its usual 2-hour move, the more of it the coin gives back over the next 24 hours, with the give-back growing fastest for the most extreme moves, only while the coin's hourly volatility over the past 30 days is high, and more so the higher it is.
Consequence: A trader would fade violent 2-hour moves only in a coin's turbulent periods, where the give-back is several times a round trip, and refuse it in calm periods, where these moves continue.
Why:
- F2: Per case, the idea's move is too small to pay. The unusual move is +0.08 % over 24 hours, against a round trip of 0.19 % (0.4 times the cost), with strength 0.016, well below F10's usual 0.05.
- F3: The give-back exists only in the most extreme 2-hour moves. On 24-hour grids, the fade earns 25 bps (t 3.0) in the 4th quintile of |scaled 2-hour move| and 26 bps (t 3.0) in the 5th. Quintiles 1 to 3 earn -3 to 13 bps (t ≤ 1.4). Only the top quintiles cover the 19 bps cost, at about 1.4 times.
- F5: The give-back of extreme 2-hour moves grows with the coin's 30-day volatility. Off the settlement hours, it is -6.7 bps (t -2.8) in the lowest volatility tercile, 9.7 bps (t 3.2) in the middle and 16.6 bps (t 3.5) in the highest. On the 24-hour grid the top-quintile give-back is 52 bps (t 2.6) in the highest tercile against 6.6 bps in the lowest.
