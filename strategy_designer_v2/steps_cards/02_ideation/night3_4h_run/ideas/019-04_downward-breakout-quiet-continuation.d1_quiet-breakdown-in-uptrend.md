---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation
line: 7.d not profitable
backtest: 019-04_downward-breakout-quiet-continuation_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes below the lowest low of a coin's preceding two-day narrow stretch, the coin falls over the next three days, and the narrower that stretch was compared with the coin's 30-day average four-hour range, the larger the fall, only while the coin's 30-day return is positive.
Consequence: Short a downward break out of a narrow range only in a coin that has risen over the past month, and refuse the short in a falling month, where the drift and the rebound eat it.
Why:
- F1: The book loses mainly because it is short a coin that drifts upward. It holds a short on 52 to 71 % of bars, and the coin's normal 18-bar drift is +0.24 % to +0.60 %. Per bar, the part of the book's result that comes from the market's own rise is -0.17 to -0.38 bps on every coin. Timing, being short when the coin falls more than usual, adds only -0.08 to +0.25 bps. Over 4790 short trades the mean is -1.21 % before fees and -1.31 % after.
- F2: After a 4h close below the prior two-day low, the drift-adjusted 18-bar return depends sharply on how wide the two-day stretch was:
- F3: That width gradient holds only while the coin's 30-day return is positive. There, the drift-adjusted 18-bar return after a down-break rises steadily from the narrowest to the widest fifth:
- F5: The idea's measured size is below the cost of a trade. The unusual move is +0.10 % per case, 0.5 times the 0.19 % cost, and the total move is -0.31 %. The down-break effect also changes sign by year: -1.91 % in 2018 (t -3.89, n 364), but +0.72 % in 2020, +1.23 % in 2021 and +0.69 % in 2025. So shorting down-breaks paid only in the bear year.
