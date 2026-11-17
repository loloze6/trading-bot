---
brief: 013_anchoring-to-recent-high
source-idea: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The more negative a coin's 30-day return, the lower its return over the next 3 days, only while the coin's 90-day return is positive.
Consequence: A coin dropping through its month inside a rising quarter is a reason to refuse a long over the next few days, more firmly the deeper the month's fall, while a month's fall inside a falling quarter is no such reason.
Why:
- F1: The book loses because it is short most of the time against coins that rise on average. Its mean daily return of -0.000193 splits into -0.000270 from the market's own rise (mean position -0.228, short on 61% of days), +0.000136 from timing and -0.000060 from fees, so the timing gain is too small to cover the short's cost against the drift.
- F3: The short side works only while the coin's 90-day return is positive. In those active cases the excess 3-day return is -0.0122 (t -2.60, n=209), against +0.0006 (t 0.18, n=462) when the 90-day return is negative.
- F4: The book's bars show the same split. When the 90-day return is up, the held short earns +0.000717 per bar (Sharpe 1.10, n=1029); when it is down, the short loses -0.000480 per bar (Sharpe -0.36, n=1796).
- F5: Inside the rising-quarter state the effect is graded. The deeper half of 30-day falls is followed by -0.0196 excess 3-day return (t -2.04, n=43), against -0.0102 (t -1.92, n=166) for the shallower half.
- F6: Across 90-day return quartiles of the active cases, the follow-up falls as the quarter rises. The deepest quarterly falls (mean -0.51) are followed by +0.0084, while the top two quartiles (mean -0.07 and +0.58) show -0.0102 (t -2.17) and -0.0107 (t -2.03).
- F8: The book earned only in falling years, 2018 (+0.000839 per day) and 2022 (+0.000170). It lost in rising years such as 2020 (-0.000547), 2023 (-0.000883) and 2024 (-0.000696), and its trades lose -0.85% each after fees, with 39% winners.
