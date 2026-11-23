---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.d1_volume-surge-after-falling-day.g1_volatile-regime-fall-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The heavier a coin's day volume against its average of the past 20 days, and the nearer the day's close sits to the day's low, the more the coin rises over the next day. The rise grows with both together: a close at the low on heavy volume is followed by the largest gains.
Consequence: A trader buys a coin after a heavy-volume day that closed near its low, more the heavier the volume and the lower the close, and refuses the trade after quiet days or closes near the high.
Why:
- F1: On falling days, a pooled regression of the next-day excess return gives the close's distance from the day's high (low close) times log volume against its 20-day mean a coefficient of +0.0181 (t 4.10, n 7151), and low close alone +0.0099 (t 2.92). The fall's own depth in usual moves adds nothing once these are in (+0.0001, t 0.11). So the tested idea's rebound is carried by closes near the low on heavy volume, not by how deep the fall was.
- F2: Falling days in the top volume tercile that closed in the bottom third of their range gained +0.89 % excess the next day (t 4.78, n 870). The same low closes on low volume gained −0.09 % (t −0.54, n 795), and high-volume falls that closed near the high gained +0.14 % (t 0.67, n 749).
- F3: On all days, ranked by a graded score of low close times relative volume, next-day excess return rises steadily by quintile: −0.16 %, −0.14 %, −0.12 %, −0.01 %, then +0.37 % in the top quintile (t 3.64, n 2922). Over non-overlapping 3-day stretches the top quintile gains +0.64 % (t 2.01, n 888).
- F6: The top-score cases the idea misses are flat: up days at −0.22 % (t −0.78, n 508). Those where the idea is long earn +0.50 % (t 4.60, n 2413). That is about 2.6 times the 0.19 % cost of a trade, against the tested idea's 1.1 times for its unusual move.
