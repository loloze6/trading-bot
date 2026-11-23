---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range
line: 7.g patterns
backtest: 029-02_breakout-volume-trapped-decline.d1_failed-breakout-from-flat-range_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day rise measured against its own 20-day daily volatility, the more the coin rises above its normal drift over the next 5 days.
Consequence: A trader would refuse shorts, failed-breakout shorts included, in the days after an unusually large up day, and would lean long in proportion to that day's size.
Why:
- F1: The pooled least-squares slope of the 5-day unusual move on the day's return in units of the coin's 20-day volatility is positive, at 0.00511 per unit, with t 2.66 on 2,699 non-overlapping cases; it is positive in all six coins (t from 0.10 for LTC to 2.37 for XRP), in both halves (w1-w12 t 2.57, w13-w24 t 1.40) and in 6 of 8 years.
- F2: After a large up day the coin keeps rising more than its drift. With z between 1 and 2 the 5-day unusual move is +1.71 % (strength 0.144, t 2.38, 255 cases), and with z above 2 it is +2.59 % (strength 0.224, t 2.06, 110 cases). After z below -2 it is only +0.46 % (t 0.45), so the response climbs with the size of the up day.
- F3: The up-day continuation (z above 1) is positive in every coin and in both halves: BTC +0.90 %, ETH +0.81 %, LTC +0.76 %, XMR +1.39 %, XRP +5.18 % (t 2.10), ZEC +2.82 %; w1-w12 +1.43 % (t 1.80), w13-w24 +2.49 % (t 2.58).
- F5: A close above the prior 20-day high is followed by a positive 5-day unusual move in all three terciles of breakout size (+1.63 %, +1.18 %, +2.05 %; strength 0.12 to 0.16) and in both halves (t 1.25 and 1.80). The size of the breakout does not grade the move, so there is continuation and no reversal.
