---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high.g1_rebound-after-scaled-sell-offs
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high.g1_rebound-after-scaled-sell-offs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall measured in units of its own 30-day daily volatility, the larger its rebound over the next 3 days, only while the coin's 30-day daily volatility is high compared with its own past.
Consequence: A trader would buy scaled sell-offs mainly when the coin is in a turbulent phase, and give less weight to the same signal in calm periods.
Why:
- F5: At 3 days the signal is drowned by noise. The standard deviation of the excess return is 0.088 against a mean of 0.00065, the forecast quintiles go up and down with no order (-0.0051 to +0.0051), coin t's range from -0.59 to 1.51, and year t's from -1.70 to 2.69.
- F6: The effect is concentrated in high-volatility conditions. In each coin's top 30-day-volatility tercile the slope t is 5.89 at 1 day and 2.40 at 3 days (forecast-positive mean excess +0.0070). In the bottom tercile it is 0.29 at 1 day and -0.95 at 3 days.
