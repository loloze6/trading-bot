---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The higher a coin's traded volume over the past day relative to its average over the past 20 days, the higher its return over the next 7 days, only on a day the coin closed higher than the day before.
Consequence: A heavy-volume up day would favour holding the coin long over the next week, more so the heavier the volume, while a thin-volume up day would give no such reason.
Why:
- F3: The plain effect sits mostly at the extremes of the forecast: the thinnest-volume quintile averages -0.87% excess 7-day return and the heaviest +0.58%, while the middle three quintiles lie between -0.04% and +0.31%.
- F4: The effect shows on up days and is mixed on down days: on bars that closed up the slope t is 2.19 (n = 1215), and terciles of relative volume give -0.47%, +0.94% and +1.65% excess 7-day return, while on down days t is 1.36 (n = 1084) and the terciles are non-monotone (-2.01%, +0.22%, -0.92%).
