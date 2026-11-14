---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.b inconclusive
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 50-day SMA is above its 200-day SMA, if the coin's return over the past 60 days is negative, its next 10-day return falls further below its usual 10-day return than after a negative past 30 days alone.
Consequence: Treat a two-month decline under a standing golden cross as the strongest reason to stay out of the coin.
Why:
- F3: The split is monotonic in past momentum: across past-30-day quintiles within forecast > 0, the mean excess return runs -0.024 (t=-2.00), -0.031 (t=-2.73), +0.002, +0.019 (t=1.54) and +0.027 (t=1.14). The same sign split holds over other look-backs: past 60 days negative gives -0.041 (n=126, t=-3.64) against +0.011 (n=297, t=0.99), and past 10 days negative gives -0.020 (t=-2.57) against +0.016 (t=1.60).
- F1: Among blocks with forecast > 0, the coin's own past 30-day return splits the result in two: after a negative past 30 days the excess 10-bar return is -0.0264 (n=265, t=-3.32), and after a positive one it is +0.0173 (n=359, t=1.68); the two cancel to +0.0005 overall, against +/-0.158 dispersion, giving the flat pooled slope (t=0.37).
