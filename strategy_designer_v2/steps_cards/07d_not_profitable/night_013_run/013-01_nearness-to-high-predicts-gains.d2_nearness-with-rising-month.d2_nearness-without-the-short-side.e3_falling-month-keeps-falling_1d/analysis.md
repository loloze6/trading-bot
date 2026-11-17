---
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3157 USD
---
## Findings
- **F1:** The book loses because it is short most of the time against coins that rise on average. Its mean daily return of -0.000193 splits into -0.000270 from the market's own rise (mean position -0.228, short on 61% of days), +0.000136 from timing and -0.000060 from fees, so the timing gain is too small to cover the short's cost against the drift.
- **F2:** The 30-day fall is not graded the way the idea says, because the deepest falls rebound. Among forecast < 0 grid cases, the deepest forecast quintile (mean forecast -18.1, n=577) is followed by +0.0025 excess 3-day return, while the middle quintiles show -0.0069, -0.0048 and -0.0057, so the deep half beats the shallow half by +0.0016.
- **F3:** The short side works only while the coin's 90-day return is positive. In those active cases the excess 3-day return is -0.0122 (t -2.60, n=209), against +0.0006 (t 0.18, n=462) when the 90-day return is negative.
- **F4:** The book's bars show the same split. When the 90-day return is up, the held short earns +0.000717 per bar (Sharpe 1.10, n=1029); when it is down, the short loses -0.000480 per bar (Sharpe -0.36, n=1796).
- **F5:** Inside the rising-quarter state the effect is graded. The deeper half of 30-day falls is followed by -0.0196 excess 3-day return (t -2.04, n=43), against -0.0102 (t -1.92, n=166) for the shallower half.
- **F6:** Across 90-day return quartiles of the active cases, the follow-up falls as the quarter rises. The deepest quarterly falls (mean -0.51) are followed by +0.0084, while the top two quartiles (mean -0.07 and +0.58) show -0.0102 (t -2.17) and -0.0107 (t -2.03).
- **F7:** Measured as the 30-day return minus the 90-day return, the larger the month's shortfall against its quarter, the lower the next 3 days. The bottom quartile of that gap is followed by -0.0088, the next by -0.0083 (t -2.00), and the top quartile by +0.0074.
- **F8:** The book earned only in falling years, 2018 (+0.000839 per day) and 2022 (+0.000170). It lost in rising years such as 2020 (-0.000547), 2023 (-0.000883) and 2024 (-0.000696), and its trades lose -0.85% each after fees, with 39% winners.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.d1_falling-month-in-rising-quarter` (from F1, F3, F4, F5, F6, F8): The more negative a coin's 30-day return, the lower its return over the next 3 days, only while the coin's 90-day return is positive.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e3_falling-month-keeps-falling.d2_month-lagging-quarter-falls` (from F2, F6, F7): The further a coin's 30-day return falls below its 90-day return, the lower its return over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
