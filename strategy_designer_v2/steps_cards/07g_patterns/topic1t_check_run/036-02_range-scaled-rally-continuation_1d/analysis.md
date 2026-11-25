---
line: 7.g patterns
backtest: 036-02_range-scaled-rally-continuation_1d
idea tested: 036-02_range-scaled-rally-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4965 USD
---
## Findings
- **F1:** The tested idea's effect is not in the 7-day returns of folds B and C. On the 7-day grid, the five quintiles of the range-scaled 3-day return are followed by excess returns of -0.32 %, -1.21 %, +0.74 %, +1.33 % and +0.22 % (top quintile t 0.18, n 201). There is no rising grade, which matches step 5's slope t 1.43 and its unusual move of -0.15 % (t -0.33).
- **F2:** Over 3 days the effect shows only in agitated markets (30-day swing above the 90-day swing). On rising 3-day bars there, the range-scaled rise grades the next-3-day excess return with slope +0.0162 (t 3.00, n 244). In calm markets the same slope is +0.0015 (t 0.33, n 455).
- **F3:** Inside the agitated rises, the grade depends on the coin's 30-day trend. In a rising trend the slope is +0.0251 (t 3.52, n 119). In a falling trend it reverses to -0.0286 (t -2.52, n 89); choppy is flat (+0.0025, t 0.15, n 36). By year the slope is positive in 2019, 2020 and 2021 (t 2.14, 1.87, 3.84) but negative in 2018 (t -1.67).
- **F4:** In falling markets, up days are faded the next day. After an up day in a 30-day falling trend, the next-day excess return averages -0.91 % (t -2.31 with same-day cases summed, 739 cases on 227 days). After up days in agitated markets it averages -0.70 % (t -2.31, 832 cases on 312 days). Neither is graded by the size of the up day (slopes t 0.58 and -0.75).
- **F5:** Down days in agitated markets rebound the next day, graded by their size: slope -0.0174 (t -5.30, n 830). The lowest decile of the scaled one-day return is followed by +1.00 % (t 4.30). This is the strongest pattern found, but it repeats the held falling and agitated down-day rebound books (044-02, 038-01, 047-01), so it is no discovery.
- **F6:** Weekdays differ. Thursday and Friday are followed by next-day excess returns of +0.47 % (t 3.19) and +0.39 % (t 2.87). Monday and Wednesday are followed by -0.31 % (t -1.98) and -0.49 % (t -2.69). Thursday–Friday beat Monday–Wednesday in each of 2018 to 2021. This is close to the held late-week book 045-01 and is not graded, so no idea is written from it.
- **F7:** The book earns almost entirely from the coins' own rise. Its mean daily return is 0.15 % against 0.13 % for holding, and it gains little as timing. Allocations above 1 are followed by next-day returns of only +0.37 %, against -0.30 % for allocations of 0.01 to 0.5.

## Ideas
- `036-02.g1_rising-agitated-scaled-rally-continuation` (from F2, F3, F1): In a rising, agitated market, a coin whose 3-day return is large against its 30-day mean daily high-to-low range keeps rising over the next 3 days, and the larger that range-scaled rise, the larger the further gain.
- `036-02.g2_falling-agitated-rally-fade` (from F3, F4): In a falling, agitated market, a coin whose 3-day return is large against its 30-day mean daily high-to-low range falls over the next 3 days, and the larger that range-scaled rise, the larger the fall that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
