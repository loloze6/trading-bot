---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades
line: 7.g patterns
backtest: 021-01_above-rising-cloud-continues-up.d2_distance-from-cloud-grades_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's 14-day volatility is low compared with its own past, its return over the next 7 days is larger the larger its 26-day return.
Consequence: A trader would follow a coin's 26-day trend over the following week mainly when the coin is calm, scaling the lean by the size of that trend.
Why:
- F4: The 26-day return predicts the next 7 days only in calm conditions, so this is momentum inside a volatility regime:
- F5: The tested cloud-distance forecast is weak at its own 26-day horizon (t 1.58, 576 cases) and is no stronger than plain 26-day momentum (t 2.51, 432 cases). That momentum is itself unstable: t -0.56 in w1 to w12 and t 4.41 in w13 to w24. By coin, the cloud forecast's t runs from -0.98 for XRP to 2.01 for BTC.
