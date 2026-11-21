---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend.c1_post-settlement-decline-four-hours
line: 7.g patterns
backtest: 017-04_postsettle-decline-after-downtrend.c1_post-settlement-decline-four-hours_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's return over the 2 hours from 20:00 UTC is positive, and the higher its 24-hour volatility at that time, the larger the rise.
Consequence: A trader can hold a coin long through 20:00–22:00 UTC each day, sizing up when its recent volatility is high.
Why:
- F3: Bars starting at 20:00 and 21:00 UTC carry the strongest positive hourly drift of the day. The mean next-bar return was +0.055% (t 6.75) and +0.044% (t 5.66), with n ≈ 17,400 each. The 2-hour return from the 20:00 start is positive in all six coins, +0.084% to +0.108%, t 3.1 to 4.7. It is positive in 7 of 8 years, the exception being 2022 at -0.043%, t -1.43.
- F4: The 20:00–22:00 UTC rise grows with the coin's 24-hour volatility. By volatility tercile it was +0.034% (t 3.15), +0.065% (t 4.34) and +0.192% (t 7.28), each with n ≈ 5,750.
