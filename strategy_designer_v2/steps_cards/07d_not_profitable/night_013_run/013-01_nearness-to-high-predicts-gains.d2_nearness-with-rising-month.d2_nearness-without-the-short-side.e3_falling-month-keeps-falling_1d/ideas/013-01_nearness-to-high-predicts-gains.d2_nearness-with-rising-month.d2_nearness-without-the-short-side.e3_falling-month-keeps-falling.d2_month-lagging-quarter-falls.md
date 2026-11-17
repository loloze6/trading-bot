---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's 30-day return falls below its 90-day return, the lower its return over the next 3 days.
Consequence: A coin whose month has turned down sharply against its quarter is a reason to stay out of longs for the next few days, more so the wider the gap.
Why:
- F2: The 30-day fall is not graded the way the idea says, because the deepest falls rebound. Among forecast < 0 grid cases, the deepest forecast quintile (mean forecast -18.1, n=577) is followed by +0.0025 excess 3-day return, while the middle quintiles show -0.0069, -0.0048 and -0.0057, so the deep half beats the shallow half by +0.0016.
- F6: Across 90-day return quartiles of the active cases, the follow-up falls as the quarter rises. The deepest quarterly falls (mean -0.51) are followed by +0.0084, while the top two quartiles (mean -0.07 and +0.58) show -0.0102 (t -2.17) and -0.0107 (t -2.03).
- F7: Measured as the 30-day return minus the 90-day return, the larger the month's shortfall against its quarter, the lower the next 3 days. The bottom quartile of that gap is followed by -0.0088, the next by -0.0083 (t -2.00), and the top quartile by +0.0074.
