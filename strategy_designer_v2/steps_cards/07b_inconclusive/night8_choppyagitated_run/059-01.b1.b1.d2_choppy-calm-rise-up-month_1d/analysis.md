---
line: 7.b inconclusive
backtest: 059-01.b1.b1.d2_choppy-calm-rise-up-month_1d
idea tested: 059-01.b1.b1.d2_choppy-calm-rise-up-month
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3508 USD
---
## Findings
- **F1:** In folds B and C, the cases' unusual 14-day move is positive but cannot be told from zero: +1.44 % with t 0.71 over 112 cases. Its median is −0.30 % and only 49.1 % of cases are above zero, so a few large moves carry the mean. Step 5's figure over all folds is +0.97 % with t 0.86.
- **F2:** The effect is drowned by the market's own moves. The unusual 14-day move is strongly negative in 2018 (−22.5 %, t −6.17, 15 cases) and 2019 (−6.4 %, t −2.55, 21 cases), and positive in 2020 (+7.3 %, t 2.29, 40 cases) and 2021 (+9.5 %, t 2.62, 36 cases). The windows swing the same way, from w7 at −22.0 % (t −7.2) to w18 at +24.3 % (t 5.8). So the sign follows the year's market, not the scaled weekly rise.
- **F3:** The grading the idea claims does not show. By forecast tercile the unusual 14-day move is −1.5 % (t −0.34), +3.0 % (t 1.10) and +2.8 % (t 0.80), so the strongest cases do no better than the middle ones. The rank correlation between forecast and move is 0.107 (p 0.26, 112 cases). Splitting by the 7-day rise itself gives the same flat pattern: −0.5 %, +4.2 %, +2.0 %.
- **F4:** A longer horizon grows the mean but does not make it clear. The unusual move is +0.6 % at 7 days (t 0.49), +1.4 % at 14 (t 0.71), +2.0 % at 21 (t 0.87) and +4.1 % at 28 (t 1.19, 100 cases). The total move does reach t 2.75 at 28 days, but that is the coins' normal drift.
- **F5:** No part of the situation holds the effect clearly:
- **F6:** No more data exists for this idea. The test already used all 19 coins, all four folds and the daily bars, and the hourly bars cover the same period. So the tested idea cannot be rerun on a larger sample.

## Ideas
- No ideas: The theme's effect is not in the data. The unusual move is positive but small and uncertain (F1), and it does not grow with the scaled weekly rise (F3). It shows only in up years and turns over in down years (F2), and no horizon, condition or coin group gives it clearly (F4, F5), with no further data to test it on (F6).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
