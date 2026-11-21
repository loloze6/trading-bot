---
brief: 018_daily-condition-caught-on-the-hour
source-idea: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades
line: 7.b inconclusive
backtest: 018-04_hourly-surge-multiday-continuation.d2_post-selloff-surge-fades_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour return, read at an hourly close, first reaches several times its 30-day average absolute daily return on the upside after its 7-day return before that day was a fall, the price rises less than the coin's usual 1-day return over the next 24 hours; the deeper that 7-day fall, the larger the shortfall.
Consequence: A trader would fade a sharp up day after a week of heavy selling for one day only, most strongly after the deepest falls, rather than hold the fade for a week.
Why:
- F1: The tested shortfall is on the side the idea predicts but too small to show at 5 days: the mean is +0.32 % per case (t 0.74, 559 cases, strength 0.033). On the same cases it is +0.53 % over 24 hours (t 2.51, 572 cases), +0.60 % over 72 hours (t 1.60), and nearly gone at 240 hours (+0.06 %, t 0.08). The fade happens in the first day, and the plan's 5-day horizon dilutes it with four days of noise.
- F2: Over 24 hours the shortfall is graded the way the idea says. Among surges after a 7-day fall (458 events), the deeper the vol-scaled fall, the lower the next 24-hour return (corr 0.17, t 3.74), and the larger the surge, the lower that return (corr 0.15, t 3.31). In the deepest third of falls the 24-hour shortfall is 1.35 % (t 3.45); in the other two thirds it is about zero (-0.31 % and -0.08 %).
- F5: On size, the 5-day test's total move is -0.33 % per case against a 0.19 % round trip, because the coins' normal rise works against a short. The 24-hour shortfall of 0.53 % is about 2.8 times that cost, and the deepest third's 1.35 % is about 7 times it.
