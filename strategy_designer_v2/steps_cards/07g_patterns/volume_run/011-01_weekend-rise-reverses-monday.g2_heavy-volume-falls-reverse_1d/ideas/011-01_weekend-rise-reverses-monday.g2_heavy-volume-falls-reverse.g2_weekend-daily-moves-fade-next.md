---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Saturday or Sunday move, measured in its usual daily moves, is partly undone over the next 1 day, and the larger that weekend day's move, the larger the reversal.
Consequence: A trader can fade each weekend day's move for the following day, in proportion to its size, rather than following it.
Why:
- F2: Saturday's volatility-scaled move is partly undone on Sunday, and the effect is graded. The next-day excess return falls by 0.38% per usual daily move (n 2,256, t -4.08), with t -3.06 in w1-12 and t -2.73 in w13-24. The sign is negative in all six coins, ranging from t -0.50 for XRP to t -3.26 for LTC.
- F3: Sunday's move also reverses on Monday (slope -0.45% per usual move, n 2,267, t -3.83). Wednesday and Thursday moves reverse about as much (t -4.05 and -4.08). Monday's own move instead continues into Tuesday (slope +0.26%, t +3.29). The two-day weekend move taken as a whole does not predict Monday (t -0.42).
