---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day return relative to its own 20-day daily volatility, the higher its return over the next 7 days.
Consequence: A strong close relative to the coin's usual daily move is a reason to hold it long for the following week, and a sharp down day is a reason to stay out.
Why:
- F1: A coin's one-day return predicts its excess 7-day return better than the tested volume forecast. On the non-overlapping 7-day grid, the pooled slope t is 3.45 (n=2299), against 1.96 for the forecast. The slope is positive in all 6 coins (t from 0.07 for LTC to 2.29 for ETH) and positive in 7 of 8 years (2024 is the exception, at t -1.82).
- F2: Scaling the one-day return by the coin's 20-day daily volatility keeps the effect (pooled t 3.33, n=2155). Its quintiles rise from -0.0186 / -0.0114 (low / high volume half) in the lowest to +0.0172 / +0.0162 in the highest. The pattern is about the same in both volume halves.
- F3: In a joint regression, the volatility-scaled one-day return (t 2.07) and the log volume ratio (t 2.12) each carry their own information, but their product does not (t -0.02). Nearness to the 20-day high adds little once both are in (t 1.30, n=2155).
