---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue
line: 7.d not profitable
backtest: 026-01_weekend-rise-reverses-early-week.d2_weekend-reversal-in-turbulent-weeks.b2_calm-weekend-falls-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's price falls from Saturday 00:00 UTC to Monday 00:00 UTC by much against its 30-day hourly volatility, it rises over the next two days (Monday and Tuesday), and the larger the fall against that volatility, the larger the rise.
Consequence: A trader would buy Monday's open after a weekend fall that is large against the coin's usual swings, rather than short it.
Why:
- F6: Measured against the coin's 30-day volatility, the size of the weekend fall grades the move the wrong way: the smallest falls are followed by a further fall of 1.16 % (t 2.78, 260 cases), and the largest falls by a rise of 0.54 % (t -1.07, 261 cases), with the middle quartiles in between (-0.18 % and +0.63 %).
- F5: Across all weekend falls the continuation grows with how calm the coin's 30-day volatility is, step by step from the calmest to the most turbulent quartile of its rank: +0.78 % (t 1.51), +0.29 %, +0.10 %, then -0.79 % (t -1.64), with about 226 cases per quartile.
