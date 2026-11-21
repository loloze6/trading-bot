---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal
line: 7.d not profitable
backtest: 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The 2-hour return into the 00 UTC funding settlement runs opposite to the return over the 24 hours after it, and the larger the pre-settlement move relative to the coin's usual 2-hour move, the larger the move back. This holds only while that 2-hour move runs against the coin's 7-day return.
Consequence: A trader would fade a move into settlement only when it runs against the week's trend, betting on the trend's return, and would refuse to fade a move that follows the trend.
Why:
- F1: The idea's move per case is smaller than one trade's cost. Over 24 hours the move is +0.13 % in total (+0.14 % unusual) against a cost of 0.19 %. The book pays fees of 3.6 to 9.6 bps a day per coin but earns only 1.8 bps a day on average, -2.4 to +6.7 bps by coin. Every coin underperforms holding, which earns 6.7 to 15.5 bps a day. That is why the book's gain against holding and its mean daily return fail.
- F3: The size of the pre-settlement move grades the reversal. By quintile of |move| in usual 2-hour moves, the 24-hour excess is 1, 3, 4, 30 and 26 bps (t 3.6 and 2.9 in the top two quintiles), so the lower 60 % of cases carry under a quarter of the cost each.
- F6: The reversal is larger when the bet points with the coin's 7-day trend, that is, when the move into settlement ran against the week's direction. Those cases gain 24 bps (t 4.2, 7571 cases), against 3 bps (t 0.6, 8531 cases) when the bet goes against the 7-day trend.
