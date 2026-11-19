---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation
line: 7.g patterns
backtest: N2-04_slow-and-fast-momentum.e1_short-horizon-dual-momentum-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's fall over the past 24 hours, the more its return over the next 1 day exceeds its average daily return, and the effect is stronger the higher the coin's 30-day volatility.
Consequence: A trader can buy a coin after a sharp one-day drop, more so when the coin is volatile, rather than sell into the fall, and should expect the rebound within a day.
Why:
- F1: A large 24-hour fall is followed by a rebound over the next day: in the lowest decile of the coins' 24-hour return (mean -8.6 %), the next 24 hours beat the coin's mean 24-hour return by +0.93 % (t 5.56, 1713 non-overlapping cases), while the middle deciles sit between -0.17 % and +0.09 % (|t| < 1.7).
- F2: The 24-hour reversal holds in every coin and nearly every year: the correlation of the past 24-hour return with the next 24-hour excess return is negative in all six coins (-0.064 for XRP to -0.129 for XMR, about 2,760 to 2,870 cases each) and in 7 of 8 years (-0.037 to -0.164; only 2024 is positive, at +0.008).
- F3: The reversal depends on volatility: the same correlation is -0.107 in the highest tercile of 30-day volatility, -0.038 in the middle tercile and -0.003 in the lowest (about 4,300 cases each), and scaling the fall by volatility still leaves the lowest quintile at +0.47 % next-day excess (t 4.36, 2588 cases).
- F5: The reversal is gone by three days: on the non-overlapping 72-hour grid, the 72-hour excess return by quintile of the past 24-hour return ranges from -0.37 % to +0.35 % with all |t| < 1.6, about 1,130 cases each.
