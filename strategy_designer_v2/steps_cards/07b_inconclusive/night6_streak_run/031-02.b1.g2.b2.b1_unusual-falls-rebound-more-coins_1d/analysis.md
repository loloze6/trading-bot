---
line: 7.b inconclusive
backtest: 031-02.b1.g2.b2.b1_unusual-falls-rebound-more-coins_1d
idea tested: 031-02.b1.g2.b2.b1_unusual-falls-rebound-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3992 USD
---
## Findings
- **F1:** The tested slope is positive but short of the bar. On the plan's 2-day grid it has a day-clustered t of 1.28 (8,995 cases, 1,230 days). Its size is an unusual move of only +0.08 % per case (t 0.42), 0.3 times the 0.22 % cost of a trade. The test used every coin and fold the data holds, so there is no more data to add.
- **F2:** The rebound is concentrated in the first day after the fall. Over the next 1 day, the same regression on the forecast gives a slope of +0.00038 with a day-clustered t of 2.45 (18,028 cases, 2,405 days). The second day alone, on the 2-day grid, has a slope of -0.00012 (t -0.54). This return given back on day 2 is what dilutes the plan's 2-day measure to t 1.28.
- **F3:** Over 1 day the effect is graded as the idea says. Mean excess return by forecast quintile, mean forecast in brackets:
- **F4:** Over 1 day the effect is broad, not carried by one part of the data.
- **F5:** Neither the coin's 30-day trend nor longer horizons separate the effect.

## Ideas
- `031-02.b1.g2.b2.b1.b1_unusual-falls-rebound-next-day` (from F1, F2, F3, F4, F5): The larger a coin's percentage fall on its latest day, measured against the standard deviation of its daily returns over the past 60 days, the more the coin rises over the next 1 day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
