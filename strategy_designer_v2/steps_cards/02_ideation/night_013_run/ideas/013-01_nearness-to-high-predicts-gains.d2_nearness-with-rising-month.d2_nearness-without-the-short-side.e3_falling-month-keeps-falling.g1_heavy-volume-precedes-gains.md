---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The heavier a coin's day volume relative to its own 30-day average volume, the higher its return over the next 3 days.
Consequence: A day of unusually heavy volume in a coin is a reason to favour a long over the next few days, more firmly the heavier the volume.
Why:
- F1: The coin's day volume relative to its own 30-day mean volume carries the clearest pattern in the bars. In the top quintile, the excess 3-day return over the coin's mean is +0.0083 (t 2.83, 1061 non-overlapping cases), against -0.0030 to +0.0009 in the four lower quintiles. The top two deciles are +0.0069 and +0.0097, but the lower deciles do not rise in order: decile 0 is +0.0028 and decile 1 is -0.0089.
- F2: The volume effect holds up under checks. In a pooled regression with nearness to the 30-day high and the 7-day return, relative volume keeps a t of 2.52 (near 0.77, 7-day return 1.27). The top quintile minus the rest is positive in 5 of 6 coins (BTC -0.0047 is the exception; XRP +0.019, ZEC +0.021), in 7 of 8 years (2018 -0.012 is the exception), and in both halves of the windows (w1-12 +0.012, t 2.99; w13-24 +0.009, t 1.85). Many angles were looked at, so it stands out only moderately.
