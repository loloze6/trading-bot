---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 3 days, only while its 1-day hourly volatility is high against its 30-day hourly volatility, and the higher that ratio, the larger the rise.
Consequence: Take the rebound only after violent, volatile drops; quiet grinding drops should not be bought.
Why:
- F1: Of the book's mean daily return of 0.000115, the market's own rise accounts for 0.000397 (mean position 0.34), so the timing part is -0.000281: being long after 1-day falls has cost money against simply holding, which is why the Sharpe trails holding's by 0.41 and the mean daily return stays below 0.0005.
- F3: The coin's 24-hour volatility against its 30-day volatility splits the long bars the same way. In the calmest quarter the next-3-day excess return is -0.0112 (t -2.59, n 344); in the most volatile quarter it is +0.0114 (t 2.40, n 344). Even among the larger forecasts, those with low relative volatility lose -0.0107 (t -2.74, n 277), while those with high relative volatility gain +0.0112 (t 2.93, n 411).
- F5: Most long positions sit on shallow 3-day falls, and these lose. The shallowest quarter of 3-day falls returns -0.0115 over the next 3 days (t -3.60, n 456), while the deepest quarter gains +0.0100 (t 2.05, n 457).
