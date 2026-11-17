---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's 7-day return, the higher its return over the next 7 days.
Consequence: A coin that rose strongly over the past week is a reason to hold it long for the next week, and a coin that fell over the past week is a reason to refuse a long.
Why:
- F3: Momentum carries over: the 7-day return predicts the demeaned 7-day forward return (slope 0.056, t = 2.72, n = 2299) and the 30-day return does too (slope 0.025, t = 2.88, n = 1723), but by coin it is mixed (XRP t = 3.48 and ZEC t = 2.57 positive, XMR t = -0.92 to -1.65 and LTC t = -0.79 negative).
- F4: Closeness to the 30-day high, the brief's own variable, carries no linear information about the next 3 days (slope t = 0.06 on all bars, t = -0.25 in rising months, n = 4283 and 2187); only its top quintile stands out (+0.62%, t = 2.24).
