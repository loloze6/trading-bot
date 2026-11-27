---
line: 7.b inconclusive
backtest: 064-02_choppy-range-top-break-continuation_1d
idea tested: 064-02_choppy-range-top-break-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4253 USD
---
## Findings
- **F1:** The positive mean rests on a few cases. Over 112 cases (81 days) in folds B and C, the mean 5-day unusual move is +5.5 % (t 1.44), but the median is −1.4 % and only 41 % of cases rise more than usual. The single largest case carries 62 % of the sum and the top five carry 96 %. Without those five, the mean falls to +0.24 %, and without the top ten it is −0.97 %.
- **F2:** The supporting slope (t 5.74 in step 5) comes from those same outliers, not from grading. Across cases, the rank correlation of the forecast with the scaled 5-day move is −0.07 (p 0.43). The slope on the winsorised move has a correlation of 0.025 (p 0.80). By forecast quartile, the 5-day mean runs +7.1 %, +1.8 %, −0.7 % and +15.3 %, with medians negative in three quartiles. So a larger clearance of the old high does not lead to a larger further rise.
- **F3:** Trimming the tails leaves a small effect that cannot be told from zero. With the 5-day move winsorised at 5 %/95 %, the mean is +1.7 % (t 1.30), and the 5 %-trimmed mean is +1.2 %.
- **F4:** No part of the data shows the effect clearly. Calm breakouts (70 cases) have a scaled 5-day move of 0.32 (t 1.68), and 0.11 at 10 days (t 1.92). Agitated breakouts (13 cases) have 0.004. By day's size relative to the 30-day swing, the terciles run t 0.70, 0.97 and 1.13. By 60-day sign, up60 gives t 1.15 and dn60 t 1.51. Every subset is under t 2.
- **F5:** The sign flips with the period, so the effect is not stable. In 2018 and 2019 the 5-day mean is −6.1 % (t −1.49) and −4.3 % (t −1.91), and 2019's 10-day mean is −7.9 % (t −2.73). In 2020 and 2021 it is +3.2 % (t 1.45) and +16.2 % (t 1.47). Windows w7 to w9 and w12 are negative; w18 is +12.7 % (t 1.84).
- **F6:** Longer horizons do not make the result clear. The mean unusual move is +0.3 % at 1 day (t 0.58), +1.7 % at 3 days (t 1.35), +5.5 % at 5 days (t 1.44) and +6.9 % at 10 days (t 1.80), each with a median below zero.
- **F7:** The test already used every fold and every coin available on daily bars, so there is no more data to rerun the idea unchanged on.

## Ideas
- No ideas: The theme's effect is not in the data. The positive mean comes from a handful of extreme cases (F1), shows no grading by the size of the breakout (F2), and holds in no coin, period, agitation or horizon with a t of 2 (F4, F5, F6). The test already covered all the daily data there is (F7).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
