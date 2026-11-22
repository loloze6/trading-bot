---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-01_volume-surge-up-continuation
line: 7.d not profitable
backtest: 028-01_volume-surge-up-continuation_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: After an hour in which the coin rises far more than its typical hourly move over the past 30 days, on volume several times its average hourly volume over the past 30 days, the price keeps rising over the next two to six hours, only while the coin's 24-hour return before that hour is modest; the larger the coin's rise over the previous 24 hours, the weaker the further rise, turning into a fall after the largest prior rises.
Consequence: A trader would take a high-volume up-hour as a reason to buy only when it starts a move, and refuse it when it caps a day that has already risen strongly.
Why:
- F5: Among the top 5 % of up-scores, the hours that follow the highest quartile of the prior 24-hour return are followed by an excess 6-hour return of −0.417 % (t −2.67, n 268). Those in the second quartile are followed by +0.231 % (t 2.35, n 267). On all up-hours the prior 24-hour return's slope is negative (t −1.47).
- F1: The idea has no edge to pay for its trades: per case over 6 hours the unusual move is +0.00 % and the total move +0.04 %, against a cost of 0.11 % per trade (8827 cases); on hours sampled once per 6-hour cell, the top 1 % of up-scores is followed by an excess 6-hour return of −0.143 % (t −0.64, n 214) and the next 4 % by +0.056 % (t 0.70, n 856).
- F3: The book is mostly a costly part-time holding of the coin: it is long on 70 % of BTC bars and 67 % of ETH bars (mean allocation 0.37 and 0.30); it gains 0.29 and 0.40 bp per bar before fees, of which the market's own rise is 0.20 and 0.19 bp; it makes 2.88 trades a day and ends at a mean daily return of −0.016 %, with a Sharpe 0.77 below holding.
