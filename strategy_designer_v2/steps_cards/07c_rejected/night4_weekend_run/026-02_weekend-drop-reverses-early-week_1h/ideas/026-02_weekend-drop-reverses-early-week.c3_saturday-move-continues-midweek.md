---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week
line: 7.c rejected
backtest: 026-02_weekend-drop-reverses-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over Saturday (from Saturday 00:00 to Sunday 00:00 UTC) is followed by a move in the same direction over Monday and Tuesday; the larger Saturday's move, the larger the move that follows.
Consequence: Saturday's move is a reason to trade with it into the week, not against it.
Why:
- F3: Only Sunday's own 24-hour move is reversed over Monday and Tuesday: the slope of the 48-hour strength on the day's return, in usual moves, is -0.155 (t -4.22, 2369 cases) for the day ending Sunday 24:00, while every other day of the week shows |t| ≤ 1.7; Saturday's return has the opposite slope, +0.126 (t 3.37), and the full 48-hour weekend return, which mixes the two, only -0.034 (t -1.27).
