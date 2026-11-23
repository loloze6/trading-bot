---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation
line: 7.c rejected
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.g3_quiet-market-hourly-breakout-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 1-hour return relative to its 24-hour volatility, the more its return over the next 4 hours runs in the opposite direction, the more so the higher its 24-hour volatility relative to its 30-day volatility.
Consequence: A trader would refuse to chase a large hourly move made in rising volatility, and expect part of it back within hours.
Why:
- F3: The reversal grows with the volatility ratio. Over 24 hours, only the top ratio quintile (1.17 to 4.84) carries it, with slope -34.2 bp and t -3.03 on 2585 cases, while the other four quintiles sit between -5.8 and +4.0 bp with |t| < 0.7. Over 4 hours the slope runs steadily from +2.9 bp (t 2.42) in the lowest quintile to -9.3 bp (t -4.42) in the highest.
- F4: The reversal outside the quiet regime is present at every horizon of a day or less: the slope t is -10.8 at 1 hour (198226 cases), -7.26 at 4 hours (49536), -3.80 at 12 hours (16458) and -5.23 at 24 hours. It fades at 48 hours (t -0.44 on 3966 cases).
