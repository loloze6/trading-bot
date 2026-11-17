---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g3_strong-day-follow-through-in-uptrends.g1_down-day-rebound-in-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall relative to its 30-day daily volatility, multiplied by how far that day's volume stands above its 30-day average volume, the higher the coin's return over the next 1 day.
Consequence: A sharp fall on heavy volume is a reason to buy for the next day, not to sell.
Why:
- F2: On down days, the heavier the volume against its 30-day average, the higher the next day's excess return. The top volume-surprise quartile of down days returns +0.0068 (t 4.85, n 1573), while the other three quartiles return -0.0004 to +0.0006. The slope on log volume surprise is positive in all six coins (0.0019 to 0.0057) and in both halves (t 2.50 and 3.71). In a joint regression the fall × volume term carries the effect (t 2.93), while the fall alone (t 1.09) and the volume alone (t 0.55) do not; on up days the volume slope has no consistent sign (-0.0040 to +0.0048).
