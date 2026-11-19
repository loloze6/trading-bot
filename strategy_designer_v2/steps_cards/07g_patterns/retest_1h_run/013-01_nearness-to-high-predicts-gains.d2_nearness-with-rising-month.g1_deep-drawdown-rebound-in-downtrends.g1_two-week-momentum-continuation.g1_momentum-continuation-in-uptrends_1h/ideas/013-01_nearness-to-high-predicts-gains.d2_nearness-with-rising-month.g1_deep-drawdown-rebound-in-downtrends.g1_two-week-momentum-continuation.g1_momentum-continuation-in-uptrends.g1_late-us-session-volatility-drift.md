---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the two hours from 20:00 to 22:00 UTC is positive, and larger the higher its 14-day volatility.
Consequence: A trader would lean long into the 20–22 UTC hours, more heavily in coins that have been volatile over the past two weeks.
Why:
- F1: The coins' average next-hour return is clearly positive in two hours of the day, 20:00 UTC (+4.8 bp, t 2.93, n 2917 timestamps after averaging the coins at each hour) and 21:00 UTC (+3.7 bp, t 2.44, n 2920), and the 20–21 UTC pair is positive in all 6 coins (+3.7 to +4.8 bp) and in 7 of 8 years (only 2022 is negative, at −2.7 bp); with 24 hours tested this would be borderline on its own, but it holds in every coin and in nearly every year.
- F2: The 20–21 UTC drift grows with the coin's 14-day volatility: +2.1 bp (t 2.69) in the calmest quintile against +11.2 bp (t 5.51) in the most volatile quintile, n ≈ 6560 per quintile pooled across coins, so these t's are overstated by the coins moving together.
