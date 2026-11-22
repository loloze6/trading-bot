---
brief: 028_volume-confirmed-hourly-moves-continue
source-idea: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound
line: 7.g patterns
backtest: 028-01_volume-surge-up-continuation.d1_high-volume-hourly-drops-rebound_1h
instruments: BTC, ETH
bar: 1h
period: folds A, B, C, D
---
Idea: The further a coin has fallen over the past 24 hours relative to its typical move over the past 30 days, the more it rises over the next 24 hours; the further it has risen, the more it falls.
Consequence: A trader would lean against the coin's last day of move, buying after the largest 24-hour falls and selling after the largest 24-hour rises.
Why:
- F4: A coin's standardised 24-hour return is followed by a 24-hour move against it. On the daily grid, the correlation is -0.058 over 5312 non-overlapping cases (t about -4.2). The bottom quintile (largest past falls) is followed by +0.39 % excess (t 2.53, 1063 cases), and the upper two quintiles by -0.24 % (t -2.09) and -0.19 % (t -1.59). The rebound after the largest falls holds in both coins (BTC +0.31 %, t 1.72; ETH +0.46 %, t 1.89) and in both window halves (+0.35 %, t 1.91; +0.42 %, t 1.73).
