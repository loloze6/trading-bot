---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high
line: 7.g patterns
backtest: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The closer a coin's close stands to its 30-day closing high, counted in its usual daily moves, the more the coin rises over the next 10 days above its usual 10-day return.
Consequence: A trader would size a long by how few daily moves separate the price from its month's high, and stay out when the price sits many daily moves below it.
Why:
- F1: Over the next 10 days, the bars whose close is within about 1.2 usual daily moves of the 30-day closing high (the top quintile of distance measured in daily volatilities, 249 non-overlapping cases) end 4.9 % above the coin's normal drift (strength 0.29, t 3.53). That is about 25 times the 0.19 % cost of a buy and a sell. Over 5 days the same quintile gives +1.71 % (strength 0.148, t 2.86, 535 cases). The effect is not graded across the other quintiles: the fourth is the worst at 10 days (-2.67 %, t -2.98).
- F3: The near-high effect is not stable. Top minus bottom quintile of distance from the 30-day high is +0.52 usual moves at 10 days in windows w13-w24 (t 3.20) and -0.05 in w1-w12 (t -0.41). It is negative in 2022 and 2023 (-0.61 and -0.59, t about -2.2 each). Per coin, the rank correlations of distance against the 10-day move are small: -0.07 to +0.12, none with p below 0.08.
- F5: The 24-hour surge the tested idea uses grades the 5-day move only weakly. Its top quintile, 1 to 11 usual daily moves, has strength 0.071 (t 1.47, 535 cases), and the quintiles below are not ordered. In the book, the trades entered at the lowest forecast quartile earn the most: +4.1 % net per trade, held 597 hours on average, against +2.9 to +3.5 % for the higher quartiles.
