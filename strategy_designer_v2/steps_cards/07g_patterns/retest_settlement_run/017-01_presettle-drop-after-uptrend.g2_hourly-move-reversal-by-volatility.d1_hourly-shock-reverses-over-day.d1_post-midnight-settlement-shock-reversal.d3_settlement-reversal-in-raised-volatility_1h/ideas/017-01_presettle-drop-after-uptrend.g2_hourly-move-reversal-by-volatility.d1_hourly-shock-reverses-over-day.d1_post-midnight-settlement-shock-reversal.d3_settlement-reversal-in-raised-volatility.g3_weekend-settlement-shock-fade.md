---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility
line: 7.g patterns
backtest: 017-01_presettle-drop-after-uptrend.g2_hourly-move-reversal-by-volatility.d1_hourly-shock-reverses-over-day.d1_post-midnight-settlement-shock-reversal.d3_settlement-reversal-in-raised-volatility_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's 1-hour return relative to its 24-hour volatility in the first hour after the 00:00 UTC settlement on Saturdays and Sundays, the more its return over the next 24 hours runs the opposite way.
Consequence: A trader would weight the post-settlement fade toward weekends, when thinner books leave the settlement move more to give back.
Why:
- F5: The settlement-hour reversal is larger on weekends: −37.9 bp per unit (t −6.8, 4833 cases) against −22.5 (t −5.5, 12111) on weekdays, with Saturday the strongest (−49.1, t −5.8). It is also larger when that hour's volume is low against its week: −34.3 (t −4.9) in the lowest volume tercile against −21.6 (t −4.4) in the highest. The weekend gap is about t 2.2, which is marginal after this many angles.
- F6: The volatility-ratio grading holds across quintiles at hour 0: the slope runs from −5.8 bp (t −0.8) at a ratio of 0.52 to −44.3 bp (t −4.5) at 1.59. Hours 6, 12 and 18 show no such grading (|t| ≤ 1.3).
