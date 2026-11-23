---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth
line: 7.g patterns
backtest: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's 1-day return falls below zero, measured in units of its 20-day daily volatility, the more the coin rises over the next 8 days.
Consequence: A trader would refuse multi-day shorts opened after a large down day, and could hold a long for about a week after one.
Why:
- F3: Over 8 days on the non-overlapping grid, the lowest fifth of volatility-scaled daily returns is followed by an excess rise of +2.92 % (t 3.25, 339 cases). The fourth fifth is followed by an excess fall of -1.80 % (t -2.79). The ordering is the same in both halves: early +4.00 % (t 3.39), late +1.96 % (t 1.47).
- F1: The day after a coin's daily return falls in the lowest tenth when measured in units of its 20-day daily volatility, the coin beats its normal daily drift by +0.53 % (t 3.61, 1450 days). The effect shrinks steadily across the deciles: the second tenth gives +0.27 % (t 2.18), the middle tenths are near 0, and the seventh to ninth tenths are negative (-0.25 %, t -2.26 in the eighth).
