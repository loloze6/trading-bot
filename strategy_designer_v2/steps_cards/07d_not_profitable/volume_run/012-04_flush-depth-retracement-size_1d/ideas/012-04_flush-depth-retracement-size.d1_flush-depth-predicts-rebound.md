---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-04_flush-depth-retracement-size
line: 7.d not profitable
backtest: 012-04_flush-depth-retracement-size_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among daily bars that fall sharply on a volume burst, the larger the bar's drop from its open to its low, the larger the price rise over the next 3 days, as the cascade is retraced.
Consequence: A trader would buy deep open-to-low flushes on heavy volume whether or not a long lower wick formed, and hold through the 3-day retracement rather than one day.
Why:
- F1: The book holds each flush for about one day while the rebound shows only over three: all 75 trades last about 24 hours, positions are held on 0.43% of bars, and flush-regime bars show an excess 1-day return of -0.0099 (t -1.45, n 76) against +0.0025 over 3 days, so every coin's trades lose on average (mean net -0.40% for BTC up to -2.46% for XRP).
- F2: The book trades too rarely (0.0043 trades per bar) because the wick condition cuts the situation down and removes its effect: falls of at least 1.5 usual moves on at least 1.5x volume give 477 bars with excess returns of +0.0086 over 1 day (t 2.92) and +0.0082 over 3 days (t 2.16), while adding a lower wick of at least 0.3 of the range leaves 145 bars with -0.0070 over 1 day (t -1.30).
- F3: Among those 477 volume-burst falls, a deeper open-to-low drop is followed by a larger 3-day rise: slope 0.168 (t 3.57, n 470), with the deepest quartile (drop above 16%) at +0.031 (t 3.18) and the other three quartiles between -0.0006 and +0.0007.
- F5: The lower wick adds nothing or hurts: its 3-day slope among volume-burst falls is -0.0038 (t -0.16), and among falls beyond 1 usual move, wicks of 0 to 0.1 of the range are followed by +0.015 over 3 days against -0.0063 for wicks of 0.6 to 0.8.
