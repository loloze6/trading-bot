---
line: 7.b inconclusive
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more_1h
idea tested: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3497 USD
---
## Findings
- **F1:** The tested slope is on the side the idea predicts but well short of the bar. Its t is 0.91 on 8,579 grid cases, of which 4,191 have a positive forecast, and grind minus jump is +0.29 %. The effect is small: the unusual move is +0.08 % per case, a strength of 0.011 against the usual ~0.05 (findings F10). That is 0.4 times the 0.19 % round trip, a size that has never paid (findings F11).
- **F2:** The effect is clear only when the coin is more agitated than usual. Among net 24-hour falls, the slope of the 48-hour excess return on the raw evenness of the losses has t 3.50 when 24-hour hourly volatility is above its 30-day level (1,220 cases, slope 0.073). It has t -0.85 when calmer (2,881 cases, slope -0.014).
- **F3:** The effect is mixed across coins and years. The slope t by coin runs from -0.85 (ETH) to 2.12 (XMR), with BTC 0.21, LTC 1.29, XRP -0.54 and ZEC 0.22. By year it is positive in 6 of 8 years but at or above 2 only in 2022 (2.05); 2024 is -1.31.
- **F4:** The effect is not graded at the top. Over the positive-forecast quintiles the mean 48-hour excess return rises from -0.24 % through +0.06 %, +0.26 % and +0.33 %, then falls to -0.12 % in the most even quintile (about 854 cases each).
- **F5:** The horizon matters. On the whole grid the slope t is 1.51 at 12 hours, 1.86 at 24, 0.91 at 48, -1.63 at 96 and -3.10 at 168. After a net fall the coin's 7-day excess return is -0.50 %, against +0.48 % on other bars (4,268 and 4,455 cases), so the rebound fades and the fall resumes within a week.
- **F6:** The depth of the fall carries more than its evenness. Among falls, depth in units of 24-hour volatility predicts the 48-hour return with t 2.15 (24-hour: t 2.54). With depth in the regression, the forecast's own t drops to 0.71. The forecast and the raw evenness correlate at 0.85.
- **F7:** More data exists than the test used. It ran on 6 coins, while 13 more have hourly bars in folds A and D and partly in B and C.

## Ideas
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more.b1_grinding-fall-more-coins` (from F1, F3, F7): The more a coin has fallen over the last 24 hours in many similar-sized hourly steps rather than in one large hour, the more it rises over the next 2 days.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more.b2_grinding-fall-in-agitation` (from F2, F1, F4): The more a coin has fallen over the last 24 hours in many similar-sized hourly steps rather than in one large hour, the more it rises over the next 2 days, only while its hourly moves over the last 24 hours are larger than its hourly moves over the last 30 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
