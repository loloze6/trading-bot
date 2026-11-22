---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation
line: 7.d not profitable
backtest: 023-03_flatter-range-stronger-reversion.d1_flat-range-breakout-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The farther a coin's close sits above the middle of its 30-day closing range, the larger its rise over the next 5 days, the flatter the 30 days were the larger that rise, only while the coin's 30-day return is positive.
Consequence: A trader buys the upper edge of a flat month only when that month still closed higher than it opened, and refuses the same signal after a net-down month.
Why:
- F5: The long cases carry the effect mainly when the coin's 30-day return is up: unusual move +0.95 % per case, t 2.7, n 1010. When it is down the figure is +0.18 %, t 0.35, n 636.
- F1: The book's gain comes from its long side only: long bars earned a mean +0.116 % per bar (sum +9.41 over 8106 bars), while short bars, more than half the book's time, lost a mean −0.037 % per bar (sum −3.38 over 9246 bars). The book is also flat on 172 bars.
- F2: On the 5-day grid, the short cases have a positive unusual move (+0.57 % per case when the 30-day trend was down, n 1459, t 2.1; +0.78 % when it was up, n 313). The coin's upward drift cancels it, so their total move is nil: −0.02 % and +0.19 %. That is no more than the 0.19 % cost of a trade. The long cases' total move is +0.76 % (n 636) and +1.54 % (n 1010).
