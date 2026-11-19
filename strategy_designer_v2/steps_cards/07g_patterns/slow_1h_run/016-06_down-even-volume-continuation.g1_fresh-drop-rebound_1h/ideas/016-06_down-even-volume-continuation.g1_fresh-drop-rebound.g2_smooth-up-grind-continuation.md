---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound
line: 7.g patterns
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more evenly a coin's 3-day rise was built, measured as its 3-day return over the sum of its absolute hourly returns, the more it keeps rising over the next 3 days.
Consequence: A smooth hourly grind upward is a reason to hold or join a rise, and a choppy rise of the same size is a reason not to.
Why:
- F5: Rises built as a smooth grind keep going: in the top quintile of path efficiency (|72h return| / sum of |hourly returns|), up moves continue by +0.0129 excess over the next 72h (t 3.44, n 653) while the other quintiles lie between -0.0036 and +0.0021, and efficiency stays significant when 3-day size and volume concentration are added (t 3.06; |r72| t -2.58).
- F6: The grind effect is not stable and has the wrong shape over one day: top-efficiency continuation is t 0.82 in w1-12 against t 3.26 in w13-24, the down-move top-efficiency quintile shows none (+0.0025, t 0.60), and the 24h continuation in the top quintile is slightly negative (t -1.17).
- F7: Volume bunched into one hour of the 3-day move goes with less continuation: the top volume-concentration quintile's continuation is -0.0036 (t -1.63), and t is -2.52 once efficiency and size are controlled.
