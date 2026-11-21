---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge
line: 7.b inconclusive
backtest: 018-05_hourly-plunge-loss-before-close.d2_ten-day-rebound-after-plunge_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, falls, the coin rises over the next 10 days more than its normal drift, and the shallower the fall measured in its 30-day average absolute daily return and the larger its 30-day return before the fall, the larger the rise.
Consequence: A trader who buys a shallow dip in a coin that has risen strongly over the past month, and holds about ten days, captures a move several times a round trip's cost, while a deep plunge is a reason to refuse that buy.
Why:
- F2: The grading the idea names fails because it runs the wrong way on the drop. Across cases, the slope of the 10-day move (in usual moves) on the depth of the 24-hour fall is −0.117 (t −2.32, n 1,009): the deepest quarter of drops is followed by −0.70 % (t −0.70, n 251), while the shallower three quarters give +0.94 % to +1.91 %. The slope on the forecast is −0.004 (t −0.84, n 1,093).
- F3: The 30-day prior rise is the part that is graded the predicted way. Across cases its slope is +0.22 (t 2.01, n 815), and +0.27 (t 2.35, n 678) among cases whose fall is under one usual daily move. Among drops deeper than one usual daily move it is −0.17 (t −0.55, n 137).
- F6: Size is not the obstacle. The unusual move is +1.08 % per case, 5.6 times the 0.19 % cost of a round trip, and the total move is 12.6 times that cost. What leaves the result unclear is the mis-signed drop grading (F2), not too few cases or too small a move.
