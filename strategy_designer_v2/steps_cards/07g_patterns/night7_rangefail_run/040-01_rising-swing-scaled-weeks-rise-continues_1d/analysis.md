---
line: 7.g patterns
backtest: 040-01_rising-swing-scaled-weeks-rise-continues_1d
idea tested: 040-01_rising-swing-scaled-weeks-rise-continues
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4365 USD
---
## Findings
- **F1:** In the rising profile on folds B and C, the 7-day excess return falls as the swing-scaled 20-day rise grows, which is the opposite of the tested idea. Over the cases with a positive swing-scaled rise the slope is -0.029 (t -2.41, 440 cases on 100 days). Over the upper half of those cases it is steeper, at -0.060 (t -3.59, 220 cases on 66 days).
- **F2:** The same negative grading appears at every horizon checked in the rising profile, though with fewer independent days the longer the horizon.
- **F3:** At 14 days the result depends on which grid is used, so the 14-day horizon is fragile and the reversal is better read at the shorter horizon.
- **F4:** Outside the rising profile, the swing-scaled 20-day rise grades nothing at 14 days. All five quintiles have excesses between -1.4 % and +2.8 %, and every |t| is at most 0.67.
- **F5:** In the rising profile, cases with a high swing-scaled rise also tend to have high recent agitation.
- **F6:** Neither a single day's move nor the weekday predicts anything once same-day cases are grouped.
- **F7:** The book earns mainly by riding long holds in the rising market, not from the forecast's grading.

## Ideas
- `040-01.g1_stretched-uptrend-rise-gives-back` (from F1, F2, F3, F4, F5): In a rising market, the more of its 20-day daily swings a coin's 20-day rise spans, the more the coin falls back against its normal drift over the next 7 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
