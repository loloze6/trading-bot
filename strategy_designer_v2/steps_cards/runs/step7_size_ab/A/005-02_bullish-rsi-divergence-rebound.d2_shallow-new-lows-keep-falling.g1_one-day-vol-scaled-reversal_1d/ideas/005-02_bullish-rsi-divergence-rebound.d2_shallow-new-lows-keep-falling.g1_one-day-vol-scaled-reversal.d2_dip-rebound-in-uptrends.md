---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d2_shallow-new-lows-keep-falling.g1_one-day-vol-scaled-reversal_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 1-day fall relative to its own 20-day daily volatility, and the nearer its close to the day's low, the more it rises over the next 1 day, and the more so the higher its 60-day return.
Consequence: A trader should buy sharp vol-scaled down days most heavily when the coin has been rising over the past 60 days.
Why:
- F1: The book's gain before fees does not cover its fees. Gross gain is 0.000231 per day and fees are 0.000360 per day, so the net is -0.000129, which matches the book's mean daily return of -0.000134 (Sharpe -0.19) at 0.80 trades per bar.
- F2: The long side pays and the short side loses. Long days (n=2823) earn 0.000769 gross, of which 0.000306 is timing and 0.000464 is the coin's drift. Short days (n=2958) lose 0.000281 gross because holding short against the coin's rise costs 0.000351, and their timing adds only 0.000071.
- F6: The long rebound is stronger inside a 60-day uptrend. Long days earn 0.001116 gross (timing +0.000584, n=720) when the 60-day return is positive, against 0.000169 (timing -0.000234, n=727) when it is negative.
- F7: Small moves still carry positions and fees. In the middle deciles of the vol-scaled move (z -0.08 to +0.31), positions are 0.05 to -0.12 and gross is -0.000192 to +0.000201. Fees are paid on these days as on others, about 0.00036 a day overall.
