---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d1_settlement-fall-recovers-over-day_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly volatility over the past 30 days is high against its own past 90 days, its return over the next 24 hours runs opposite to its 24-hour return. The larger the 24-hour move against its usual 24-hour move, and the higher that relative volatility, the larger the reversal.
Consequence: After a large 24-hour fall in a coin that is unusually volatile for itself, a trader has a reason to be long for the next day, and a reason to refuse a long after a large 24-hour rise in that state.
Why:
- F1: A coin's 24-hour fall reverses over the next 24 hours only when its volatility is high. In the top tercile of each coin's 30-day hourly volatility, the 24h-return quintiles (24h return scaled by its usual 24h move) give an excess return over the next 24h of +1.25 % (t 5.12, 1012 cases) for the largest falls and −0.69 % (t −3.14, 991 cases) for the largest rises. In the low-volatility tercile the same quintiles give +0.02 % (t 0.14) and +0.17 % (t 1.49).
- F2: The reversal grows with volatility measured against the coin's own past. Sorting the 24h grid cases by 30-day volatility over its 90-day median, the slope of the next-24h excess return on the scaled 24h return is +0.3 bp (t 0.06), −14.0 bp (t −2.80) and −33.2 bp (t −6.65) from the low to the high tercile (about 4309 cases each).
- F3: In high volatility the reversal is graded. Across the fall quintiles, the next-24h excess return climbs from −0.38 % (t −1.45) for the mildest falls to +1.64 % (t 4.16, 424 cases) for the largest. +1.64 % is 8.6 times the 0.19 % cost of a trade, against the tested idea's total move of +0.23 % per case.
- F4: The high-volatility 24h reversal holds coin by coin and year by year, with differing strength:
