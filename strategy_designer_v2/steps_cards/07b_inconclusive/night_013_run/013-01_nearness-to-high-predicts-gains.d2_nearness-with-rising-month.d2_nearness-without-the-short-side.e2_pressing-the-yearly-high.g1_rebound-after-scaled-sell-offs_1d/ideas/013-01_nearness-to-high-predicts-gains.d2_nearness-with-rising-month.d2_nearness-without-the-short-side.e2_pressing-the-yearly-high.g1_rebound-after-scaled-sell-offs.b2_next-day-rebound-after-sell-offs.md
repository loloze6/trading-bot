---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high.g1_rebound-after-scaled-sell-offs
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e2_pressing-the-yearly-high.g1_rebound-after-scaled-sell-offs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall measured in units of its own 30-day daily volatility, the larger its rebound over the next 1 day.
Consequence: A trader would buy a coin's sharp volatility-scaled sell-off for the next day only, sized with the depth of the fall, and not count on the bounce lasting several days.
Why:
- F2: The effect is clear at short horizons and fades with the horizon: on the pooled non-overlapping grids the slope t is 6.43 at 1 day (n 17,380), 2.94 at 2 days (n 8,650), 0.90 at 3 days (n 5,723), -0.29 at 5 days (n 3,419) and -1.69 at 7 days (n 2,443), so the plan's 3-day horizon reads the rebound after most of it has already happened.
- F3: At 1 day the rebound is graded and sits in the largest falls: among forecast-positive bars the two top forecast quintiles have mean excess returns of +0.0037 (t 3.05, n 1,703) and +0.0057 (t 4.39, n 1,703), while the three lower quintiles range from -0.0011 to +0.0001.
- F4: The 1-day effect is broad. Its slope is positive in all 6 coins (t from 1.32 for BTC to 5.55 for XMR) and in both window halves (t 4.77 in w1–12, 4.41 in w13–24). It is positive in every year from 2018 to 2023 (t 1.21 to 4.03) and fades in 2024 (t 0.72) and 2025 (t -0.53).
