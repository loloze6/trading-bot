---
line: 7.g patterns
backtest: 031-01.g1.g1.g1.d1_two-week-rise-carries-weekend_1d
idea tested: 031-01.g1.g1.g1.d1_two-week-rise-carries-weekend
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4547 USD
---
## Findings
- **F1:** The weekend effect is all on Saturday. At Friday's close the 14-day volatility-scaled rise predicts Saturday's excess return with slope 0.0056 (t 2.85, 2118 cases, 363 days). By z14 quintile, from fall to rise, Saturday's excess return is −0.38 %, −0.14 %, +0.32 %, +0.41 % and +1.07 %. It predicts nothing for Sunday (slope t 0.17) or for Monday and Tuesday together (t −0.52).
- **F2:** The Friday-to-Saturday slope holds in both halves of the period: t 2.11 up to 2021 (1056 cases) and t 2.01 from 2022 (1062 cases). It also holds for other lookbacks. Friday's 7-day rise gives t 2.95 and its 28-day rise t 2.68. Thursday's 7-day rise predicts Saturday's return, its day after, with t 3.36.
- **F3:** The same past rise predicts nothing for the next day on any other weekday. The 14-day slope t is −0.54 on Monday bars, −0.13 on Tuesday, −0.11 on Wednesday, 1.29 on Thursday, −0.33 on Saturday and 0.00 on Sunday. The continuation is specific to Saturday, not a general daily trend.
- **F4:** The book earns its weekend on Saturday and takes its tail on Sunday. Its mean daily return is +0.267 % on Saturdays against +0.060 % on Sundays. Of its worst 2 % of active days, 61 fall on Sunday and 31 on Saturday. Of its best 2 %, 55 fall on Saturday and 37 on Sunday.
- **F5:** A large Saturday move partly reverses on Sunday. Saturday's volatility-scaled move predicts Sunday's excess return with slope −0.0052 (t −2.29, 2172 cases). The top Saturday quintile (mean z 1.15) is followed by −0.75 % on Sunday and the bottom quintile (mean z −0.90) by +0.24 %. With more than 50 slopes examined, this is borderline.

## Ideas
- `031-01.g1.g1.g1.d1.g1_two-week-rise-carries-saturday` (from F1, F2, F3, F4): The higher a coin's 14-day rise, measured in its usual daily moves at Friday's close (UTC), the more it rises over the following day, Saturday, alone.
- `031-01.g1.g1.g1.d1.g2_saturday-surge-fades-sunday` (from F5, F4): The larger a coin's rise on Saturday (UTC), measured in its usual daily moves, the more it falls back over the following day, Sunday.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
