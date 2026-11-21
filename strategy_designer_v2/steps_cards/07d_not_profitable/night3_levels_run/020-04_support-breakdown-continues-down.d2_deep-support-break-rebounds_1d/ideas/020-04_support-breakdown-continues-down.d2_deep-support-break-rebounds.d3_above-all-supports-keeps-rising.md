---
brief: 020_support-and-resistance-at-past-turning-prices
source-idea: 020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds
line: 7.d not profitable
backtest: 020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above every price where it turned up in the past 90 days, it tends to rise over the next 5 days, and the nearer its close is to its 60-day high, the larger the rise.
Consequence: Holding a coin that has broken none of its recent supports and sits near its highs captures the drift that the support-break book leaves on the table.
Why:
- F1: The book loses where it spends most of its time: it is long on 74 % of bars, and on the 2366 grid cases where the close sits under a past swing low at all, the following 5-day unusual move is -0.32 % (t -1.51; total +0.27 %, barely above the 0.19 % cost). On the 1053 cases with no support broken it is +0.71 % (t 1.83; total +1.30 %). Yet the book holds a mean allocation of 0.48 in the first state and 0.05 in the second, so it is long when the coin does worse than usual and flat when it does better. This is why it trails holding: 0.038 % against 0.119 % per day, and a Sharpe 0.15 below holding's.
- F8: When the coin is above every recent swing low, the next 5 days rise more the nearer it is to its 60-day high. Across drawdown terciles the unusual move is +0.20 % (deepest drawdown), +0.82 % and +0.95 % (nearest the high; t 1.45, 324 cases).
- F7: The book's falls are deep against its gain. Its deepest fall is 47 % in w14, where the coins averaged -0.43 % a day, and 5 other windows fall more than 35 %. This gives a Calmar of 0.17, with the book long through broken-support declines.
