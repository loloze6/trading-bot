---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g1_large-daily-fall-rebounds
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways.g1_large-daily-fall-rebounds_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin's daily fall, the coin rises over the next 2 days, and the rise is larger the larger the fall in units of its 20-day volatility multiplied by that day's volume relative to its 20-day average volume.
Consequence: A trader would treat a heavy-volume capitulation day as a buying opportunity, and would not treat a quiet drift lower the same way.
Why:
- F2: Large falls on heavy volume rebound and large falls on light volume do not, which is the opposite of the brief's low-volume reasoning. Among the two lowest z-deciles, the next-day excess return is +0.0065 (t 4.52, n 1597) when the day's volume is in the top tercile against its 20-day mean, and +0.0005 (t 0.22, n 493) in the bottom tercile. Ranking falls by fall size × volume ratio puts the whole effect in the top quintile: +0.0062 (t 3.44, n 948), with the other quintiles between -0.0001 and +0.0011.
- F3: The heavy-volume rebound lasts two days. Over non-overlapping 2-day samples, falls on top-tercile volume are followed by +0.0061 (t 2.20, n 788), against -0.0032 (t -1.40, n 740) on bottom-tercile volume.
- F4: The two conditions add up. Top-quartile falls with high volume in a high-volatility regime return +0.0159 the next day (t 3.33, n 229). The same high-volume falls in a low-volatility regime return -0.0029 (t -1.02, n 281).
