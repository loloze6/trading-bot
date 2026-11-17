---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.b1_sunday-move-reverses-both-ways_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's daily close-to-close move is partly undone over the next day on any day of the week, and the larger that day's move relative to the coin's usual daily move over the past 60 days, the larger the move back.
Consequence: A trader would lean against every large daily move rather than Sunday's alone, so the book is exposed on many more days and its mean daily return can grow.
Why:
- F1: The book earns only on Mondays: its mean on Mondays is 0.00150, every other weekday is about 0 (Sunday −0.00037, from fees), and it holds a position on only 28.6 % of days with an average |allocation| of 0.053, so its mean daily return of 0.000162 is far below holding's 0.00139.
- F3: The gain comes almost entirely from the largest Sunday moves. The top |forecast| tercile makes 0.0040 per case on Monday at a mean |allocation| of 0.73, against 0.00005 for the bottom tercile at 0.075. The bottom two terciles each make less than the roughly 0.0009 round-trip fee (0.00044 on Sunday plus 0.00043 on Monday).
- F7: The next-day reversal is not limited to the weekend. The mean of −sign(today's move) × the next day's return is 0.00325 after Sunday but also 0.00312 after Tuesday and 0.00186 after Saturday (about 5,200 cases each), so a one-day-a-week book leaves most of this effect unused.
