---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high
line: 7.g patterns
backtest: 018-04_hourly-surge-multiday-continuation.d1_surge-near-monthly-high_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin whose close stands near its 30-day closing high keeps rising over the next 10 days by more than its usual 10-day return, and the larger its 7-day return measured in usual daily moves, the larger that rise.
Consequence: A trader would buy strength that arrives at the month's high and hold it for over a week, and refuse a position near the high when the past week was flat or falling.
Why:
- F1: Over the next 10 days, the bars whose close is within about 1.2 usual daily moves of the 30-day closing high (the top quintile of distance measured in daily volatilities, 249 non-overlapping cases) end 4.9 % above the coin's normal drift (strength 0.29, t 3.53). That is about 25 times the 0.19 % cost of a buy and a sell. Over 5 days the same quintile gives +1.71 % (strength 0.148, t 2.86, 535 cases). The effect is not graded across the other quintiles: the fourth is the worst at 10 days (-2.67 %, t -2.98).
- F2: Among bars in the two quintiles nearest the 30-day high, the coin's past 7-day return grades the move over the next 10 days. From the lowest to the highest tercile the strength is -0.12, +0.01 and +0.38 (about 166 cases each; top minus bottom about 0.50 usual moves, roughly t 4.5). Over 5 days the terciles give -0.04, +0.08 and +0.14 (about 357 cases each; difference roughly t 2.4).
- F3: The near-high effect is not stable. Top minus bottom quintile of distance from the 30-day high is +0.52 usual moves at 10 days in windows w13-w24 (t 3.20) and -0.05 in w1-w12 (t -0.41). It is negative in 2022 and 2023 (-0.61 and -0.59, t about -2.2 each). Per coin, the rank correlations of distance against the 10-day move are small: -0.07 to +0.12, none with p below 0.08.
