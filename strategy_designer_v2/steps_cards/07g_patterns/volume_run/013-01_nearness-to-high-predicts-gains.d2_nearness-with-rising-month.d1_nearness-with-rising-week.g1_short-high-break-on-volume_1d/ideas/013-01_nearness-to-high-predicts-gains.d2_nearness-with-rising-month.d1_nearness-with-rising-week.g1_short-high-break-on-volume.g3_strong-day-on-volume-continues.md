---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g1_short-high-break-on-volume_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day rise relative to its own 30-day daily volatility, and the heavier that day's volume against its 30-day average, the higher the coin's return over the next 7 days.
Consequence: Favour week-long longs after a coin's strong vol-scaled up day on heavy volume, rather than waiting for it to near its recent high.
Why:
- F2: At the 7-day horizon, the last day's own move predicts as well as the idea's forecast. Over non-overlapping 7-day samples, the slope t on 7-day excess return is 3.45 for the 1-day return (n 2299) and 3.22 for the vol-scaled 1-day return (n 2011), against 4.17 for the forecast and 2.55 for distance to the high. In a joint regression on 1723 samples, none of distance (t 1.54), volume ratio (t 1.40) or the vol-scaled day (t 1.67) stands out on its own.
- F4: The gain concentrates in the top of the move. The top quintile of the vol-scaled day earns +1.81% 7-day excess (t 2.31, n 402); the other four quintiles lie between -0.87% and +0.10%. A strong up day on heavy volume earns +2.40% (n 264), against -0.82% for a down day on heavy volume (n 225).
