---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-02_weekend-drop-reverses-early-week
line: 7.c rejected
backtest: 026-02_weekend-drop-reverses-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's price rises over Sunday (from Sunday 00:00 to Monday 00:00 UTC), it falls over the following two days (Monday and Tuesday); the larger Sunday's rise, the larger the fall.
Consequence: A Sunday rally made in thin trading is a reason to sell or short the coin for Monday and Tuesday, and a reason to refuse a long into the week.
Why:
- F3: Only Sunday's own 24-hour move is reversed over Monday and Tuesday: the slope of the 48-hour strength on the day's return, in usual moves, is -0.155 (t -4.22, 2369 cases) for the day ending Sunday 24:00, while every other day of the week shows |t| ≤ 1.7; Saturday's return has the opposite slope, +0.126 (t 3.37), and the full 48-hour weekend return, which mixes the two, only -0.034 (t -1.27).
- F4: The Sunday reversal is mainly on the short side: after a Sunday rise the coin fell 1.05 % below its drift over the next 48 hours (t 4.88, 1225 cases, strength 0.155), against a +0.32 % rise after a Sunday fall (t 1.51, 1144 cases); in the top quintile of Sunday rises the fall was 1.11 % (t 2.93, 474 cases).
- F5: The Sunday reversal holds across the data: the move against Sunday's direction is positive in all 6 coins (from +0.35 % in BTC to +1.06 % in XMR, t from 1.14 to 3.14) and in 7 of 8 years (2023: -0.02 %, t -0.09).
- F6: The Sunday reversal is specific to the weekend: after the days ending Monday to Thursday, the largest-rise quintile was followed by a 0.40 % further rise above drift (t 2.24 for continuation, 1902 cases), not by a fall.
- F7: The Sunday-rise fall is large next to the cost of a trade: the 1.05 % unusual move is about 5.5 times the 0.19 % cost; with the coins' normal drift of about +0.28 % per 48 hours against a short, the total move is about +0.77 %, about 4 times the cost; the tested idea's total move was -0.22 %, -1.1 times the cost.
