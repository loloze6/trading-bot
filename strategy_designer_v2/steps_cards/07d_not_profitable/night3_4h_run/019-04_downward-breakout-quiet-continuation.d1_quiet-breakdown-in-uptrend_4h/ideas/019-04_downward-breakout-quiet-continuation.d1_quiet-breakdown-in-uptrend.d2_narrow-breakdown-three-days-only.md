---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend
line: 7.d not profitable
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes below the lowest low of a coin's preceding two-day narrow stretch, the coin falls over the next three days, and the narrower that stretch was compared with the coin's 30-day average four-hour range, the larger the fall, only while the coin's 30-day return is positive and only over the three days after that bar's close.
Consequence: Short only the narrowest breakdowns in a rising month and close the short within three days, never carrying it into a month that has turned down.
Why:
- F1: The book's loss comes from holding shorts long after the signal ends. There were 1254 short trades with a mean gross of -3.29 % and a net of -3.39 %, and 28 % of them won. They lasted 295 hours on average against a 72-hour horizon, and 97 % of the bars held short had a forecast of 0. The 302 trades held more than 12 days lost about -9.8 % to -10.0 % gross each, against -0.60 % for the trades held 2 to 3.5 days.
- F2: Because of that holding, the book stays short whatever the month does. 54 % of its held short bars had a negative 30-day return, which is outside the idea's own regime. The book earned only in falling years: 2018 at +0.038 %/day while the coin made -0.35 %/day, and 2022 at +0.008 %/day against -0.18 %/day. It lost in rising years, for example 2020 at -0.027 %/day while the coin made +0.42 %/day. This gives a Sharpe of -0.23 against holding's +0.55.
- F3: Inside the idea's regime (positive 30-day return), the 3-day short move after a close below the 12-bar low depends on the stretch's width. It falls steadily from the narrowest fifth to the widest: +1.04 % (n 101, t 1.04), +0.21 %, +0.12 %, -1.36 % (n 218, t -2.90) and -2.61 % (n 239, t -4.19). Only the narrowest fifth gives a total move above the 0.19 % cost of a trade, about 5 times it.
- F6: The short effect is not stable over time. By year, in the idea's regime, it was +5.5 % in 2018 (t 4.70) and -3.9 % in 2021 (t -4.21), and it was negative in 6 of 8 years. Overall its total move per case is +0.14 %, 0.7 times the 0.19 % cost of a trade, so as tested the idea cannot pay.
