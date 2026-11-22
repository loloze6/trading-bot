---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend
line: 7.g patterns
backtest: 025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 60-day return is positive, the 5-day return is higher the higher its 30-day return measured in usual daily moves, on any day and not only after a sharp rise.
Consequence: In a coin rising over two months, a trader would lean long in proportion to the strength of its last month, and would not use the last month's move as a signal in a coin falling over two months.
Why:
- F1: The 30-day trend effect holds only in coins whose 60-day return is positive. Regressing the 5-day excess return on the 30-day move in usual daily moves gives a slope t of 3.10 on 843 grid cases when the 60-day return is up, and t -0.13 on 848 cases when it is down. By 60-day tercile the slope t is -0.31 in the lowest third, 3.65 in the middle and 2.56 in the top, about 564 cases each.
- F2: The 30-day trend effect does not need a sharp up day. On ordinary days (1-day move between -1 and +1 usual moves) the slope of the 5-day excess return on the 30-day move has t 2.44 on 1858 cases, against t 1.37 on the 92 sharp-rise cases. Over all grid bars it has t 3.03 on 2555 cases. Ordinary days after a falling month have a 5-day excess return of -0.84 % (t -2.45, 928 cases).
- F4: Longs depend on the longer trend. Long bars earn +0.56 % per bar when the coin's 60-day return is up (t 3.52, 950 bars) and -0.15 % when it is down (t -1.45, 349 bars).
- F3: The book's gain comes from its long side. Long bars earn +0.35 % per bar (t 4.45, 2440 bars) against +0.08 % for short bars (t 1.79, 1276 bars). Short trades lose 2.43 % on average after fees with 33 % winners, while long trades gain 3.85 % with 59 % winners.
