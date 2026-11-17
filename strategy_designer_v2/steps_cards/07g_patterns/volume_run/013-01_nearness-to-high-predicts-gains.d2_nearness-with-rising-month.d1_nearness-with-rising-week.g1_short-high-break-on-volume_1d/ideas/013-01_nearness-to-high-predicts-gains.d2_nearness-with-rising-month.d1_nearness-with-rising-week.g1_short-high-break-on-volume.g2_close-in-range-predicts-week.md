---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's daily close sits within that day's high-low range, the higher the coin's return over the next 7 days.
Consequence: Favour longs in coins closing at the top of their daily range, and distrust coins closing at the bottom of it.
Why:
- F3: Where the close sits inside the day's range also predicts the next 7 days. The slope t of 7-day excess return on (close - low)/(high - low) is 2.94 (n 2443).
- F2: At the 7-day horizon, the last day's own move predicts as well as the idea's forecast. Over non-overlapping 7-day samples, the slope t on 7-day excess return is 3.45 for the 1-day return (n 2299) and 3.22 for the vol-scaled 1-day return (n 2011), against 4.17 for the forecast and 2.55 for distance to the high. In a joint regression on 1723 samples, none of distance (t 1.54), volume ratio (t 1.40) or the vol-scaled day (t 1.67) stands out on its own.
