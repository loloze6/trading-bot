---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades
line: 7.g patterns
backtest: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin's 24-hour return falls below zero, measured against its 30-day average absolute daily return, the more its price rises above its usual drift over the next 1 to 2 days. The rebound is larger the higher the coin's 30-day volatility.
Consequence: A trader would buy a coin after an unusually deep one-day fall, more heavily the deeper the fall and the more volatile the coin, rather than sell into it or follow it short.
Why:
- F1: A sharp 24-hour fall is followed by a rebound. On a daily grid of all six coins, the bottom decile of the 24-hour return measured in the coin's 30-day mean absolute 24-hour return beats the coin's normal drift by +0.70 % over the next 24 hours (t 4.30, 1408 cases), +0.82 % over 48 hours and +0.77 % over 72 hours (t 3.25). The second decile beats it by +0.34 % over 24 hours (t 2.59). The middle deciles are near 0 to -0.16 %.
- F2: The rebound is graded and appears in every coin. On days with a 24-hour fall, the deeper the fall, the larger the next-24-hour excess return. The Spearman rho on the 24-hour return is -0.066 to -0.157 for all six coins, and every p is below 0.025 (XRP p 4e-8, ETH 6e-4, XMR 1.6e-3, ZEC 1.7e-3, LTC 0.013, BTC 0.024).
- F3: The rebound holds in both halves of the windows. In the bottom two deciles, the 24-hour excess is +0.53 % in w1–w12 (t 4.34, 1385 cases) and +0.51 % in w13–w24 (t 3.02, 1431 cases). This makes it the most robust of the roughly 15 angles examined.
- F4: The rebound grows with the coin's 30-day volatility. Over 24 hours after the bottom two deciles of the 24-hour return, the excess is -0.002 % in the lowest volatility tercile (t -0.01, 969 cases), +0.35 % in the middle tercile (t 2.19, 982) and +1.30 % in the highest (t 5.17, 865). The top tercile's move is about 6.8 times the backtest's 0.19 % round-trip cost, against 3.7 times for the 0.70 % decile average.
- F5: The rebound does not depend on the prior 7-day trend. After the bottom two deciles of the 24-hour return, the 24-hour excess is +0.46 % when the 7-day return was negative (t 3.42, 1951 cases) and +0.67 % when it was positive (t 4.25, 863).
