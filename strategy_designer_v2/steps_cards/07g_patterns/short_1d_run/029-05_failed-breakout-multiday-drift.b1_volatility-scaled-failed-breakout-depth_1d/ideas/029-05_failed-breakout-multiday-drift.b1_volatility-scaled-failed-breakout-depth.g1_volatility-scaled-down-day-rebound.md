---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth
line: 7.g patterns
backtest: 029-05_failed-breakout-multiday-drift.b1_volatility-scaled-failed-breakout-depth_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's 1-day return falls below zero, measured in units of its 20-day daily volatility, the more the coin rises over the next day.
Consequence: A trader would avoid shorting, and lean long, on the day after a coin's unusually large down day compared with its usual daily move.
Why:
- F1: The day after a coin's daily return falls in the lowest tenth when measured in units of its 20-day daily volatility, the coin beats its normal daily drift by +0.53 % (t 3.61, 1450 days). The effect shrinks steadily across the deciles: the second tenth gives +0.27 % (t 2.18), the middle tenths are near 0, and the seventh to ninth tenths are negative (-0.25 %, t -2.26 in the eighth).
- F2: The rebound after the lowest fifth of volatility-scaled days is positive for all six coins: BTC +0.18 %, ETH +0.32 %, LTC +0.32 %, XRP +0.35 %, ZEC +0.37 %, and XMR strongest at +0.85 % (t 4.06). It holds in both halves of the windows (w1–w12: +0.48 %, t 3.91; w13–w24: +0.32 %, t 2.19).
- F7: Several other angles showed nothing that stands out after this many looks, judged by the 8-day excess move by quintile:
