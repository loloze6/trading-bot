---
line: 7.b inconclusive
backtest: 062-01.b1_choppy-calm-falls-all-coins_1d
idea tested: 062-01.b1_choppy-calm-falls-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3935 USD
---
## Findings
- **F1:** The test's result points the way the idea predicts but stays far short of the bar: slope t 0.87 (500 grid cases on 208 days), unusual move in the short direction +0.32 % (t 0.75, 530 days), strength 0.030 of a usual 11.68 % move. The coins' normal drift of −0.69 % against the short turns the total move to −0.38 %. The test already used all four folds and all 19 coins on daily bars, so no more data is available.
- **F2:** In folds B and C the effect is clearer over 10 days than over the plan's 5. Among the signalled bars, the day-clustered slope t is 2.20 at 10 days (92 cases, 55 days), against 1.54 at 5 days and 1.65 at 3 days. The mean unusual move in the short direction is 2.7 % at 10 days, against 2.0 % at 5.
- **F3:** Over 10 days the further fall is graded by the swing-scaled 5-day fall. The mean excess 10-day return by bin of the scaled fall is:
- **F4:** The 5-day result depends on which 5-day grid is used. On grid offset 0 the short unusual move is 2.0 % (t 2.34). On offsets 1 to 4 it is only 0.8 % to 1.1 % (t 0.8 to 1.1), with slope t of −0.10, 1.23, 1.65 and −0.95. At 5 days the grading is mostly noise.
- **F5:** The effect is mixed across periods and coins. The mean excess 5-day return after a signal is:
- **F6:** Inside the choppy calm profile, the bars with the largest 5-day falls are followed by lower returns than the rest. The lowest quintile of past 5-day returns (mean −7.7 %) is followed by a −3.8 % excess 5-day return (t −2.86, 47 cases) and −6.0 % over 10 days. The two rising quintiles are followed by +1.0 % and +1.3 %, and bars with no signal by +0.6 %.

## Ideas
- `062-01.b1.b1_choppy-calm-falls-ten-days` (from F2, F3, F4, F6): In a choppy, calm market, a coin whose 5-day return is more negative, measured against its 30-day daily swing, falls further over the next 10 days. The larger the swing-scaled 5-day fall, the larger the further fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
