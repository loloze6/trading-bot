---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-05_hourly-plunge-loss-before-close
line: 7.g patterns
backtest: 018-05_hourly-plunge-loss-before-close_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, falls to a large multiple of its 30-day average absolute 24-hour return, the price rises over the next 24 hours, and the larger the drop in those multiples, the larger the rise.
Consequence: An outsized 24-hour plunge is a reason to buy the coin for a day rather than to short it, with more conviction the deeper the plunge.
Why:
- F1: A large 24-hour drop is followed by a rebound over the next 24 hours, not by a further fall. The rebound grows with the drop's size in multiples of the coin's 30-day mean absolute 24-hour return (z):
- F2: The rebound after drops with z ≤ -2.5 is positive on all 6 coins, but it is uneven across time:
- F3: The book lost because it sat short on the wrong side of the rebound in F1.
- F4: Over the next 24 hours, the highest-volatility fifth of bars is the only quintile with a positive excess move: +33 bps, 3100 cases, t 2.9. The other four quintiles run from -6 to -13 bps. This is consistent with the rebound in F1 being concentrated after violent falls.
