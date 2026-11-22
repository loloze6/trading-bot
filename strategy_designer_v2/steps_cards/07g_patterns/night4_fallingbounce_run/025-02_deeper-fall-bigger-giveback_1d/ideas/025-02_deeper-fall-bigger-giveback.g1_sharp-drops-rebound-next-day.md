---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-02_deeper-fall-bigger-giveback
line: 7.g patterns
backtest: 025-02_deeper-fall-bigger-giveback_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall, measured in its usual daily moves over the past 20 days, the larger its rise over the next day.
Consequence: A trader can buy into a coin's sharp daily drops for a one-day rebound, sized up the sharper the drop, and should refuse to short on the day after one.
Why:
- F1: A sharp one-day fall is followed by a graded rebound the next day. On days with a fall (z<0, where z is the day's return over the 20-day standard deviation), the regression of the next day's standardised unusual return on z has slope -0.078 with t -4.4 over 7529 days. The slope is negative in all six coins (XMR t -3.9, XRP t -2.3, ZEC t -2.0, ETH t -1.6, BTC t -0.6, LTC t -0.4) and in 7 of 8 years, with 2020 and 2021 strongest (t -4.5 and -3.9). The next-day unusual move is +0.53 % (t 3.9, 1511 days) after falls of 1 to 2 usual moves and +0.72 % (t 2.3, 425 days) after falls beyond 2 usual moves. Both are well above the 0.19 % a trade costs.
- F2: The rebound after falls weakens but is still there over 2 days. On the non-overlapping 2-day grid, the pooled slope on z (z<0) is -0.059 with t -2.4 over 3673 cases, and every coin's slope is negative.
