---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation
line: 7.d not profitable
backtest: 018-04_hourly-surge-multiday-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside, the price keeps rising over the next 5 days by more than the coin's usual 5-day return, only while the close stands near its 30-day high: the closer the close to its 30-day high at that hour, the larger the rise.
Consequence: A trader would take the surge only when it happens at or near the month's high, and refuse surges that are rebounds inside a month-long decline, which are most of the book's exposure during the coins' shared falls.
Why:
- F1: The book fails on its falls, not on its gain: chained over the windows its deepest fall is 61.5 % against a yearly return of 33.1 % (Calmar 0.54 against 0.75 required), even though its Sharpe of 0.79 beats holding's by 0.24.
- F2: The book is in effect a scaled holding of the coins. It holds a position on 98.3 % of coin-days, at a mean allocation of 0.81 when in. Its losing windows match the coins' losing windows: in w2 the book's daily returns sum to -0.39 against the coins' -0.46, in w7 -0.33 against -0.58, and in w14 -0.49 against -0.52. Its chained fall reaches -0.54 in w2, -0.61 in w3 and -0.59 in w4, which is one long fall shared with the coins.
- F3: The idea has no edge of its own to offset those falls. Over the 3205 cases the unusual 120-bar move is -0.01 % (t -0.06). The total move is +0.63 %, 3.3 times the 0.19 % round trip, but it is all the coin's normal drift. The unusual move is -0.1 times the cost.
- F5: Nearness to the 30-day high is the situation that separates the surges, though the grading is not smooth across its quintiles:
- F7: On the book's own days, nearness to the 30-day high at the previous day's close comes with more gain but not with fewer large losses:
