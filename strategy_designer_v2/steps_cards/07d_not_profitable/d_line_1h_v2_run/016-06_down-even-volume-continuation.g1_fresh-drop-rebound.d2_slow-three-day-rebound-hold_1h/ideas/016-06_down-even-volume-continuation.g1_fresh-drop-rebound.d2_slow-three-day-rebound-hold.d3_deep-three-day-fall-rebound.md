---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The deeper a coin's 3-day fall, the more it rises over the next 3 days.
Consequence: Size rebound longs by the depth of the 3-day fall, not just by the last day's drop.
Why:
- F5: Most long positions sit on shallow 3-day falls, and these lose. The shallowest quarter of 3-day falls returns -0.0115 over the next 3 days (t -3.60, n 456), while the deepest quarter gains +0.0100 (t 2.05, n 457).
- F6: The book's gain rests on a few windows. Book Sharpe ranges from -2.43 (w14) and -2.20 (w7) to +3.20 (w11), and the windows where the coin fell (w2, w7, w14) are the book's worst. This matches the failed leave-one-out Sharpe (-0.015) and the Calmar (0.0014).
