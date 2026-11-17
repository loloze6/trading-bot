---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.d1_weekend-move-reverses-both-ways_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a coin's own daily fall that is large against its 20-day volatility, the coin rises over the next 1 day, and the larger the fall in units of its usual daily move, the larger the rebound.
Consequence: A trader could take a long position for one day after a sharp volatility-scaled fall on any weekday, rather than only after weekends.
Why:
- F5: On days other than Sunday, only the largest falls are followed by a next-day rebound. The bottom quintile of the daily return scaled by its 20-day standard deviation (mean z −1.40) is followed by +0.39% excess over the next day (t=3.86, n=2487); the other four quintiles lie between −0.11% and −0.07%, with no t beyond 1.1. All six coins are positive (XMR +0.75%, t=3.43), and 6 of 8 years are positive.
- F3: The Sunday reversal is not graded by size, which is why the supporting check failed. By Sunday z quintile, the 2-day excess return is +0.65%, +0.77%, −0.27%, −1.74% (t=−4.90) and −0.47% (t=−1.25). The largest weekend rises reverse less than the moderate ones, which is why the larger half of |forecast| had the lower reversal (−0.08% difference).
