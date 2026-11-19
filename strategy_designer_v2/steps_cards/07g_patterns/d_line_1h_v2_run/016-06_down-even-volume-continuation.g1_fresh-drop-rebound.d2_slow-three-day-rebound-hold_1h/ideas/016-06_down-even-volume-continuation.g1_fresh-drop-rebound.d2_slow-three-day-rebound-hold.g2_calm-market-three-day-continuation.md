---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
line: 7.g patterns
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly volatility over the past 7 days is low, the larger its 3-day return, the further it keeps moving in the same direction over the next 3 days.
Consequence: In calm stretches, follow a 3-day move rather than fading it.
Why:
- F2: In the bottom third of 7-day hourly volatility, the sign flips: moves continue. The 1-day return predicts the next 3 days at +0.0066 per sd (t 2.3, n 1751) and the next 1 day at +0.0021 per sd (t 2.3, n 5414). The 3-day return predicts the next 1 day at +0.0038 per sd (t 4.2, n 5414). In the middle volatility third, the 3-day return predicts the next 3 days at +0.0074 per sd (t 3.1, n 1749). By coin over 3 days, five of six slopes are positive, but only XMR reaches t 2.8, so this is less firm than F1.
