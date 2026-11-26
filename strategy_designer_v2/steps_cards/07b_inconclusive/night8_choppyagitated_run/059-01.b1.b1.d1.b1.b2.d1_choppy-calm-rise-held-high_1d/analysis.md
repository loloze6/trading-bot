---
line: 7.b inconclusive
backtest: 059-01.b1.b1.d1.b1.b2.d1_choppy-calm-rise-held-high_1d
idea tested: 059-01.b1.b1.d1.b1.b2.d1_choppy-calm-rise-held-high
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3877 USD
---
## Findings
- **F1:** Step 5's main measure is on the predicted side but cannot be told from zero: the unusual 7-day move per case is +0.31 % with a day-pooled t of 0.42 over 343 days (536 cases). Its strength is 0.018 of the coin's usual 12.84 % move, about a third of the 0.05 that real ideas usually show. On the folds I can see, the measure is +0.88 % (t 0.76, 129 cases), or +1.16 % day-pooled (t 0.53, 98 days).
- **F2:** The effect points opposite ways in different years. In 2018 the mean unusual 7-day move is -7.3 % (t -3.14, 21 cases) and in 2019 it is -3.5 % (t -2.07, 30). In 2020 it is +2.8 % (t 1.59, 37) and in 2021 +6.5 % (t 2.62, 41). By window, w7 is -10.3 % (t -3.27) while w18 is +13.2 % (t 3.66). The near-zero average is two opposite effects cancelling, not one small effect.
- **F3:** The grading the theme claims is absent where I can see it. The Spearman correlation of the scaled weekly rise with the next 7-day unusual move is -0.06 (-0.02 over 14 days). By quartile of the scaled rise, the unusual move goes +0.99 %, +4.19 %, +5.22 % and then -0.56 % for the largest rises (scaled rise 2.58). By quartile of the forecast, the largest quartile is -2.14 % (t -1.10).
- **F4:** Changing the horizon does not give a clear answer either. The unusual move is -0.43 % over 1 day (t -1.14) and -0.37 % over 3 days (t -0.65), then +2.32 % over 14 days (t 1.30). Only the total 14-day move, +4.93 % (t 2.71), clears 2, and that comes mostly from the coins' normal drift.
- **F5:** The effect is not concentrated in a few coins. Per coin, the means run from -4.9 % (XMR, t -2.00, 19 cases) to +3.7 % (ZEC, t 1.68, 16) and +1.7 % (BTC, t 1.11, 27), with fewer than half of all cases positive (44 %, median -1.40 %).

## Ideas
- No ideas: The test already used every daily fold and coin available, so more data cannot help. The effect flips sign by period (F2) with no condition I measured that separates the two, its grading fails (F3), and no other horizon shows it clearly (F4); after this many amendments, the theme's effect is not in the data.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
