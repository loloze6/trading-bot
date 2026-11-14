---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While the 50-day SMA is above the 200-day SMA, price keeps drifting upward, except that the drift is largest soon after the cross while the spread is still narrow. The drift shrinks as the spread grows wide or jumps sharply.
Consequence: A trader would hold the most just after a fresh up-cross and scale down as the trend becomes extended, instead of adding into it.
Why:
- F4: Forecast size bought risk rather than edge. Allocation rose to 1.87 on average in the top forecast bucket (15–20). There the next-bar return was only 0.00155, against the coins' holding mean of 0.00129, while its standard deviation rose from 0.0486 to 0.0589.
- F5: The drift is strongest when the spread is smallest. Active bars in the lowest spread quintile returned 0.00273 per bar (t 2.99). The two highest quintiles returned 0.00084 (t 0.77) and 0.00144 (t 0.93).
- F6: The drift is also weak when the spread has already jumped. Active bars in the top quintile of 10-bar spread change returned 0.00048 (t 0.32). The middle quintile returned 0.00281 (t 2.62).
- F7: Across the book, active bars returned 0.00074–0.00155 per bar by forecast bucket. That is little above the coins' 0.00129 holding mean, which leaves a Sharpe 0.19 below holding's.
