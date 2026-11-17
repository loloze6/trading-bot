---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin, each day's daily return measured in its 20-day daily standard deviations is reversed over the next 1 day: the larger the day's move, the larger the following day's move against it, and the reversal is largest after Saturday and Sunday moves.
Consequence: Lean against every large daily move into the next day, not only Sunday's, so the edge is collected seven days a week instead of one.
Why:
- F1: The book holds a position only on the Sunday-to-Monday bar (share of non-zero positions on other days 0.000, mean |position| 0.41 on Sundays), so a real Sunday edge of 0.00129 per Sunday (t 2.51, n 2489) becomes a book mean daily return of only 0.0000562 against the 0.0005 required. Holding the coins returns 0.00118 a day with standard deviation 0.0407, a Sharpe of about 0.55 against the book's 0.16.
- F2: Fees cost 0.000898 per Sunday, about 70 % of the Sunday gain before fees of 0.00129, so the one-day-a-week round trip eats most of the edge.
- F3: The one-day reversal of a move measured in 20-day standard deviations is not specific to Sunday. The slope of the next day's excess return on minus the move is positive with t 3.47 for Wednesday's move, 5.27 for Saturday's, 3.53 for Sunday's, 2.50 for Thursday's and 2.36 for Tuesday's (n about 2270 each). Monday's move continues instead (slope -0.0022, t -2.44).
