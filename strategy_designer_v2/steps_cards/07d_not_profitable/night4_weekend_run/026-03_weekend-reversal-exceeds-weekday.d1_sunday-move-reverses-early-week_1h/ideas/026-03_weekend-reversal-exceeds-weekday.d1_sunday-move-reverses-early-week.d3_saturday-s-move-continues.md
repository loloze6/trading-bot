---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week
line: 7.d not profitable
backtest: 026-03_weekend-reversal-exceeds-weekday.d1_sunday-move-reverses-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Saturday is followed by a move in the same direction over Monday and Tuesday: the larger Saturday's 24-hour return, the larger the move its way over the next two days.
Consequence: A trader would lean with Saturday's move into the week, the opposite of fading the whole weekend.
Why:
- F2: Regressing the next 48 hours on both days shows they pull in opposite directions. Sunday's 24-hour return reverses (slope −0.154, t −4.09), while Saturday's continues (slope +0.104, t 2.79), over 2355 coin-weeks. Sunday minus Saturday gives a slope of −0.129 (t −5.07); the 48-hour weekend sum gives only −0.024 (t −0.87).
- F3: The edge is graded on Sunday's move minus Saturday's, read in the bet's direction. The 48-hour gain rises across quintiles from −0.23 % (t −0.68) to +0.13 %, +0.79 %, +0.89 % and +1.34 % (t 2.98), about 471 cases each. A pure Sunday reversal with no counter-Saturday is worth nothing.
