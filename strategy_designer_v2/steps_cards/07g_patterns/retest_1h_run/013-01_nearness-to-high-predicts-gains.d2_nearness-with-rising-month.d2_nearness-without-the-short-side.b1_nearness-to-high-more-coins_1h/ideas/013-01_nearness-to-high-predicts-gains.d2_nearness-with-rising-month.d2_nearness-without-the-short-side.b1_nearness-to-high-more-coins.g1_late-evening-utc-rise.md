---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1h
period: folds A, B, C, D
---
Idea: Each coin rises over the two hours from 21:00 to 23:00 UTC, and the rise is larger the higher the coin's hourly volatility over the past 7 days.
Consequence: A trader holding or adding long exposure into 21:00 UTC captures a recurring rise, sized up when the coin's recent volatility is high.
Why:
- F1: Each coin rises in the two hours from 21:00 to 23:00 UTC: the mean 2-hour return is 0.000991 (t = 10.75, n = 24274 non-overlapping days). The hourly log returns are 0.000416 (t = 7.03) at 21:00 and 0.000492 (t = 8.72) at 22:00, the two highest t values of the 24 hours. The pattern holds in all 19 coins (excess over the other hours from 0.000067 in TRX to 0.001429 in ONDO) and in 7 of 8 years, 2022 being the one negative year (-0.000383).
- F2: The evening rise grows with the coin's 7-day hourly volatility, rising steadily across volatility quintiles from 0.000344 (t = 3.14) in the calmest to 0.002604 (t = 8.37) in the most volatile, n = 4855 each. It is the same while the 30-day return is positive (0.000982) or not (0.001001).
