---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's 3-day rise relative to its own 20-day daily volatility, the higher its return over the next 3 days.
Consequence: A strong 3-day advance, scaled by the coin's volatility, is a reason to hold or add to a long over the following 3 days.
Why:
- F5: A 3-day rise continues and a 3-day fall does not reverse. On the non-overlapping 3-day grid, the slope of the demeaned next-3-day return on the volatility-scaled 3-day rise is 0.0070 (t 2.89, n 2356). For 3-day falls it is −0.0013 (t −0.46, n 2359).
- F6: The rising-month momentum holds at every volatility level. The r7 slope is t 2.48 in the low tercile, t 1.43 in the middle and t 3.18 in the high tercile (about 297 cases each). Scaling r7 by volatility gives t 3.61, so the effect is not a volatility artefact.
