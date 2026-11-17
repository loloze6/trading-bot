---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's moderate weekend move (Sunday close-to-close, up to roughly one to two usual daily moves) is undone over the next 3 days. The larger such a moderate move relative to the coin's usual daily move, the larger the move back, while its most extreme weekend moves continue in their own direction over the next day.
Consequence: A trader would fade ordinary weekend drifts but not the outsized weekend moves, which carry information and produced the book's largest losing positions.
Why:
- F3: Sizing is inverted at the extremes. The largest-rise quintile carries the biggest positions (mean |position| 0.81, mean |forecast| 14.9) but reverses least over 1 day (0.0017) and loses money (mean gain −0.0021). In the top quartile of |z| the 1-day reversal is about 0 in both trend states (−0.0009 and −0.0008), while the middle quartiles reverse most (0.015–0.018 in down-trends).
- F6: The 60 worst book days average −9.2% for the book while the coin's own day averages +1.6%, and the coin rose on 58% of them. The deepest falls are shorts held into a continuing rise, which is what drags Calmar to 0.061.
