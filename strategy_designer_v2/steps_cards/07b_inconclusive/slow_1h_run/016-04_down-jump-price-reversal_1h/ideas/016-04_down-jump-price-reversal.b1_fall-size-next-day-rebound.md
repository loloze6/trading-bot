---
brief: 016_grind-versus-jump-moves
source-idea: 016-04_down-jump-price-reversal
line: 7.b inconclusive
backtest: 016-04_down-jump-price-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the larger its 3-day fall, the more it rises over the next 1 day.
Consequence: A trader would lean long after the deepest 3-day falls for about a day, whatever shape the fall took, and would expect little or nothing after shallow ones.
Why:
- F2: The test's negative slope (t -1.92 on 2,762 fallen cases) comes from the size of the fall, not from its shape: tiny falls underperform and large falls rebound. In the top share quintile the excess 72-hour return is -1.05 %, and in the small-fall tercile it is -0.22 % to -1.18 % across share terciles, against +0.10 % to +0.87 % in the big-fall tercile.
- F3: Once fall size is controlled, the way the fall was built adds nothing. In a regression on fall size, the share of hourly losses carried by the top 3 has t -0.58 at 72 hours and t 1.57 at 24 hours, and the absolute top-3 loss has t 0.20 at 72 hours. Inside the big-fall tercile, the lowest loss-share tercile rebounds most (+1.46 % excess over 72 hours, against +0.04 % and +0.15 %).
- F5: The size of the 3-day fall carries a clear graded reversal that is strongest over the next day. On the fallen grid cases, excess return regressed on the 72-hour return has t -8.11 at 24 hours (slope -0.144, n 2,669). The same regression gives t -3.53 at 72 hours and t -2.54 at 168 hours. With the top-3 loss in the model, the 24-hour fall-size coefficient keeps t -7.12.
