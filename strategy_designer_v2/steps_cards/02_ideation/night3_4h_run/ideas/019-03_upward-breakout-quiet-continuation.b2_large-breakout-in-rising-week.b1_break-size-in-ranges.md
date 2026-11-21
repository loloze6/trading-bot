---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week
line: 7.b inconclusive
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes above the highest high of a coin's preceding two days, only while the coin's 7-day return is positive, the coin rises over the next three days. The rise grows with how far that close sits above the two-day high, counted in the coin's 30-day average four-hour range, and is largest for closes one or more average ranges beyond the high.
Consequence: A trader would buy upward breaks in proportion to how many average 4h ranges they clear in a rising week, and treat small breaks just above the high as no reason to trade.
Why:
- F1: The test came out inconclusive because of how the forecast was built, not because the effect was missing. The standardise transform pushed 89 % of the 2,416 cases to the cap of 20 (median forecast 20, 25th percentile 20). Cases strictly above that median therefore do not exist, so the supporting check returned None.
- F2: Measured on the idea's own size, the raw break above the two-day high in 30-day mean 4h ranges, the effect is graded in the direction the idea predicts. The top half of breaks beats the bottom half over 3 days by +1.05 % (+0.93 % against −0.12 %, Welch t 2.75, about 1,208 cases per half).
- F3: The effect sits in the largest breaks. Raw-break quintiles 1 to 3 (mean 0.08 to 0.41 ranges) show unusual 3-day moves of +0.20 %, −0.19 % and −0.33 % (t −0.9 to 0.6). Quintile 4 (0.75 ranges) shows +0.53 % (t 1.4), and quintile 5 (1.9 ranges) shows +1.80 % (t 3.38, 446 cases, strength 0.198).
- F4: The largest breaks move far more than a trade costs. In the top quintile the unusual 3-day move of +1.80 % is about 9 times the 0.19 % round trip, against 2.2 times for all cases.
- F6: The break-size gradient holds across most of the data, though its size varies:
