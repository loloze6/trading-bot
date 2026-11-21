---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend
line: 7.b inconclusive
backtest: 019-04_downward-breakout-quiet-continuation.d1_quiet-breakdown-in-uptrend_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes below the lowest low of a coin's preceding two-day stretch while the coin's 30-day return is positive, the coin rises over the next three days. The wider that stretch was compared with the coin's 30-day average four-hour range, the larger the rise.
Consequence: In a coin that has risen over the past month, buy a break below a wide two-day range rather than short it, and refuse the short most firmly when the broken range was wide.
Why:
- F3: The short does not pay its cost and turns against itself with time. The total short move is +0.14 % per case against a 0.19 % round trip (0.7 times the cost). The short's total move is +0.15 % at 1 day, -0.14 % at 6 days (651 cases) and -0.74 % at 10 days (621 cases). Over these 6 coins' windows the normal 18-bar drift is +0.24 % to +0.60 %.
- F4: The clear effect is on the other side and graded by the stretch's width. Take every downward break (close below the prior 12-bar low) in a rising 30-day month, one per 18-bar cell, 932 cases. When the prior two-day stretch was wide, the coin rises over the next three days:
- F5: This width-rebound gradient is broad and large next to cost. The Spearman correlation between stretch width and the long unusual 3-day move is +0.13 overall and positive in all 6 coins (+0.04 to +0.25). It is positive or zero in 7 of 8 years, the exception being 2021 at -0.02. In the widest quartile the total rise grows from +1.11 % at 1 day (t 2.64) to +4.02 % at 6 days (t 4.38, 223 cases). Over 3 days the total rise is about 14 times the 0.19 % cost, and the unusual move about 11 times.
