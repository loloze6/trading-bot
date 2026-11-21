---
line: 7.g patterns
backtest: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines_1d
idea tested: 022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3974 USD
---
## Findings
- **F1:** When the coin's 90-day return is positive (the "unknown" regime), a day's return scaled by its 20-day volatility predicts the next 5 days. The slope is +0.097 usual moves per standard deviation (t 3.78, 1624 independent 5-day cases) and is positive on all 6 coins. It holds in both halves of the windows: t 2.32 on w1-w12 (716 cases) and t 3.05 on w13-w24 (908).
- **F2:** That effect comes from strong up days. The top quintile of scaled day returns (mean +1.54 volatility units) is followed by an unusual move of +2.68 % over 5 days (total +3.26 %, t 3.96, 326 cases), which is 14 times the 0.19 % cost of a trade. Among positive days alone the slope is +0.216 usual moves per unit (t 4.41, 824 cases), while the four lower quintiles show no slope (t -0.63). Its strength by year is uneven: t 4.63 in 2019, between -0.56 and 1.43 in the other years.
- **F3:** In the same rising regime, nearness to the 20-day high predicts the next 5 days on all 6 coins: slope +0.094 usual moves per standard deviation, t 3.66, 1624 cases. The top quintile is followed by +0.096 usual moves (+1.70 % total). Read together with the scaled day return (correlation 0.29), both keep their own weight (t 2.87 and t 2.79).
- **F4:** The tested rebound is absent. In the falling regime (90-day return negative), the slope on depth below the 90-day high is t 0.79 over 1652 cases. The unusual move per case is -0.44 % (-0.050 of a usual move), and the total move of +0.13 % is 0.7 times the 0.19 % cost. Short-horizon continuation measures in this regime lean negative instead: 20-day return t -1.84, nearness to the 20-day high t -1.76, each with 1 or 2 of 6 coins positive.
- **F5:** The book earned 2.8 bps a day on average across the 24 windows, against 12.0 bps for holding the coins. It lagged holding in 7 of 8 years (for example 5.1 against 40.9 bps in 2021), was in a position on 56 % of bars, and held 0.54 of the book on average when in.
- **F6:** Two other patterns did not hold up as findings:

## Ideas
- `022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines.g1_strong-up-day-continuation-uptrend` (from F1, F2, F4): While a coin's 90-day return is positive, the larger its 1-day rise measured against its typical daily move over the past 20 days, the higher its return over the next 5 days.
- `022-02_combination-beats-best-single.d1_combination-only-in-downtrends.d3_rebound-after-deep-declines.g2_near-20-day-high-uptrend` (from F3, F4): While a coin's 90-day return is positive, the closer its close stands to its highest close of the past 20 days, the higher its return over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
