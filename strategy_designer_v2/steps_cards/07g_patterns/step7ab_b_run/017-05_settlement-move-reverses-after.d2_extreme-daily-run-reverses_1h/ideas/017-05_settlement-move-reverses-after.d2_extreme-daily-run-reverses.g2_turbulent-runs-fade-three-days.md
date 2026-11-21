---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.d2_extreme-daily-run-reverses
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.d2_extreme-daily-run-reverses_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly volatility over the past week is high, the larger its 24-hour run, measured in usual 24-hour moves, the more of that run it gives back over the next 3 days, more after falls than after rises.
Consequence: A trader can hold a fade of an extreme daily run for three days in turbulent weeks, spreading one trade's cost over a longer and larger move.
Why:
- F1: The reversal of a coin's 24-hour run appears only when its past-week hourly volatility is high: after a run of more than one usual 24-hour move, the forecast-signed drift-adjusted return over the next 24 hours is +189 bps (t 6.32, 859 non-overlapping cases) in each coin's top volatility quintile, against -10 to +20 bps (|t| ≤ 1.12, about 856 cases each) in the four lower quintiles.
- F2: Inside the top volatility tercile the reversal is graded by the size of the run: by quartile of the absolute volatility-scaled 24-hour return, the signed 24-hour return is +6, +7, +63 (t 3.60) and +134 bps (t 6.52), about 1,389 cases each. The upper half is 3 to 7 times the round-trip cost of about 19 bps, while the idea as tested captured only 6 bps per case, 0.3 times that cost.
- F4: The reversal is stronger after falls than after rises. In the top volatility tercile, falls are followed by a rebound of +200 bps (t 6.45, 685 cases) and rises by a give-back of +67 bps (t 2.40, 677 cases). The book's trades show the same split: longs earned +0.32 % net (24,717 trades) and shorts lost -0.96 % net (23,093 trades).
- F5: The high-volatility rebound after falls lasts beyond a day: over the next 72 hours, top-tercile coins earn +253 bps above drift after falls beyond -1.5 usual moves (t 2.59, 100 cases) and +141 bps after falls of -0.5 to -1.5 (t 2.91, 379 cases).
