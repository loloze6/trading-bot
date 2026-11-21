---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend
line: 7.d not profitable
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes below the lowest low of a coin's preceding two days, the coin rises over the next three days, and the deeper the coin's fall over the past 30 days, the larger the rise.
Consequence: Buy new two-day lows in a coin that has already fallen hard over the past month rather than shorting them.
Why:
- F5: Over all down breaks, the 3-day short total depends on the 30-day return at both ends. In the strongest-rising fifth (median +29 %) it was -1.05 % (n 444, t -2.34), and in the steepest-falling fifth (median -31 %) it was -1.47 % (t -3.32), so the coin rose afterwards in both. In the middle three fifths it was between -0.58 % and +0.25 %.
- F2: Because of that holding, the book stays short whatever the month does. 54 % of its held short bars had a negative 30-day return, which is outside the idea's own regime. The book earned only in falling years: 2018 at +0.038 %/day while the coin made -0.35 %/day, and 2022 at +0.008 %/day against -0.18 %/day. It lost in rising years, for example 2020 at -0.027 %/day while the coin made +0.42 %/day. This gives a Sharpe of -0.23 against holding's +0.55.
