---
brief: 027_panic-days-are-followed-by-a-premium
source-idea: 027-01_panic-range-multiple-rebound
line: 7.g patterns
backtest: 027-01_panic-range-multiple-rebound_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin falls over a 24-hour stretch, it earns more than its usual return over the next 3 days. The deeper the fall in usual 24-hour moves, and the larger the stretch's high-low range as a multiple of its 30-day average 24-hour range, the larger that excess return.
Consequence: The forced-selling discount is earned back within days, not weeks, so a panic rebound should be held for about 3 days rather than 14.
Why:
- F1: Within 24-hour falls, panic severity (the fall's depth in usual 24h moves times the 24h range multiple) predicts the next 3 days in a graded way: the strength runs from -0.035 (t -0.84, 506 cases) in the mildest quintile to +0.052 (t 1.02) in the fourth and +0.209 (t 4.62, 505 cases) in the most severe. Over the next 1 day it runs from -0.025 to +0.152 (t 4.93, 1543 cases).
- F2: The same panic premium is gone by 14 days, which explains the tested idea's null result: among falls, the 24h fall depth has no link to the 14-day excess (Spearman -0.014, p 0.76, 489 cases), and the tested cases' unusual move over 84 bars was -0.13 % (t -0.21, 1144 cases).
- F3: The top quintile of the 24h range multiple is followed by a 3-day strength of +0.172 (t 4.93, 1032 cases). It is +0.236 (t 4.94, 560 cases) after falls against +0.097 (t 1.89, 472 cases) after rises, holds when clustered by time (t 2.52 over 460 distinct times), and is positive in all 6 coins (0.055 to 0.314) and all 8 years (0.035 to 0.383).
