---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin rises over Saturday (UTC), and the rise is larger the larger the coin's rise over the preceding 5 days in units of its 20-day volatility.
Consequence: A trader could hold the coin long from Friday's close to Saturday's close, with more size after a strong week.
Why:
- F6: Saturday is the strongest calendar day. Holding the coin, Saturday's daily return is +0.45% (t=5.53, n=2484), and the bar after Friday's close earns +0.30% above the coin's mean (t=3.76, n=2479). That bar is positive in 6 of 8 years and for all 6 coins, but the book is flat on it.
- F7: Strong 5-day rises tend to continue, but the effect is not stable. The top quintile of the volatility-scaled 5-day return is followed by +0.63% excess over 2 days (t=3.34, n=1442). The fourth quintile is negative (−0.29%), and the top quintile is negative in 2019 and 2023, so the pattern is weak given how many angles I looked at.
