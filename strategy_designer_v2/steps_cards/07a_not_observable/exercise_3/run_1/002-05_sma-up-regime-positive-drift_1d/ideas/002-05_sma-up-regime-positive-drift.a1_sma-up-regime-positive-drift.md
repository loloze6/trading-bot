---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-05_sma-up-regime-positive-drift
line: 7.a not observable
backtest: 002-05_sma-up-regime-positive-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C and D
---
Idea: While a coin's 50-day simple moving average is above its 200-day simple moving average, its close-to-close return over the next 1 day is higher than on its other days, and the further the 50-day average stands above the 200-day average, the higher that next-day return.
Consequence: If confirmed, a trader would hold a coin long while its 50-day average stays above its 200-day average and lean in harder as the gap widens. If rejected, a trader would refuse long positions taken on that signal.
Why:
- F1: The test ran on one coin (BTCUSD) and one window (w1, 120 daily bars, year 2022). It found 13 in-stretch bars (forecast > 0), 107 out-of-stretch bars and 0 short bars, with 1 up-cross stretch, against the plan's minimum of 100 in-stretch bars, 100 out-of-stretch bars and 3 stretches.
- F2: The only stretch was already under way on the window's first bar (first positive-forecast bar at position 0) and lasted 13 bars, so the data held only the tail of one earlier upward cross and no new upward cross at all.
- F3: The situation was rare in this period because 2022 was a falling market for BTC: the recorded spread component sat mostly below zero (mean -56.5, min -92.0, max 50.3), with 107 of 120 bars (89%) below zero.
- F4: The outcome varies far more from day to day than the effect being sought: the next-day return's standard deviation is 0.0332, against an in-stretch mean of -0.0076 and an out-of-stretch mean of -0.0007. With 13 in-stretch cases the in-stretch mean's standard error is about 0.0092, which is larger than the difference itself (-0.0069, Welch t -0.95).
- F5: Even at the plan's minimum of 100 cases per side, a 0.0332 daily standard deviation means only a difference of about 0.009 per day or more would reach t = 2. Reaching the minimum counts is therefore a floor, and the test needs many more coin-windows than one.
- F6: The forecast uses a 200-day SMA standardised over its own past 200 values, so each window spends a long warm-up before recording. Only 120 bars were left in w1, which makes the idea's long-average situation long compared with the windows. A finer bar size would not help, because the warm-up is the same in real time.
