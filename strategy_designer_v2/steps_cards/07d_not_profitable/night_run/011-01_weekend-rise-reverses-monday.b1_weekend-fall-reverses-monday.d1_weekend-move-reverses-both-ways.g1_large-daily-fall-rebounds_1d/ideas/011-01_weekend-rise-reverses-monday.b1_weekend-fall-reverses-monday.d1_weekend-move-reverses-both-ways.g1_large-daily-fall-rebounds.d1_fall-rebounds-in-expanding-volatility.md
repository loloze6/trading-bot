---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g1_large-daily-fall-rebounds
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g1_large-daily-fall-rebounds_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin's own daily fall that is large against its 20-day volatility, the coin rises over the next 1 day, and the larger the fall in units of its usual daily move, the larger the rebound, only while the coin's 20-day volatility is high against its 60-day volatility, the rebound being larger the higher that ratio.
Consequence: A trader would buy sharp volatility-scaled falls only when volatility is expanding. The trader would refuse them in calm, contracting-volatility stretches, where the falls carry on and the fees are wasted.
Why:
- F1: Whether the rebound shows up depends on the volatility regime. When a coin's 20-day volatility is low against its 60-day volatility, the held bars lose: the lowest quintile of that ratio (0.17–0.71) has a mean next-day excess return of -0.0068 (t -4.11, n 685) and the next quintile -0.0030 (t -1.56). The upper three quintiles (ratio above 0.86) earn +0.0048 (t 2.77), +0.0027 and +0.0055 (t 2.63).
- F2: The losses in the low-volatility-ratio regime do not depend on how large the fall was. In its tercile, mean excess return is -0.0038, -0.0054 and -0.0086 from the largest to the smallest falls. In the high-ratio tercile the largest falls rebound +0.0136, so the graded rebound only exists while volatility is expanding.
- F3: Split by volatility-ratio tercile, the held bars sum to -1.67 gross gain against 0.40 in fees in the low tercile, +1.51 in the middle and +3.77 in the high. Fees are spread evenly across terciles (0.39–0.40), so the calm-regime trades cost as much to run as the profitable ones.
- F4: The book does not keep up with holding, and its daily return and Calmar fall short. Its mean daily return is 0.000289 (Sharpe 0.48) against holding's 0.00118 (Sharpe 0.55), and its deepest fall is -32.8%. Fees take 3.73 of 8.82 summed gross gain (42%), and the market's own rise adds only 0.000141 per bar against 0.000366 of timing.
