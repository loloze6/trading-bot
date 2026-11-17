---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.d2_weekend-falls-rebound-early-week.g1_high-volatility-one-day-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin whose last day's fall was large relative to its usual daily move over the past 60 days rises over the next 1 day. The rise is larger the larger that scaled fall and the higher the coin's 20-day volatility stands against its own 60-day history.
Consequence: Buy sharp falls in turbulent stretches for one day, and do not short sharp rises symmetrically.
Why:
- F1: The reversal is almost all on falls. In the top third of 20-day volatility against its 60-bar history, the largest third of down days were followed by a next-day market-adjusted return of +0.0100 (t 5.74, n 1056). The largest third of up days in the same tercile were followed by only −0.0028 (t −1.76, n 1138). In the middle volatility tercile the large down days gave +0.0041 (t 2.17, n 740) and the large up days −0.0006 (t −0.34, n 791).
- F2: Across deciles of the scaled 1-day move, only the two most negative deciles were followed by clearly positive next-day returns: +0.0070 (t 4.68, n 1436) and +0.0030 (t 2.35, n 1436). The top decile gave −0.0015 (t −1.10, n 1436), so the up-side fade the book trades adds little.
- F3: The rebound after large high-volatility falls is stable over time: +0.0053 (t 4.15, n 1115) in windows w1–w12 and +0.0057 (t 3.13, n 1180) in w13–w24.
