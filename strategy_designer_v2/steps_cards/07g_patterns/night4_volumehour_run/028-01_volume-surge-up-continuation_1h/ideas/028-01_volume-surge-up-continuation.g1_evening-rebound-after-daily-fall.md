---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-01_volume-surge-up-continuation
line: 7.g patterns
backtest: 028-01_volume-surge-up-continuation_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: In the two hours after 20:00 UTC, a coin rises, and the further it has fallen over its past 24 hours (measured against its usual 24-hour move), the larger that rise.
Consequence: A trader can buy a coin into the late-UTC evening after a 24-hour fall, sizing the position with the depth of the fall, and avoid evening longs after a 24-hour rise.
Why:
- F1: The next-hour return is unusually high from the closes of the bars opening at 20:00 and 21:00 UTC. Pooled over both coins the excess mean was +0.045 % (t 4.0) and +0.040 % (t 3.7), about 5,835 cases each. It holds in each coin on its own: for the bar opening at 21:00 the excess return scaled by the 30-day usual hourly move has t 3.6 in BTC and 3.4 in ETH, 2,200 cases each. These are the only two hours out of 24 at |t| > 3.4.
- F2: That two-hour rise depends on the previous 24 hours. Measured from the close of the bar opening at 19:00 UTC, the excess return over the next two hours was +0.133 % (t 2.6, 880 cases) after the bottom quintile of the 24-hour move scaled by the usual move, and +0.076 % (t 2.0) after the second quintile. It was −0.004 % (t −0.1) in the middle quintile, −0.067 % (t −2.1) in the fourth and −0.029 % (t −0.8) in the top. So the larger the prior fall, the larger the evening rise.
- F3: The evening two-hour rise is positive in both coins overall: BTC +0.036 % (t 1.85) and ETH +0.051 % (t 2.09), 2,918 cases each. By year it is positive in 7 of 8 years for BTC and 6 of 8 for ETH, but significant only in 2020 (t 3.0 and 2.6). Its mean of about +0.04 to +0.09 % is below the 0.11 % cost of a trade unless it is concentrated by the prior 24-hour fall.
