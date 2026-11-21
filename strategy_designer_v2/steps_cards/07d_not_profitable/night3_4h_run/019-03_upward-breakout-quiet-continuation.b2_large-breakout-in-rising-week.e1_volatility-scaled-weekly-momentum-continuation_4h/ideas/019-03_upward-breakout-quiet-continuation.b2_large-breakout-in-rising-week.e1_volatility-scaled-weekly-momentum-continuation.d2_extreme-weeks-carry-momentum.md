---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.e1_volatility-scaled-weekly-momentum-continuation_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The larger a coin's 7-day return, measured in units of its own 4h volatility, the more the coin rises over the next twelve days, the rise growing faster than the return itself so that the strongest weeks for their volatility carry most of it.
Consequence: A trader would put nearly all of the position into the rare weeks that are extreme for the coin's volatility, cutting the trades on ordinary weeks whose move does not cover the cost.
Why:
- F1: The book fails on size. Per case over 3 days, the total move is +0.18 % and the unusual move +0.17 % (strength 0.017 against a usual move of 8.17 %, 5544 cases), while a buy and a sell cost 0.19 %. That is 0.9 times the cost, so the mean daily return is 0.00045 against the 0.0005 required, and the Sharpe of 0.41 trails holding's by 0.14.
- F2: The move is carried almost entirely by the strongest weeks. On the 18-bar grid, cases with forecast size above 10 gain +0.67 % over 3 days, net of drift in the signal's direction (n 2513). Cases with size 2 to 5 lose -0.31 % (n 835). Cases with size 5 to 10 gain +0.05 % (n 1355). So most of the bets placed on mid-sized weeks pay the cost for nothing.
- F3: The move outlasts the 3-day horizon. Strong-week cases (forecast above 10) gain +0.67 % net of drift over 3 days, +0.73 % over 6 days and +1.67 % over 12 days. For the top positive bucket alone the excess rise is +0.72 %, +0.94 % and +2.30 %. Holding 3 days captures under half of the move and pays the cost on each re-entry.
- F7: Trading leaves little after cost. Gross gain per unit traded is 13 to 52 bps on five coins and -5 bps on XMR, against about 9.5 bps paid per unit traded. Turnover is 0.19 to 0.34 of the book per coin per day.
