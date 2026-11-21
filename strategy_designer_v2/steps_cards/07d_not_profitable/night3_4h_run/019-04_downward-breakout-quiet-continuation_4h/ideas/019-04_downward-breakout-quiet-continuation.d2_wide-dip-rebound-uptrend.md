---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation
line: 7.d not profitable
backtest: 019-04_downward-breakout-quiet-continuation_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes below the lowest low of a coin's preceding two days while its 30-day return is positive, the coin rises over the next three days, and the wider those two days' range was compared with the coin's 30-day average four-hour range, the larger the rise.
Consequence: A sharp, wide-range drop in a coin that is in a monthly uptrend is a dip to buy for three days, not a breakdown to short.
Why:
- F2: After a 4h close below the prior two-day low, the drift-adjusted 18-bar return depends sharply on how wide the two-day stretch was:
- F3: That width gradient holds only while the coin's 30-day return is positive. There, the drift-adjusted 18-bar return after a down-break rises steadily from the narrowest to the widest fifth:
- F6: Down-breaks that come after the steepest 30-day falls also rebound: the lowest fifth of 30-day return gives +1.05 % drift-adjusted over 18 bars (t 2.37, n 444).
