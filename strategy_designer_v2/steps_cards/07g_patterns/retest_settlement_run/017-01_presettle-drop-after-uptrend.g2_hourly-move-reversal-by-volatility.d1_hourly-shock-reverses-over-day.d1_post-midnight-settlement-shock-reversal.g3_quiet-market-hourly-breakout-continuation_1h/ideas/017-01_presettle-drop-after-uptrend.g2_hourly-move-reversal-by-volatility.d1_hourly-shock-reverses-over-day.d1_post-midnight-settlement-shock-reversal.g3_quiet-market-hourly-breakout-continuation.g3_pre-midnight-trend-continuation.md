---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: At the 23:00 UTC close, the larger a coin's 24-hour return, the more its return over the next 3 hours continues in the same direction.
Consequence: A trader would ride a coin's 24-hour run through the 00:00 UTC settlement hours, more so the stronger the run, and refuse to fade it then.
Why:
- F5: At the 23:00 UTC close, the hour before the 00:00 funding settlement, the next 1 and 3 hours continue the coin's 24-hour return, graded by its size. This is the opposite of the brief's pre-settlement lean. The slope t is +10.1 for 1 hour (17215 cases) and +7.75 for 3 hours (17073 cases). By |trend z| quartile, the trend-signed 3-hour unusual move rises 0.02 %, 0.05 %, 0.06 %, 0.17 %, with t 0.87, 2.02, 2.51, 4.05. The 3-hour slope is positive in all 6 coins (BTC t 5.6), but it is concentrated in 2018–2020 (t 3.4, 3.3, 8.6); 2021–2025 range from t -1.7 to 1.6.
