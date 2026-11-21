---
brief: 016_grind-versus-jump-moves
source-idea: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising
line: 7.d not profitable
backtest: 016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_efficient-rise-keeps-rising_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more efficiently a coin has risen over its past 3 days, the more it keeps rising over the next 3 days, the more so the closer its price stands to its highest close of the past 30 days.
Consequence: An efficient rise that pushes into new 30-day highs is a reason to be long and larger, while one far below its 30-day high is a weak reason.
Why:
- F4: On the 72-bar grid, the idea's effect appears only with a positive 30-day return.
- F5: Across all positive-forecast cases, the efficiency effect is graded only at its top. Excess 72-bar returns by efficiency quintile run -0.51 %, -0.22 %, -0.10 %, +0.20 %, +1.16 % (top t 2.87, 573 cases each). The idea's overall unusual move is -0.13 % per case, so most of the forecast range sizes the book on noise.
- F6: Efficient rises close to the 30-day high continue most. In the top third of efficiency and the nearest third to the 30-day high, the excess 72-bar move is +1.44 % (t 2.80, 369 cases). Far from the high it is +0.43 % (t 0.70, 168 cases).
