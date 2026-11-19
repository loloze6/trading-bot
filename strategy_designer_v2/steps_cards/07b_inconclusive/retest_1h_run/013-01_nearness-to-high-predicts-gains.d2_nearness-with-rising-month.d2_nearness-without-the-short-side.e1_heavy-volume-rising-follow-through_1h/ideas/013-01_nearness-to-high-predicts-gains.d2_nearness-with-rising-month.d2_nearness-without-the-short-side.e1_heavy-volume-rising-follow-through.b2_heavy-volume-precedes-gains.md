---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The higher a coin's daily volume relative to its own 20-day average volume, the higher its return over the next 3 days, whether its 30-day return is rising or falling.
Consequence: Unusually heavy volume in a coin is a reason to lean long for the next few days, and unusually thin volume is a reason to refuse a long, in any month.
Why:
- F3: The plan's forecast throws away part of the signal: within positive forecasts the 72-hour slope is flat (+0.000015, t 0.04, n 1,190), yet the raw volume ratio predicts the 72-hour excess return with t 2.80 (n 2,837), and its quintiles rise in order (-0.0013, -0.0001, +0.0019, +0.0082, +0.0088), so the standardise-and-clip step dilutes a graded effect.
- F5: The rising-month condition is not where the effect lives: the price-recomputed volume ratio predicts the 72-hour excess return about as well on non-trending grid cases (slope 0.0062, t 2.91, n 2,305) as the raw ratio does on trending ones (slope 0.0068, t 2.80), and at 24 hours it also holds off-regime (t 2.70, n 7,120).
