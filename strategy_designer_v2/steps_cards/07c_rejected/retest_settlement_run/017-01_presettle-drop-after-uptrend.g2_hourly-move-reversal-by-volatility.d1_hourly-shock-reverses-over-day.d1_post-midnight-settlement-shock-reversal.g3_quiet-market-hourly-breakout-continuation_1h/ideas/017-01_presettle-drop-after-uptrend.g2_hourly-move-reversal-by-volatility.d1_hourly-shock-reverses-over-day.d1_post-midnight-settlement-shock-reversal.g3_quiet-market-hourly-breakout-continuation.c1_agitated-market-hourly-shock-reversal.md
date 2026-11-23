---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation
line: 7.c rejected
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's 24-hour volatility is high relative to its 30-day volatility, the larger its 1-hour return relative to its 24-hour volatility, the more its return over the next 24 hours runs in the opposite direction, and the more so the higher that volatility ratio.
Consequence: A trader would fade, not follow, an outsized hourly move made while the market is already agitated, and hold the fade for a day, because the give-back is larger than the cost of a trade.
Why:
- F2: Outside the quiet regime, where 24-hour volatility is at or above 30-day volatility, the hour's move clearly reverses over the next 24 hours: the slope is -28.9 bp per unit with t -5.23 on 8219 cases, and the signed unusual move is -0.313 % with t -5.11, which is about 1.6 times the 0.19 % cost of a trade.
- F3: The reversal grows with the volatility ratio. Over 24 hours, only the top ratio quintile (1.17 to 4.84) carries it, with slope -34.2 bp and t -3.03 on 2585 cases, while the other four quintiles sit between -5.8 and +4.0 bp with |t| < 0.7. Over 4 hours the slope runs steadily from +2.9 bp (t 2.42) in the lowest quintile to -9.3 bp (t -4.42) in the highest.
- F4: The reversal outside the quiet regime is present at every horizon of a day or less: the slope t is -10.8 at 1 hour (198226 cases), -7.26 at 4 hours (49536), -3.80 at 12 hours (16458) and -5.23 at 24 hours. It fades at 48 hours (t -0.44 on 3966 cases).
- F5: Outside the quiet regime the reversal grows with the size of the hour's move. The signed 24-hour unusual move is -0.14 % (t -1.51) for |z| ≤ 0.5, -0.33 % (t -2.87) for 0.5 to 1, -0.64 % (t -4.31) for 1 to 1.5, and -0.93 % (t -3.22) for 2 to 3.
- F6: Over all bars, the 24-hour slope is negative in every coin, strongest in ZEC (-31.4 bp, t -2.73) and XRP (-22.7 bp, t -2.41), with BTC, LTC and XMR at t -1.46 to -1.90 and ETH near zero (t -0.06).
