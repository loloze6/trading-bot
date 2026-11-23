---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger the coin's 24-hour return after the first hour following the 00:00 UTC settlement runs against that hour's move, the more its return over the following 24 hours runs back toward that hour's direction.
Consequence: A trader would not hold the post-settlement fade past one day, and would take the opposite side on the second day after the largest reversals.
Why:
- F5: The hour-0 reversal partly gives itself back on the following day. For hour-0 moves of 2 to 3 usual moves, the second day's signed return is -0.53 % (t -3.21, 1012 cases) after +0.67 % on the first day. The 48-hour signed mean is only +0.16 % (t 0.67).
