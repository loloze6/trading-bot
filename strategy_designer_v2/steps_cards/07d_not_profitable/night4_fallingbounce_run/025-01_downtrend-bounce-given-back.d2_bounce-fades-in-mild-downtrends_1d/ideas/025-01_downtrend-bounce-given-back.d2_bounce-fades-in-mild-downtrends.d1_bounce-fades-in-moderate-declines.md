---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends
line: 7.d not profitable
backtest: 025-01_downtrend-bounce-given-back.d2_bounce-fades-in-mild-downtrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a fall over the next 5 days, only while its 90-day fall is moderate rather than a crash. Within that range, the closer the 90-day fall is to its middle depth, the larger the fall that follows.
Consequence: A trader would fade bounces only in coins in a moderate decline and stop shorting bounces in coins that have crashed, where the short pays the rebound and the drift.
Why:
- F1: The book's loss is the coins' own rise working against its shorts, not bad timing: its mean daily return is -0.000237, of which -0.000244 comes from the market's own rise. That leaves about +0.000007 a day of timing, while the book is short on 41.5 % of days at a mean allocation of -0.49.
- F2: On the bounce cases (982 in my reconstruction), the short's unusual 5-day move is only +0.32 % (t 1.07), while the coins' normal 5-day drift is +0.30 % to +0.91 % upward. The total move a short earns is therefore -0.28 % per case, below zero before the 0.19 % cost of a trade.
- F3: The fade depends on how deep the 90-day fall is, and not in a straight line. In the deepest fifth of falls (mean 90-day return -51 %), bounces keep rising: unusual move -1.38 % (t -1.64), total -1.97 % against the short. In the middle fifth (mean -22 %), the fade is +1.84 % unusual (t 3.11) and +1.24 % total, the only group whose total move clears the cost. The shallowest fifth (mean -4 %) shows +0.91 % (t 1.54).
