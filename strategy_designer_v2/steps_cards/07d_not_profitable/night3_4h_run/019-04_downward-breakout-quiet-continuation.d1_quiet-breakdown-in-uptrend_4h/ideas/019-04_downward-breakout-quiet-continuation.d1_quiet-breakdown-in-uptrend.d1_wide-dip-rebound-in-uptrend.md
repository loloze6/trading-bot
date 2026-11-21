---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend
line: 7.d not profitable
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes below the lowest low of a coin's preceding two days while the coin's 30-day return is positive, the coin rises over the next three days, and the wider that two-day stretch was compared with the coin's 30-day average four-hour range, the larger the rise.
Consequence: Buy a two-day-low break in a coin that rose over the past month, more when the two days before it were wide, instead of shorting it.
Why:
- F3: Inside the idea's regime (positive 30-day return), the 3-day short move after a close below the 12-bar low depends on the stretch's width. It falls steadily from the narrowest fifth to the widest: +1.04 % (n 101, t 1.04), +0.21 %, +0.12 %, -1.36 % (n 218, t -2.90) and -2.61 % (n 239, t -4.19). Only the narrowest fifth gives a total move above the 0.19 % cost of a trade, about 5 times it.
- F4: In a rising month, a break below the two-day low after a wide stretch is followed by a rise that keeps growing for days. In the widest fifth of stretch width the coin rose 1.09 % over 1 day, 2.61 % over 3 days, 3.90 % over 6 days and 5.56 % over 12 days. The 3-day rise alone is about 14 times the cost of a trade.
- F5: Over all down breaks, the 3-day short total depends on the 30-day return at both ends. In the strongest-rising fifth (median +29 %) it was -1.05 % (n 444, t -2.34), and in the steepest-falling fifth (median -31 %) it was -1.47 % (t -3.32), so the coin rose afterwards in both. In the middle three fifths it was between -0.58 % and +0.25 %.
- F2: Because of that holding, the book stays short whatever the month does. 54 % of its held short bars had a negative 30-day return, which is outside the idea's own regime. The book earned only in falling years: 2018 at +0.038 %/day while the coin made -0.35 %/day, and 2022 at +0.008 %/day against -0.18 %/day. It lost in rising years, for example 2020 at -0.027 %/day while the coin made +0.42 %/day. This gives a Sharpe of -0.23 against holding's +0.55.
