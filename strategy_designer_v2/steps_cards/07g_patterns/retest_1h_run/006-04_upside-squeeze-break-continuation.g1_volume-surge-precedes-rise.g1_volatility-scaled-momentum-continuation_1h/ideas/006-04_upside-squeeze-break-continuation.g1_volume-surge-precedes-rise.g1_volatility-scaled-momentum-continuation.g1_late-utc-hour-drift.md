---
brief: 006_range-compression-precedes-expansion
source-idea: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.g1_volume-surge-precedes-rise.g1_volatility-scaled-momentum-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's price rises over the two hours from 21:00 to 23:00 UTC each day, by an amount that grows with the coin's own 20-day hourly volatility.
Consequence: Hold or add long exposure into the late-UTC hours and avoid selling just before them, scaling the expected gain with the coin's recent volatility.
Why:
- F1: Hourly returns between 21:00 and 23:00 UTC rise far more than any other hours. Pooled raw means are 5.5e-4 at 21h (t 6.87) and 4.4e-4 at 22h (t 5.76), against at most t 3.2 for any other hour. In units of each coin's 20-day hourly volatility, the 21–22h bars average +0.032 to +0.061 against about 0 for the other hours, and all six coins are positive (Welch t 1.88 to 3.70). The late-minus-other gap is positive in 18 of 24 windows (t 3.26 across windows) and in 7 of 8 years; 2022 is the exception at −0.053 (t −2.80).
