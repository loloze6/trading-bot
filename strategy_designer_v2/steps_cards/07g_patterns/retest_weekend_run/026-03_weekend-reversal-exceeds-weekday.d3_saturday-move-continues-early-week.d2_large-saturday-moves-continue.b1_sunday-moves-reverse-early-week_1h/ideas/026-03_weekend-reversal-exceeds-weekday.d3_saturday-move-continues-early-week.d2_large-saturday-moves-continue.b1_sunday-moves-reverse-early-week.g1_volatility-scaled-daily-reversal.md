---
brief: 026_weekend-moves-reverse-in-the-week
source-idea: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week
line: 7.g patterns
backtest: 026-03_weekend-reversal-exceeds-weekday.d3_saturday-move-continues-early-week.d2_large-saturday-moves-continue.b1_sunday-moves-reverse-early-week_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 24-hour return, measured in its usual 30-day move, is followed over the next 24 hours by a move in the opposite direction, on any day of the week. The larger that return and the higher the coin's current 30-day usual move against its own usual level of the past three months, the larger the reversal.
Consequence: A trader would lean against the past day's move every day rather than only on Mondays, and bet more when the coin is unusually volatile.
Why:
- F1: The 24-hour reversal is not special to weekends: on a non-overlapping daily grid of every day, the drift-adjusted next-24h return regressed on the past 24h return in usual 30-day moves has a slope of -0.00168 (t -5.85, 12638 cases). By the weekday of the closing day, the next-24h slope is -0.0036 (t -3.9) at Monday 00:00 but just as large on other days: -0.0034 (t -4.6) at Sunday 00:00, -0.0024 (t -4.1) on Friday and -0.0027 (t -3.8) on Thursday. Tuesday's slope is the only positive one (+0.0017, t 2.8).
- F2: That reversal grows with volatility. When the coin's 30-day usual move is measured against its own median over about 83 days, the daily-grid slope is +0.0004 (t 0.9) in the low tercile, -0.0023 (t -4.5) in the middle and -0.0032 (t -6.3) in the high tercile. The z × vol-ratio interaction is -0.0029 (t -3.6). In the high-vol tercile the next-24h return is +0.66 % after the lowest third of 24h moves and -0.25 % after the highest third, a spread of about 0.9 %. That spread is 4.8 times the 0.19 % cost of a trade. The high-vol slope is negative in all 8 years (t from -0.9 to -4.7) and in every coin, with t below -2 everywhere except XRP (t -1.1).
