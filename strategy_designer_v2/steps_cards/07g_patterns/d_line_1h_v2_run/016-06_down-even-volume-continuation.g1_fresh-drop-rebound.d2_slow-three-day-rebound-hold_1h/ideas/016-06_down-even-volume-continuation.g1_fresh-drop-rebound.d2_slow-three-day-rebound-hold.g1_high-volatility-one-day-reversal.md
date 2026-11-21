---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
line: 7.g patterns
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly volatility over the past 7 days is high, the larger its 1-day return, the more it moves the opposite way over the next 1 day, with most of that move inside those 24 hours.
Consequence: In turbulent stretches, fade a 1-day move and close within about a day instead of holding for three.
Why:
- F1: In the top third of each coin's 7-day hourly volatility, the 1-day return reverses over the next 1 day. The slope of the next-24h excess return on the standardised 1-day return is -0.0070 per sd (t -11.2, n 5413 non-overlapping cases). It holds in both halves of the windows (t -5.2 in w1-12, t -9.7 in w13-24) and in every coin when split on 1-day volatility (t -2.8 to -5.2). It is still -0.0066 per sd over the next 3 days (t -3.8, n 1751).
- F3: The tested rebound after a fresh drop in a 3-day fall is real but front-loaded, which is why the supporting check failed (-0.00125). After a 3-day fall:
