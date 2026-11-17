---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.g1_deep-drawdown-rebound-in-downtrends.g2_volume-surge-precedes-gains_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's traded volume over the past day relative to its average over the past 20 days, taken with the sign of that day's return, the higher its return over the next 7 days.
Consequence: A trader would lean long a coin after a heavy-volume rise and away from it after a heavy-volume fall, in proportion to how unusual the day's volume was.
Why:
- F4: The effect shows on up days and is mixed on down days: on bars that closed up the slope t is 2.19 (n = 1215), and terciles of relative volume give -0.47%, +0.94% and +1.65% excess 7-day return, while on down days t is 1.36 (n = 1084) and the terciles are non-monotone (-2.01%, +0.22%, -0.92%).
- F5: Relative volume signed by the day's direction predicts more clearly than relative volume alone: its 7-day slope t is 2.94 (n = 2299) and its 14-day t is 3.33 (n = 1008), it is positive in all 6 coins at 7 days (t 0.11 to 2.08) and in 7 of 8 years, and its sextiles rise from -0.83% to +1.76% excess 7-day return.
