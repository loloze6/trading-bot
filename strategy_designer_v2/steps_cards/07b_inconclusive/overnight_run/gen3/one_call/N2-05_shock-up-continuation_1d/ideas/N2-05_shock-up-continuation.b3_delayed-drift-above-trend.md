---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-05_shock-up-continuation
line: 7.b inconclusive
backtest: N2-05_shock-up-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After an outsized up day in a coin trading above its 50-day average, the coin rises from the next day's close to five days after the shock, more than its usual daily drift.
Consequence: A trader would enter the day after the shock, not on the shock close, and only in coins above their 50-day average.
Why:
- F5: Measured from the bar after the event (bars t+1 to t+5), top-tercile prior-20-day events gain +2.68% (t 2.61, n 163, hit 58.9%). The next-bar excess over all events is −0.20% (t −0.88), so any continuation starts after the first day.
- F6: Big up days that close above the prior 20-day closing high gain +1.82% over 5 bars (t 2.01, n 245), against −0.02% (t −0.04, n 242) for those that do not. Similarly, events above the 50-bar average gain +1.27% (t 1.91, n 299), against +0.03% (t 0.04, n 157) below it.
- F2: Much of the drift is the market's own move: the other five coins rise +1.05% over the same 5 bars (t 2.92, n 601), and the coin's 5-bar return correlates 0.59 with theirs. Measured relative to that basket, the excess is +0.42% (t 0.99).
