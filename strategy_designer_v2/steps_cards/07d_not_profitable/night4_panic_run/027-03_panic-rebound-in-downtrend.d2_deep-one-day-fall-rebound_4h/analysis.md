---
line: 7.d not profitable
backtest: 027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound_4h
idea tested: 027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3602 USD
---
## Findings
- **F1:** The book is almost a copy of holding the coins, which is why it fails on Calmar. It is long on 99.3 % of bars at a mean allocation of 1.08, and its daily returns track holding with correlation 0.93 and beta 0.93. Its deepest fall is -79.6 % against holding's -81.2 %, and its yearly return is 22.7 % against holding's 13.0 %.
- **F2:** The forecast does not decide when the book is in the coin. The forecast is 0 on 51 % of bars, yet the allocation stays positive on 98.8 % of those bars at a mean of 1.07, because each signal is held for 84 bars (14 days). So the book sits through every market fall, with no link to whether a panic happened.
- **F3:** Fall depth alone carries no unusual move. Across 1152 cases the unusual move is -0.06 % per case (strength -0.005) and the pooled slope t is -0.87. Among the 441 grid falls, the slope of the 14-day excess return on depth has t 1.13.
- **F4:** The effect appears only where the fall comes with an unusually wide range, and it is graded by that width. Falls in the lowest quartile of 24-hour range against the 30-day range (ratio 0.53) have a 14-day excess of -2.3 %, while the top quartile (ratio 1.64) has +1.2 %. The slope on the range ratio has t 2.24, and depth × range ratio has t 1.76 (n 441).
- **F5:** Read through the volatility ratio (7-day volatility against 60-day), signal cases in the calmest quartile (ratio 0.59) have a 14-day excess of -5.3 % (t -2.54, n 92), and the most agitated quartile (ratio 1.42) has +4.2 % (t 1.71, n 91). Among the book's long bars, the top volatility quintile earns 11.2 bp per bar, while the other four range from -1.6 to +3.0 bp.
- **F6:** The book's falls are the market's falls. Its 200 worst 30-day spells average -32.7 % against holding's -31.4 % over the same spells. In the five worst windows it was long on 98–100 % of bars, mostly after 30-day declines (mean 30-day return when long -5 % to -17 %).

## Ideas
- `027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound.d1_deep-fall-in-wide-range` (from F2, F3, F4, F6): The deeper a coin's 24-hour fall against its usual 24-hour move, the higher its return above its normal drift over the next 14 days, only while its last 24 hours' bar range is wider than its usual 30-day bar range, and the more so the wider that range relative to usual.
- `027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound.d2_deep-fall-under-volatility-expansion` (from F1, F5, F6): The deeper a coin's 24-hour fall against its usual 24-hour move, the higher its return above its normal drift over the next 14 days, only while its 7-day volatility is above its 60-day volatility, and the more so the higher that ratio.
- `027-03_panic-rebound-in-downtrend.d2_deep-one-day-fall-rebound.d3_range-blowout-down-rebound` (from F4, F5): The wider a coin's bar range over the last 24 hours relative to its usual 30-day range while its 24-hour return is negative, the higher its return above its normal drift over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
