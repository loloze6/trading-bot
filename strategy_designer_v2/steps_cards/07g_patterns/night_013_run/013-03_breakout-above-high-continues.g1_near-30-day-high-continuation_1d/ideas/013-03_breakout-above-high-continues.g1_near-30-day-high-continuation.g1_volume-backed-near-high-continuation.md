---
brief: 013_anchoring-to-recent-high
source-idea: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation
line: 7.g patterns
backtest: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes near the highest high of its prior 30 days, the heavier its traded volume over the last 5 days relative to its 30-day average, the larger its return over the next 10 days.
Consequence: A trader would favour longs on coins pressing their 30-day high on swelling volume and refuse those approaching it on thin volume.
Why:
- F2: Among near-high samples (top 40 % of distance per coin), heavy recent volume carries the follow-through. With 5-day volume over 30-day volume in its top tercile, the excess 10-day return is +0.042 (t 2.77, n 168), against −0.006 and −0.007 in the lower terciles. The high-minus-low Welch t is 2.47, and the slope on log relative volume has t 3.80.
- F3: The near-high volume gap has the same sign in all six coins (high minus low: BTC +0.030, ETH +0.018, LTC +0.016, XMR +0.077, XRP +0.062, ZEC +0.085). In coins far below the high it reverses (low-volume tercile +0.008, high −0.020). The gap is concentrated in windows w13–w24 (+0.076 vs −0.033); in w1–w12 it is +0.006 vs +0.012.
- F1: The 10-day edge sits only in the closest-to-high quintile. On non-overlapping 10-day samples, the excess return by distance-to-30-day-high quintile is −0.010, −0.0075, −0.0014 and −0.0108 for q0 to q3 (none with |t| above 1.3), against +0.030 (t 2.48, n 252) for the top quintile (mean distance −1.4 %). Per-coin slopes are significant only for XRP (t 2.60) and ZEC (t 2.46); BTC, LTC and XMR have slopes at or below 0.
