---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: At the 13:00 UTC close, the larger a coin's 24-hour return, the more its return over the next 3 hours runs in the opposite direction.
Consequence: A trader would fade a coin's 24-hour run for the 3 hours after 13:00 UTC, more so the stronger the run, and refuse to chase it at that hour.
Why:
- F4: At the 13:00 UTC close, the return over the next 1 and 3 hours runs against the coin's 24-hour return, graded by its size. The slope t is -11.6 for 1 hour and -10.96 for 3 hours (17263 cases, one per coin-day). In the top quartile of |24h trend z|, the trend-signed 3-hour unusual move is -0.20 % (t -4.45). The 3-hour slope is negative in 7 of 8 years (t ≤ -2 in 2018 and 2021–2025) and in 5 of 6 coins (XMR t -9.7, ZEC -6.7, LTC -4.2, BTC -3.7, ETH -2.9; XRP +0.15).
