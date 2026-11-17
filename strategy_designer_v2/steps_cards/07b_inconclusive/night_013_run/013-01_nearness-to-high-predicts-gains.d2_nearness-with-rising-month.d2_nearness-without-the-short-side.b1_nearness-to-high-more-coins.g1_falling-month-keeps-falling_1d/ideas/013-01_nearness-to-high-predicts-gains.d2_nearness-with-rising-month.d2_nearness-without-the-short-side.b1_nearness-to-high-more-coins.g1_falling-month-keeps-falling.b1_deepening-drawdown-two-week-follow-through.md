---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g1_falling-month-keeps-falling
line: 7.b inconclusive
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.b1_nearness-to-high-more-coins.g1_falling-month-keeps-falling_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's 30-day return is negative, the further its close sits below its 60-day high compared with how far below that high it has sat over the past 60 days, the lower its return over the next 14 days relative to its own average.
Consequence: A coin in a falling month whose slide below its recent high has deepened beyond its usual recent drawdown is a candidate for a two-week short or a reduced long, rather than a one-week trade.
Why:
- F1: The test's main measure is on the side the idea predicts but far too small for its size: the pooled slope of the 7-day excess return on the forecast is +0.00045 with t 0.86 over 2655 falling-month grid cases. The test already used every coin and every fold available, so there is no more data to run it on.
- F2: The raw depth below the 60-day high does not carry the effect at any horizon, and at 7 days it leans the wrong way. Its 7-day slope is -0.00026 (t -1.53, n 2655), so a deeper close gave a slightly higher return. Its 14-day slope is -0.00019 (t -0.53, n 1221) and its 30-day slope is +0.0003 (t 0.32, n 591).
- F4: The effect shows at a longer horizon than the plan's 7 days. On non-overlapping grids, the forecast slope is t 2.43 at 14 days (n 1221) and t 2.17 at 21 days (n 812), against t 0.86 at 7 days and t -0.06 at 30 days. At 14 days it rises to t 3.28 once the 30-day return is held alongside it (the 30-day return's own t is -2.01).
- F5: The 14-day effect leans on a few years and is thin per coin. It is strong in 2020 (t 3.12, n 81) and 2022 (t 4.15, n 236), negative in 2023 (t -1.73, n 184) and near zero in the other years. 74% of 19 coins have a positive slope, but the median coin's t is only 0.39.
