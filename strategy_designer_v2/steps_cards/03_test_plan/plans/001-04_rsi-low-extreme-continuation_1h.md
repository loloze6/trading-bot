---
idea: 001-04_rsi-low-extreme-continuation
brief: 001_rsi-extremes-predict-next-move
data-instruments: BTC, ETH, BNB
data-bar: 1h
data-period: fold A
---
Forecast: Short-only RSI continuation. Take the 14-bar Wilder RSI of the 1h closes. When RSI is below 50, the forecast is negative and proportional to (50 − RSI). That value is divided by the mean absolute value of its previous 60 stored values, times 10, and capped at −20. It is zero whenever RSI is 50 or above. The deeper the RSI sits below 50, the larger the short, so the biggest shorts come at the lowest readings. The forecast is never positive.
Config: 001-04_rsi-low-extreme-continuation_1h_config.json
Confirm: The test uses one horizon, 24 bars, sampled on non-overlapping blocks of 24 bars. Each 24-bar forward return of the coin is taken minus that coin-window's mean 24-bar return, so that holding the coin is the baseline. Two groups are compared: - extreme bars: the 10% of bars with the most negative forecast (lowest RSI); - neutral bars: bars where the recorded RSI is between 40 and 60. The idea is confirmed if the mean excess return of the extreme group, minus that of the neutral group, is negative with t ≤ −2 pooled over all coins and windows, and is negative in at least 2 of the 3 coins. Supporting check: the pre-cost portfolio return is positive in at least 11 of the 18 coin-windows.
Reject: The idea is rejected if the pooled extreme-minus-neutral difference in 24-bar excess return is zero or positive. If that difference is positive with t ≥ 2, the result is evidence of reversal, the opposite of the idea.
Inconclusive: The difference is negative but with t between −2 and 0. Or it is negative pooled but negative in fewer than 2 of the 3 coins. Or the main measure confirms but the supporting check fails (fewer than 11 of 18 coin-windows positive).
Deviation: The idea says "after RSI reaches a low extreme". The config tests "while RSI is below 50, sized by how far below". The short starts at any reading under 50, not only at extremes, and its size is measured against the last 60 bars rather than a fixed RSI level. High readings get no long position, because the idea is only about the downside. The comparison of extreme against neutral readings is made in the criterion, not in the forecast.
