---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is positive, the higher its 7-day return, the higher its return over the next 7 days.
Consequence: In a rising month, weight long exposure by the past week's rise, which carries the predictive content that closeness to the high does not.
Why:
- F2: In the trending regime the gain sits almost entirely in the top forecast fifth (next-bar coin return 0.0056, gain 0.0035 per bar, mean position 0.60), while the bottom fifth holds a mean short of -0.25 as the coin still rises 0.0007 per bar and earns only 0.0001, and the middle fifths earn between -0.00003 and 0.0006.
- F3: On the non-overlapping 7-day grid in the trending regime (888 cases), the coin's 7-day return predicts its excess 7-day return with t 4.09 and the 30-day return with t 2.10, but closeness to the 52-week high gives only t 0.59, and its fifths do not rank the gain (excess 0.0064, -0.0175, 0.0355, 0.0163, 0.0095 from farthest to nearest).
