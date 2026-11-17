---
line: 7.d not profitable
backtest: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month_1d
idea tested: 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3357 USD
---
## Findings
- **F1:** The book's gain comes only from the top fifth of its forecasts. Trending bars in forecast quintile 4 (mean forecast 8.3, allocation 0.48) earn 0.00223 per bar. Quintiles 0 to 2 earn between -0.00008 and 0.00013, although their next-day coin return rises from 0.00006 to 0.0018.
- **F2:** The short side, which comes from "far below the high" turning the forecast negative, adds nothing. Short bars inside the trending regime number 3502 and earn a mean of 0.00000016 per bar. Over all short bars, the gain summed to -0.107: the coin's own rise cost -0.797 and timing returned only +0.690. Long bars summed +4.96, of which 1.71 was the rise and 3.25 was timing.
- **F3:** The book is lightly invested, so its mean daily return is only 0.000251 against the coins' 0.00123. Its mean allocation is 0.28 on long bars and the regime is "unknown" (mostly flat) on 8503 of 17044 bars. Pooled over windows, the deepest fall of its chain is -14.4%.
- **F4:** The falls come when the coin's recent move has faded, and in calmer markets.
- **F5:** Among long bars, the gain is graded by the coin's own past 7-day return.
- **F6:** Nearness to the high does predict 7-day excess returns inside the regime, with slope 0.00037, t 2.15 and 1013 non-overlapping cases. The top nearness fifth returns 3.2% over 7 days against about 0.9% in the farthest two fifths.
- **F7:** The nearness effect weakens in the most volatile tercile of 20-day volatility.

## Ideas
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week` (from F1, F4, F5, F6): The closer a coin's daily close sits to its highest close of the past 52 weeks, the higher its return over the next 7 days, only while its 30-day return is positive. Inside that state, the higher the 30-day return and the higher its 7-day return, the larger the gain.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side` (from F2, F3, F6): The closer a coin's daily close sits to its highest close of the past 52 weeks, the higher its return over the next 7 days, only while its 30-day return is positive. Inside that state, the higher the 30-day return the larger the gain, and the gain is larger the further its close sits above its lowest close of the past 52 weeks, so a coin far below its high earns little rather than falling.
- `013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d3_nearness-strongest-when-calm` (from F6, F7): The closer a coin's daily close sits to its highest close of the past 52 weeks, the higher its return over the next 7 days, only while its 30-day return is positive. Inside that state, the higher the 30-day return the larger the gain, and the calmer its daily moves over the past 20 days relative to its past year, the stronger this link.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
