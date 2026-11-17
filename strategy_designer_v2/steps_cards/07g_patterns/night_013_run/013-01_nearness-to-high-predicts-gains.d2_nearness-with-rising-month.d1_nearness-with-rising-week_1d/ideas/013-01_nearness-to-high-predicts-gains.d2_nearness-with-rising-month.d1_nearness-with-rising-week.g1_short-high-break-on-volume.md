---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits to its highest close of the past 20 days, and the heavier that day's volume against its 30-day average, the higher the coin's return over the next 7 days.
Consequence: Favour longs in coins pressing their 20-day high on heavy volume, and distrust near-high closes on thin volume.
Why:
- F1: Closeness to the 20-day closing high predicts the next 7 days better than closeness to the 52-week high, and it works best with heavy volume. On 1,958 non-overlapping 7-day grid cases, the combined rank of 20-day-high closeness and the day's volume (over its 30-day mean) gives a slope t of 3.95 on the 7-day return minus the coin's mean. Taken alone, 20-day-high closeness has t 3.49; in a multivariate fit with 52-week closeness it keeps t 2.31 while 52-week closeness turns negative (t -2.24, n 558).
- F2: Volume grades the gain near the 20-day high. In the top fifth of 20-day-high closeness, the 7-day excess return rises with volume: 0.0033 (n 131), then 0.0159 (n 130), then 0.0318 (n 131). In the joint table, top closeness with top-tercile volume gives +0.0369 (n 201), against -0.0162 for top closeness with bottom-tercile volume (n 78).
- F3: The 20-day-high-plus-volume slope is positive in 6 of 8 years, with t above 2 in 2020 (2.32), 2024 (3.02) and 2025 (2.12). It is negative in 2018 (-0.85) and 2023 (-0.58), so it is not steady every year.
