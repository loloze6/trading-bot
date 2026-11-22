---
brief: 023_range-reversion-when-no-trend
source-idea: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days
line: 7.g patterns
backtest: 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 30-day net move has been small relative to its 30-day high-low range, the closer its close sits to the bottom of that range, the further it falls over the next 5 days.
Consequence: A trader would not buy a flat coin near the bottom of its month's range expecting a bounce, and would rather lean short the lower it sits.
Why:
- F1: Among flat coins (30-day net move under half the 30-day high-low range), those closing in the bottom fifth of the range (position ≤ -0.3) moved further down over the next 5 days rather than reverting. The mean was -0.22 of a usual 5-day move (t -3.14, 155 non-overlapping cases), and the bottom flat quintile of the 30-day return was also negative (-0.115, t -2.71, 399 cases).
- F2: In flat coins, range position correlated positively with the next 5-day unusual move (r 0.058, t 2.20, 1442 cases), and so did the 30-day return (r 0.047, t 1.78). This is the opposite sign to the brief's reversion. Only the bottom of the range carries it: the top fifth averaged -0.058, t -0.71, 134 cases.
