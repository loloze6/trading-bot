---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin's down day, the higher that day's volume relative to its median daily volume over the past 20 days, the larger the coin's rise over the next 1 day.
Consequence: A fall on heavy volume is a reason to lean long the next day, more so the heavier the volume, rather than to treat it as the start of a further decline.
Why:
- F4: After a down day, the higher that day's volume relative to its 20-day median, the larger the next day's return (slope 0.0046 per unit of log relative volume, t = +5.4, n = 7906). After an up day the slope is t = +0.95 (n = 8162). Over all days the slope is positive in 7 of 8 years.
