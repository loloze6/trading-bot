---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins
line: 7.g patterns
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend.b1_quiet-breakdown-more-coins_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 4h
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is negative, a 4-hour close below the lowest low of the preceding 2 days is followed by a fall over the next 3 days. The narrower those 2 days' range was compared with the coin's 30-day average 4-hour range, the larger the fall.
Consequence: A trader should short quiet-range breakdowns in coins that fell over the past month, and refuse the same short when the preceding range was wide.
Why:
- F4: A downward break after a narrow 2-day stretch is followed by a fall, and the effect is strongest in a falling month, not the rising month the tested idea used. With the 30-day return negative, breaks in the narrowest quartile are followed by -1.61 % against drift (t -5.3, 795 cases, only 1 of 19 coins up). The rising-month version gives -0.50 % (t -1.4, 431 cases), which matches the inconclusive verdict.
- F5: In falling months, the move after a downward break is graded by how narrow the preceding stretch was. Over 3 days against drift it is -1.61 % (t -5.3) for the narrowest quartile, -0.64 % (t -1.9) for the second, +0.24 % (t 0.6) for the third and +0.78 % (t 2.3) for the widest. For the narrowest quartile, the effect appears in every era: -1.01 % (t -2.1), -1.56 % (t -3.3) and -1.10 % (t -3.1).
- F7: Narrow stretches are not followed by larger moves, against the brief's premise. The mean absolute 3-day move is 5.85 % after the narrowest fifth of 2-day stretches, against 6.75 % after the widest fifth. Upward breaks show no grading by narrowness: every quartile lies between -0.01 % and +0.20 %, with |t| < 1.
