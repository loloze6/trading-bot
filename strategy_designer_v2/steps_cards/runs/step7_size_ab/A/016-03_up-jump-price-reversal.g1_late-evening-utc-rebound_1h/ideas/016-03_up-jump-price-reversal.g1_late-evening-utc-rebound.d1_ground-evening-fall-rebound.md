---
brief: 016_grind-versus-jump-moves
source-idea: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound
line: 7.d not profitable
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin has fallen over the 24 hours up to the 20:00 UTC close, the more it rises over the next 2 days, only while that fall was made of many small hourly steps, and the more evenly the fall was spread across its hours, the larger the rise.
Consequence: A long taken after a deep, evenly ground evening fall and held for two days earns a move several times the round-trip fee, unlike a 2-hour hold.
Why:
- F1: Fees, not the forecast, sink the book: across the 11,085 trades (all long, median 120 minutes) the mean gross gain per coin is 0.01–0.15 % and the mean net is -0.09 to +0.05 %; the fee runs 0.107 % per unit of turnover, and the summed bar gains of 4.84 sit against costs of 9.38, giving a Sharpe of -1.08 and a mean daily return of -0.026 %.
- F2: The 2-hour effect is real but smaller than a round trip: decision bars with a positive forecast earn a 2-hour excess return of 0.095 % (t 5.31, n 8,596), and the best forecast fifth (the fourth) earns only 0.22 %, against about 0.21 % of round-trip fee; the shallowest-fall fifth earns 0.010 % (t 0.31) while still paying full fees.
- F4: The rebound after the deepest falls lasts for days: the lowest 24-hour-return fifth at the 20:00 close earns an excess of 0.27 % over 24 hours (t 2.69) and 0.28 % over 48 hours (t 2.14, n 3,454), while the middle fifths turn negative over the same horizons (-0.18 % at 24 h, t -2.62).
- F5: Among the deepest falls, those built from many small hourly steps rebound most and longest: the tercile with the smallest share taken by the largest hour earns 0.37 % over 2 h (t 4.53), 0.45 % over 24 h (t 2.17) and 0.74 % over 48 h (t 2.87, n 1,151); the middle tercile earns -0.007 % over 48 h and the jump-made tercile 0.11 % (t 0.55).
