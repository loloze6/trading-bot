---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue
line: 7.b inconclusive
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return over Sunday, measured against the coin's usual 30-day move, is followed over the next two days (Monday and Tuesday) by a move in the opposite direction. The larger Sunday's move in usual moves, the larger the reversal.
Consequence: A trader would lean against Sunday's move at Monday 00:00 UTC for two days, betting more the larger that move was in usual moves, and would refuse to bet on a continuation of Saturday's move.
Why:
- F4: The effect the brief describes shows clearly one day later, on Sunday's 24-hour move, measured on the bar that opens Sunday 23:00.
- F5: At the 48-hour horizon, Sunday is the only day whose move is strongly reversed. The other days' moves are followed by between -0.19 % (Friday, t -1.55) and +0.35 % (Thursday, t 2.55). Over 24 hours, though, Tuesday's move is also reversed on Wednesday (-0.45 %, t -3.86), so a one-day reversal is not weekend-only.
- F6: Saturday's own move is partly reversed on Sunday (24 hours: -0.23 %, t -2.56), but this is undone by 48 hours (+0.06 %). This explains why a 48-hour bet on Saturday's move captures a total move of only +0.08 % per case, 0.4 times the 0.19 % cost of a trade. Sunday's 48-hour reversal of 0.73 % is about 3.8 times that cost.
- F7: The grading of Sunday's reversal is not yet shown. Sunday's top quintile of |move in usual moves| is reversed by 0.60 % over 48 hours (t -1.54, n 426), no more than the 0.73 % of all Sundays. Whether the reversal is proportional to Sunday's size is what the new idea has to establish.
