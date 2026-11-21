---
line: 7.g patterns
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more_1h
idea tested: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4087 USD
---
## Findings
- **F1:** The tested shape adds nothing beyond the fall itself. Among net 24-hour falls, the largest hourly move's share of the day's moves has a pooled slope t of -0.97 against the 48-hour excess return (n 4101, coins -2.11 to +0.73). The largest hour's share of volume has t -1.30. This matches the step-5 strength of 0.011 and the unusual move of 0.4 times the cost.
- **F2:** The depth of a 24-hour fall predicts the rebound. Among net falls, the 24-hour return in units of the coin's 30-day hourly volatility has a pooled slope t of -4.36 on the 48-hour excess (n 3841), and the slope is negative on all 6 coins (t -1.17 to -2.41). Over all grid bars, the deepest-fall quintile ends +0.46 % above drift (t 2.62, n 1575, strength 0.068), which is 2.4 times the 0.19 % round trip.
- **F3:** Among net 24-hour falls, a hotter day leads to a larger rebound. The last 24 hours' volatility over the coin's 30-day volatility has a pooled slope t of +4.20 on the 48-hour excess (n 3841), positive on all 6 coins (t +1.33 to +2.00). Over all bars, the top quintile ends +0.52 % above drift (t 2.48, strength 0.064).
- **F4:** The last 24 hours' volume over the coin's 30-day average daily volume predicts the next 48 hours. Its pooled slope t is +4.19 on the 48-hour excess (n 7859), positive on all 6 coins (+0.29 to +3.52) and in 6 of 8 years (2021 -2.19, 2022 -0.47). On net falls alone it is t +3.79. The top quintile ends +0.40 % above drift (t 1.96, strength 0.050), 2.1 times the cost.
- **F5:** The 24-hour excess return depends on the weekday. From Friday's bars it is +0.52 % (t 5.38, n 2459); from Monday's it is -0.36 % (t -3.24) and from Thursday's -0.40 % (t -3.46). This is a calendar condition, not a graded situation, so I write no idea from it.
- **F6:** The book's gain is mostly the coin's own drift. In the book's worst decile of days the book loses 3.6 % while the coins lose 7.5 %, and in its best decile it gains 3.8 % while the coins gain 7.8 %. By year the book earns about half of each year's coin mean (for example 2020 +0.25 % against +0.42 %, 2018 -0.10 % against -0.35 %). This fits a long-only book whose timing adds little and whose Calmar failed at 0.55.

## Ideas
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more.g1_deep-daily-fall-rebounds` (from F2, F1): The deeper a coin's fall over the last 24 hours, measured against its usual daily move over the past 30 days, the more it rises over the next 2 days.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more.g2_turbulent-fall-rebounds-more` (from F3, F1, F2): After a net fall over the last 24 hours, the higher the coin's hourly volatility over those 24 hours compared with its past 30 days, the more it rises over the next 2 days.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d3_grinding-fall-rebounds-more.g3_heavy-volume-precedes-rises` (from F4, F3): The higher a coin's traded volume over the last 24 hours compared with its average daily volume over the past 30 days, the more it rises over the next 2 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
