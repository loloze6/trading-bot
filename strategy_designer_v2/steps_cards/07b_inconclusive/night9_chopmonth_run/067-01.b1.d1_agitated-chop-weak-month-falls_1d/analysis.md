---
line: 7.b inconclusive
backtest: 067-01.b1.d1_agitated-chop-weak-month-falls_1d
idea tested: 067-01.b1.d1_agitated-chop-weak-month-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3293 USD
---
## Findings
- **F1:** The test's own result is on the predicted side but short of the bar. The slope t is 1.09 on 215 cases over 108 days, and the unusual move is +1.22 % per 7 days with a t of 1.66 over 265 days. The test already used all four folds and all 19 coins, so there is no more data to give it.
- **F2:** In folds B and C, one window carries the effect. On the 58 short cases, the mean unusual 7-day move is +1.71 % (t 0.90). Window w16's 5 cases average +32.9 % (t 19.1), and without w16 the mean is -1.23 % (t -0.80, median -0.29 %, 49 % positive).
- **F3:** Without w16 the grading goes the wrong way. The slope t of the 7-day unusual move on the forecast is 0.61. By depth of the short, the deepest third averages -1.53 % and the middle third -2.85 %, against +0.31 % for the shallowest third.
- **F4:** No other horizon shows a fall that grows with the past month's fall. The unusual move in the short direction is +0.84 % over 3 days (t 0.51) and +0.62 % over 5 days (t 0.33). It is -0.54 % over 14 days (t -0.21) and -3.34 % over 21 days (t -0.90), and the slope t on the forecast is -1.34 at 21 days.
- **F5:** The effect is not steady across periods or coins. By year it is +1.86 % in 2019 (t 1.04), +13.0 % in 2020 (t 3.05, which includes w16) and -3.65 % in 2021 (t -1.47). Across coins, only ETH (8 cases, t 2.63) and ADA (4 cases) are clearly positive, and LINK and TRX are negative.

## Ideas
- No ideas: The fall after a weak month in a choppy, agitated market appears only in one crash window (w16) and reverses without it (F2, F3). No horizon, depth of fall or period shows it in a graded way (F4, F5), and no more data exists to retest it (F1), so the theme's effect is not in the data.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
