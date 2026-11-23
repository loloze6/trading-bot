---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d2_convex-post-settlement-shock-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more a coin's first hour after the 00:00 UTC settlement extends its prior 24-hour run in the same direction, measured as that hour's move times the prior 24-hour return, the more its next 24 hours run against both.
Consequence: A trader would fade the post-settlement hour mainly when it pushes the day's crowded run further, and refuse to fade it when it moves against that run.
Why:
- F2: At 00:00 the reversal is graded by how far that hour extends the prior 24-hour run in the same direction. By quintile of (sign of the hour's move × prior 24-hour return), the top quintile fades +0.772 % (t 7.27, n 3391) against +0.104 % (t 1.06) in the bottom quintile. Hours moving with the prior day fade +0.403 % (t 7.48, n 9308) against +0.170 % (t 3.15, n 7788) for hours against it.
- F1: The 00:00 UTC hour's move is faded over the next 24 hours far more than any other hour's: the faded 24-hour return in excess of drift is +0.297 % (t 7.76, 17096 daily cases). No other hour reaches t 2.6: the largest is hour 22 at +0.093 % (t 2.54), and hour 3 goes the other way at −0.114 % (t −3.00). The effect is tied to the settlement clock, not to hourly moves in general.
