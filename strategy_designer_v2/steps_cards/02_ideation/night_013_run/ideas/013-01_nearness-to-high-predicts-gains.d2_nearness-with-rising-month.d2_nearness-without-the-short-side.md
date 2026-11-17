---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits to its highest close of the past 52 weeks, the higher its return over the next 7 days, only while its 30-day return is positive. Inside that state, the higher the 30-day return the larger the gain, and the gain is larger the further its close sits above its lowest close of the past 52 weeks, so a coin far below its high earns little rather than falling.
Consequence: Treat distance below the high as a reason to stand aside, not to sell short. That removes short positions that cost the market's rise and earned no timing.
Why:
- F2: The short side, which comes from "far below the high" turning the forecast negative, adds nothing. Short bars inside the trending regime number 3502 and earn a mean of 0.00000016 per bar. Over all short bars, the gain summed to -0.107: the coin's own rise cost -0.797 and timing returned only +0.690. Long bars summed +4.96, of which 1.71 was the rise and 3.25 was timing.
- F3: The book is lightly invested, so its mean daily return is only 0.000251 against the coins' 0.00123. Its mean allocation is 0.28 on long bars and the regime is "unknown" (mostly flat) on 8503 of 17044 bars. Pooled over windows, the deepest fall of its chain is -14.4%.
- F6: Nearness to the high does predict 7-day excess returns inside the regime, with slope 0.00037, t 2.15 and 1013 non-overlapping cases. The top nearness fifth returns 3.2% over 7 days against about 0.9% in the farthest two fifths.
