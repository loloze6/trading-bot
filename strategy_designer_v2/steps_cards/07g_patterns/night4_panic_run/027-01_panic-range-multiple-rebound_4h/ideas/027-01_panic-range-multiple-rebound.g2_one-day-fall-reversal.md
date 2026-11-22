---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-01_panic-range-multiple-rebound
line: 7.g patterns
backtest: 027-01_panic-range-multiple-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: The more a coin's 24-hour return falls below zero, measured in its usual 24-hour moves over the past 30 days, the more it earns above its usual return over the next 24 hours.
Consequence: A sharp 24-hour drop is a reason to buy for a one-day reversal, and the deeper the drop, the larger the expected bounce.
Why:
- F4: The deepest quintile of 24h moves in usual-move units is followed by a 1-day strength of +0.105 (t 5.30, 3190 cases), against -0.039 to -0.050 in the top two quintiles (Spearman -0.090, p 4e-30). It is positive in all 6 coins (t 1.23 to 2.74) and all 8 years (0.040 to 0.259), and holds when clustered by time (t 2.05 over 1210 times).
- F1: Within 24-hour falls, panic severity (the fall's depth in usual 24h moves times the 24h range multiple) predicts the next 3 days in a graded way: the strength runs from -0.035 (t -0.84, 506 cases) in the mildest quintile to +0.052 (t 1.02) in the fourth and +0.209 (t 4.62, 505 cases) in the most severe. Over the next 1 day it runs from -0.025 to +0.152 (t 4.93, 1543 cases).
