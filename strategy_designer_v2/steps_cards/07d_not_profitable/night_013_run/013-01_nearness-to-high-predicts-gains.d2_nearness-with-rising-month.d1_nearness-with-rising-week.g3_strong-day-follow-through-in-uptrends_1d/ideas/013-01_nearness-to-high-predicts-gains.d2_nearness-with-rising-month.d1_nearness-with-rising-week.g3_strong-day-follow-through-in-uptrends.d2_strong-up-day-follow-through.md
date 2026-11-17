---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, the larger its latest one-day gain relative to its 30-day daily volatility, the higher its return over the next 7 days.
Consequence: In an up-month, add after unusually strong up days, and treat down days as no reason to short a coin that keeps drifting up.
Why:
- F3: Over the 1 day the book actually holds, the forecast points the wrong way: on trending non-overlapping 1-day cases the slope is -0.000052 (t -1.08, n 8624), and the next-day return is 0.0024 after negative forecasts against 0.0013 after positive ones; the edge appears only at 7 days (slope 0.00110, t 3.04, n 1215) and 14 days (slope 0.00162, t 1.94, n 585).
- F4: The short side carries the loss: short bars earn -0.00161 per bar (timing -0.00113, gain from the market's rise -0.00047), while long bars earn +0.00128 per bar (timing +0.00068); in up-months even the second-lowest forecast quintile is followed by a 7-day return of +0.019.
