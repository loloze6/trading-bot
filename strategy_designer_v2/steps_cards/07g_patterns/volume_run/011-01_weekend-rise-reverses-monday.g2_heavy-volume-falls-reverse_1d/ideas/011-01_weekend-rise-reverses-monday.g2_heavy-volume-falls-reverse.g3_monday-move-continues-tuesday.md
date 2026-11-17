---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.g2_heavy-volume-falls-reverse_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Monday move, measured in its usual daily moves, continues over the next 1 day, and the larger Monday's move, the larger Tuesday's move in the same direction.
Consequence: A trader should follow Monday's move into Tuesday rather than fade it, as the return of weekday liquidity seems to carry new direction.
Why:
- F3: Sunday's move also reverses on Monday (slope -0.45% per usual move, n 2,267, t -3.83). Wednesday and Thursday moves reverse about as much (t -4.05 and -4.08). Monday's own move instead continues into Tuesday (slope +0.26%, t +3.29). The two-day weekend move taken as a whole does not predict Monday (t -0.42).
