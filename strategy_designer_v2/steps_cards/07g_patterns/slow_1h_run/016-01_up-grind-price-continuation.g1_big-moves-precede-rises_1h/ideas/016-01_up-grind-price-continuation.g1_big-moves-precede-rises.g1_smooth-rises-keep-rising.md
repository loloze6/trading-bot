---
brief: 016_grind-versus-jump-moves
source-idea: 016-01_up-grind-price-continuation.g1_big-moves-precede-rises
line: 7.g patterns
backtest: 016-01_up-grind-price-continuation.g1_big-moves-precede-rises_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more of a coin's 3-day rise is made of hourly steps in the same direction (its net 3-day move over the sum of its absolute hourly moves), the more the coin rises over the next 3 days.
Consequence: After a 3-day rise, a trader leans long harder the smoother that rise was, and holds back after a choppy rise of the same size.
Why:
- F1: The coin rises more after its smoothest up moves: over all six coins and every window there were 5,539 non-overlapping 3-day cases. Among 3-day up moves, those in the top quintile of path efficiency (net 72-hour move divided by the sum of absolute hourly moves) were followed by a 72-hour excess return of +1.23% (t=3.26, n=638). The bottom quintile was followed by -0.45% (t=-1.21). The slope of the excess return on efficiency is 0.0565 (t=3.32, n=2,865) for up moves, against 0.0176 (t=1.00, n=2,674) for down moves.
- F2: Efficiency does not add to the move's size and volatility. When it shares a regression with the signed standardised 3-day move and the hourly volatility, efficiency's coefficient falls to -0.0022 (t=-0.04). The signed move keeps t=1.89 and volatility t=2.38. So the grind effect in F1 overlaps with plain 3-day momentum, which is positive in all six coins (slopes t 0.06 to 1.48).
- F3: The tested forecast's payoff is U-shaped in the signed 3-day move, not rising with its size. The excess 72-hour return is +0.29% (t=1.05) in the lowest quintile, -0.77% (t=-3.55) in the middle quintile and +0.67% (t=2.27) in the highest. This explains why the slope t of 3.67 came with negative timing in the book: timing part -0.0005 per day, Sharpe -0.38.
