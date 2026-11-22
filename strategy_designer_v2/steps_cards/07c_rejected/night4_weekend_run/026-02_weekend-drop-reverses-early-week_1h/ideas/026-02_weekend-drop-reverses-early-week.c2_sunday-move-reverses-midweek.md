---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week
line: 7.c rejected
backtest: 026-02_weekend-drop-reverses-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over Sunday (its 24-hour return to Monday 00:00 UTC) is followed over Monday and Tuesday by a move in the opposite direction; the larger Sunday's move, the larger the opposite move.
Consequence: Sunday's move, more than the whole weekend's, is the part of thin-liquidity trading to lean against when the week opens.
Why:
- F3: Only Sunday's own 24-hour move is reversed over Monday and Tuesday: the slope of the 48-hour strength on the day's return, in usual moves, is -0.155 (t -4.22, 2369 cases) for the day ending Sunday 24:00, while every other day of the week shows |t| ≤ 1.7; Saturday's return has the opposite slope, +0.126 (t 3.37), and the full 48-hour weekend return, which mixes the two, only -0.034 (t -1.27).
- F5: The Sunday reversal holds across the data: the move against Sunday's direction is positive in all 6 coins (from +0.35 % in BTC to +1.06 % in XMR, t from 1.14 to 3.14) and in 7 of 8 years (2023: -0.02 %, t -0.09).
- F6: The Sunday reversal is specific to the weekend: after the days ending Monday to Thursday, the largest-rise quintile was followed by a 0.40 % further rise above drift (t 2.24 for continuation, 1902 cases), not by a fall.
