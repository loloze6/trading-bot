---
brief: 022_weak-effects-combined-by-what-worked-before
source-idea: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility
line: 7.g patterns
backtest: 022-02_combination-beats-best-single.d3_momentum-fades-in-high-volatility_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 14-day return, measured in units of its 30-day daily volatility, the higher its return over the next 10 days.
Consequence: Momentum bets on the last two weeks' move should be held for about ten days rather than three to four weeks, because the move they capture has faded by then.
Why:
- F1: A coin's 14-day return, in units of its 30-day volatility, predicts its excess return over the next 10 days, and the effect grows with the move. On the non-overlapping 10-day grid with all 6 coins pooled, the standardised product has mean 0.078 (t 2.60, 1,403 cases, 5 of 6 coins positive). The largest-move third of cases has an unusual move of 268 bps (t 3.40, 468 cases) and a strength of 0.16, which is 3 times the usual 0.05 (F10). Its total move of 294 bps is about 15 times this backtest's 19 bps round trip.
- F2: That 10-day momentum is not steady over time. The unusual move is 215 bps (t 3.37, 707 cases) in windows w13 to w24 but -47 bps (t -0.91, 696 cases) in w1 to w12. The 7-day return behaves the same way at 10 days: 143 bps (t 2.23) late against 25 bps (t 0.49) early.
- F3: Momentum that pays at 5 to 10 days is gone by 20 days, the tested horizon. The 28-day volatility-scaled return gives t 2.20 at 5 days and at 10 days, but t 0.72 at 20 days (539 cases). The tested idea's own size at 20 days is -0.44 % per case, which is -2.3 times the cost of a trade.
