---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the smaller that fall is next to the coin's 3-day volatility, the more the coin keeps falling over the next 3 days.
Consequence: Gentle declines are the ones to short, while large volatility-scaled falls carry no continuation and should be refused.
Why:
- F3: Among fallen coins, only the shallow falls continue; deep falls do not. On the non-overlapping 72-bar grid, the shallowest raw-fall quintile had a 72-bar excess return of -0.0115 (t -3.81, n 534) and the deepest +0.0060 (t 1.30, n 534). By volatility-scaled fall, the shallowest quintile was -0.0091 (t -2.51) and the deepest +0.0002 (t 0.04).
- F2: The fees come from the shallowest falls, where the 3-day return hovers near zero and the regime keeps switching on and off. On active bars in the shallowest quintile of the volatility-scaled fall, turnover was 0.033 and fees were 3.6e-5 per bar. In the deepest quintile they were 0.0014 and 1.0e-6.
