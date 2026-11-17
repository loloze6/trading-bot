---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The closer a coin's daily close sits to its highest close of the past 52 weeks, the higher its return over the next 7 days, only while its 30-day return is positive. Inside that state, the higher the 30-day return the larger the gain, and the calmer its daily moves over the past 20 days relative to its past year, the stronger this link.
Consequence: Trust the near-high signal most in calm markets and scale it down when daily swings are wide, where nearness carries little information.
Why:
- F6: Nearness to the high does predict 7-day excess returns inside the regime, with slope 0.00037, t 2.15 and 1013 non-overlapping cases. The top nearness fifth returns 3.2% over 7 days against about 0.9% in the farthest two fifths.
- F7: The nearness effect weakens in the most volatile tercile of 20-day volatility.
