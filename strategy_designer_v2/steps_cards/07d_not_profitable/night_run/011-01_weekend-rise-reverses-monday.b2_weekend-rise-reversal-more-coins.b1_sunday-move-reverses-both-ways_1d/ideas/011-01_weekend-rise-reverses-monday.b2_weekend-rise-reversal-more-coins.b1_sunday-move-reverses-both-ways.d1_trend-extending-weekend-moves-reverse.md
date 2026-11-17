---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that moved over the weekend (its Saturday-to-Sunday close-to-close return) moves the other way over the next 2 days (Monday and Tuesday), and the larger the weekend move in either direction, the larger the move back, all the more when the weekend move ran in the same direction as the coin's 20-day return.
Consequence: A trader would lean hardest against Sunday moves that extend the coin's recent 20-day trend and hold the lean through Tuesday, and would size down against Sunday moves that run against the trend.
Why:
- F2: The reversal the book bets on lasts two days, but the book is held only on Monday: per active Sunday (n = 5238), the gross Monday gain is 0.00147 (t = 3.99) and the Tuesday gain it would have added is 0.00099 (t = 2.84), and the signed Tuesday move against Sunday's move is +0.0027 after falls and +0.0044 after rises.
- F3: The gain comes almost entirely from the largest Sunday moves. The top |forecast| tercile makes 0.0040 per case on Monday at a mean |allocation| of 0.73, against 0.00005 for the bottom tercile at 0.075. The bottom two terciles each make less than the roughly 0.0009 round-trip fee (0.00044 on Sunday plus 0.00043 on Monday).
- F4: Sunday's own move grades the reversal better than the two-day weekend move. Its Spearman correlation with the next two days' reversal is 0.120, against 0.029 for the Saturday-plus-Sunday return (n = 4320).
- F5: Sunday moves that run with the coin's prior 20-day return reverse more over Monday and Tuesday than moves against it. The signed two-day reversal is 0.0154 vs 0.0060 in the largest |z| quartile and 0.0126 vs 0.0039 in the second quartile (about 510–570 cases each).
- F6: Shorting Sunday rises loses when the 20-day trend is flat: −0.00017 per case on Monday in the middle 20-day-return tercile (n = 756). In the down and up terciles it gains 0.0016 and 0.0007.
