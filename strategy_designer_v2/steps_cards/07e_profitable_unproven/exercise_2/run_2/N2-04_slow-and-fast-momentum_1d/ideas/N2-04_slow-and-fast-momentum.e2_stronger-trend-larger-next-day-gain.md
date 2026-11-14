---
brief: 002_moving-average-cross-trend-persistence
source-idea: N2-04_slow-and-fast-momentum
line: 7.e profitable but not proven
backtest: N2-04_slow-and-fast-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The further a coin's 60-day and 20-day returns sit above their own usual size, the larger its return over the following days.
Consequence: A trader can scale a long position up as the coin's slow and fast returns stretch above their normal size, and keep it small when the up-trend is only just beginning.
Why:
- F3: The effect is graded. On held days, the next day's coin return rose with the forecast quartile: 0.0019, 0.0019, 0.0033 and 0.0047 at mean forecasts of 4.2, 9.6, 13.8 and 19.0. The book's daily mean rose from 0.00045 to 0.0051 across the same quartiles.
- F2: The book earns from timing more than from the market's own rise. Of its mean daily return of 0.000754, only 0.000252 is exposure times the coin's drift and 0.000553 is timing (t 3.64), at a mean allocation of 0.21. The coin rose 0.002937 a day while held against 0.000311 while flat (n 5,816 vs 11,564; Welch t 3.21), even though the plan's 20-bar excess return was not significant (mean 0.019, t 0.85, 269 blocks).
- F6: The trade results are right-tailed. The win rate is 45% and the median trade is −0.77%, while the top 10 of 2,401 trades carry 11,493 of the 24,718 summed net percent and the top 5% of trades carry 21,608.
