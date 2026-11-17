---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through
line: 7.g patterns
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The wider a coin's daily high-low range relative to its own average range over the past 20 days, the higher its return over the next 3 days.
Consequence: A day of unusually wide range is a reason to lean long for the following few days, and an unusually narrow day is a reason to refuse a new long.
Why:
- F1: Across all six coins, a wider daily range relative to its own 20-day average range comes before a higher demeaned 3-day return (slope 0.0056, t = 3.02, n = 4715 non-overlapping cases); the slope is positive in 5 of 6 coins (ZEC t = 2.39, XRP t = 1.72, BTC the only negative at t = -0.35), but it fades at 7 days (slope 0.0032, t = 0.63, n = 2011).
- F2: The tested volume effect is confined to rising months: the volume-ratio slope on the demeaned 3-day return is 0.0076 (t = 3.15, n = 2187) when the 30-day return is positive, against 0.0012 (t = 0.53, n = 2096) when it is not, and the top volume quintile in rising months carries +1.29% (t = 2.63, n = 439).
