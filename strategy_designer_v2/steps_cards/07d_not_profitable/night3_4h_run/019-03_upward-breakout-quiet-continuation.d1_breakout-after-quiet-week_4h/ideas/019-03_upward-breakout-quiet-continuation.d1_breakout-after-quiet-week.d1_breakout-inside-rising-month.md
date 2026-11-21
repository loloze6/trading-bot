---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes above the highest high of a coin's preceding two-day narrow stretch, the coin rises over the next three days, larger the narrower that stretch was compared with the coin's 30-day average four-hour range, only while the coin's own 30-day return is positive.
Consequence: A trader should take upward breakouts only in a coin that has risen over the past month, and refuse them in a falling month, where the book's 48 % fall was held.
Why:
- F1: Calmar fails because of one long fall: the book's deepest fall is 48 % (yearly return 34 %, Calmar 0.70). It runs 555 days, from w5 to w10, while the coins' average fell 59 %, and windows w5, w7, w9 and w12 lost 7 to 25 % with in-window falls of 21 to 33 %.
- F2: The book's gain comes from bars where the coin's 30-day return is positive. In position there, the mean gain is 6.7 bps per 4h bar outside w5–w10 (t 4.95, 18931 bars) and 5.4 bps inside them (t 2.24, 6397 bars). Where the 30-day return is negative, it earns 1.2 bps outside the fall (t 0.94, 13375 bars) and loses 2.9 bps inside it (t -1.29, 3973 bars).
- F3: The book spends 31 % of its in-position bars with a negative 30-day return. Gross of costs, staying flat there would have raised Calmar from 1.15 to 1.66, cut the deepest fall from 39 % to 29 %, raised the yearly return from 44 % to 48 % and raised the Sharpe from 1.06 to 1.30. Using the 60-day return instead gives a Calmar of only 1.27.
- F4: The same split shows on the 14-day return. In-position gain is -3.1 bps per bar in its lowest quintile (median -14 %, t -2.09, 9999 bars) and -1.1 bps in the next (t -0.82). It is 7.0, 7.2 and 5.8 bps in the upper three quintiles (t 4.5, 4.2, 2.6).
- F7: The idea's own move is smaller than a trade's cost. Per case, the unusual move is +0.18 % over 3 days (strength 0.020, t 1.13, 3102 cases), 0.9 times the 0.19 % round-trip cost. The total move is +0.58 %, 3.0 times the cost, so the book earns mostly from the coin's drift, which it takes while the coin is rising.
