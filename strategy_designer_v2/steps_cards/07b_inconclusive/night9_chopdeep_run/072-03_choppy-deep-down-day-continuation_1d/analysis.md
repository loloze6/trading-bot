---
line: 7.b inconclusive
backtest: 072-03_choppy-deep-down-day-continuation_1d
idea tested: 072-03_choppy-deep-down-day-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3633 USD
---
## Findings
- **F1:** Step 5's main measure is zero rather than short of the bar: the mean timing gain is 0.0000369 with t 0.04 over 1885 cases on 1108 days. On down days in choppy markets, depth does not rank the next day at all (Spearman of depth against next-day excess return 0.004, p 0.92, 621 cases). The depth quintiles are not in order: -0.80 %, +0.21 %, +0.08 %, -0.41 %, +0.46 % from deepest to shallowest.
- **F2:** The idea held next day on up days instead, the side the test left out. On choppy up days, the deepest quintile below the 20-day high fell -1.07 % the next day (t -2.18, 126 cases), against -0.09 % for the quintile at the high. Deepest 40 % minus shallowest 40 % was -0.76 % against +0.01 % (Welch t -1.89, 629 cases), Spearman 0.076 (p 0.058).
- **F3:** On up days the grading grows with the horizon. On a non-overlapping grid, depth against forward excess return gives Spearman 0.28 (p 0.001, 122 cases) over 5 days and 0.45 (p 0.0002, 64 cases) over 10 days. The deepest 40 % lost -4.7 % over 5 days and -9.5 % over 10 days, while the shallowest 40 % gained +3.2 % and +3.9 %. The graded gain has t 2.64 over 5 days (76 days) and 2.71 over 10 days (38 days). Over 10 days the strength is 0.31 of a usual move.
- **F4:** Down days stay ungraded at every horizon tested, with Spearman 0.03 at 3 days, 0.00 at 5 days and 0.05 at 10 days. Pooling down days with up days dilutes the effect: over 10 days the pooled t is 2.05 against 2.71 for up days alone. This is why a down-day test sees nothing.
- **F5:** Across coins, the 5-day up-day grading is positive on 5 of 6 coins, with Spearman from 0.11 (LTC) to 0.31 (XRP); XMR is the exception at -0.14. It depends on the sampling grid, with Spearman falling from 0.28 to 0.20, 0.16, 0.06 and -0.07 over the five offsets. It is not steady across years either: -0.13 in 2018, 0.01 in 2019, 0.13 in 2020 and 0.26 in 2021. So the longer-horizon up-day effect is real in sign but noisy, and needs all four folds to be judged.
- **F6:** The test's one-day horizon is too short for this cost. The tested book's total move per case is -0.21 %, only 1.1 times the 0.19 % cost of a trade. Over 5 to 10 days, deep up-day cases move -4.7 % to -9.5 % (F3), many times that cost.

## Ideas
- `072-03.b1_choppy-deep-bounce-fades` (from F2, F3, F4, F5, F6): In a choppy market, on a day that closed up, the further the close sits below the coin's 20-day high, in units of its 20-day daily-return standard deviation, the larger its fall over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
