---
brief: 023_range-reversion-when-no-trend
source-idea: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b2_near-high-momentum-three-days
line: 7.g patterns
backtest: 023-03_flatter-range-stronger-reversion.d2_monthly-return-momentum-continuation.d1_momentum-near-the-60-day-high.b2_near-high-momentum-three-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day return measured in units of its own daily volatility over the past 20 days, the larger its move in the same direction over the next 3 days, and the more so the calmer its past 20 days have been.
Consequence: A trader leans with a sharp 3-day move when the coin has been quiet for weeks, and gives the same move little weight when the coin is already volatile.
Why:
- F1: Over the next 3 days a coin follows its own past 3 days only when it has been calm. On non-overlapping 3-day cases, regressing the standardised excess return on the 3-day return scaled by the 20-day daily volatility gives slope 0.067 with t 3.70 (n 1716) in each coin's lowest-volatility tercile, against t 0.80 and 0.84 in the middle and highest terciles (n 1715 and 1716).
- F2: Inside the calm tercile the continuation is graded. The mean excess 3-day return rises from −0.73 % (t −2.18, n 348) in the most-down quintile of the scaled 3-day return to +0.74 % (t 1.99, n 342) in the most-up quintile.
- F3: The calm-tercile continuation holds in both halves of the record and in most coins, so it is not one period. The slope's t is 2.35 in w1–w12 (n 983) and 2.86 in w13–w24 (n 733); by coin it is 3.57 for ETH, 2.16 for XRP, 1.78 for BTC, 0.92 for ZEC and 0.78 for LTC, and −0.37 for XMR (n 286 each).
- F4: The same grading shows when calm is measured against the coin's own recent history. With 20-day volatility divided by its 120-day median, the slope on the scaled 3-day return is t 2.26 in the lowest tercile, 0.76 in the middle and −0.33 in the highest (n about 1091 each). The 20-day mean deviation in volatility units gives t 3.09 in the calm tercile and 0.83 and 1.44 in the others.
