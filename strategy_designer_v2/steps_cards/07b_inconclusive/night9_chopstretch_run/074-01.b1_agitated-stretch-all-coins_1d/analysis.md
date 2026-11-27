---
line: 7.b inconclusive
backtest: 074-01.b1_agitated-stretch-all-coins_1d
idea tested: 074-01.b1_agitated-stretch-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.2081 USD
---
## Findings
- **F1:** On the visible folds B and C, the tested cases (forecast > 0 on the 10-day grid) show no rebound at any horizon. The mean excess return is -0.33 % over 3 days (t -0.24), -0.41 % over 5 days (t -0.24), -0.24 % over 10 days (t -0.10) and +1.49 % over 20 days (t 0.42), on 244 cases over 72 days. This matches step 5's whole-data size, an unusual move of -0.56 % (t -0.75, 467 days), so the weak positive weighted mean (t 0.68) is noise rather than a rebound too small to show.
- **F2:** The graded part of the idea is absent. Among agitated grid bars closing below their 20-day average, the Spearman correlation between depth and the 10-day excess return is -0.03 (n 209). The depth quartiles do not order either: deepest +1.55 % (t 0.26), q2 -2.51 % (t -1.10), q3 +1.10 % (t 0.35), shallowest -1.99 % (t -0.53).
- **F3:** The contrast the brief predicts holds on the calm side only, and it is a continuation, not a rebound. Below-average bars in calm markets fall further, by -3.44 % over 10 days (t -2.06, 211 cases, 68 days) and -3.21 % over 5 days (t -2.63). Agitated ones give -0.45 % over 10 days (t -0.19) and -1.10 % over 5 days (t -0.57), so agitation removes the fall but brings no rise.
- **F4:** No part of the data carries a rebound clearly enough to amend the idea to it.
- **F5:** The test already used every fold (A to D) and all 19 coins, so no more data is available to sharpen a result that is on the predicted side only in its weighted mean. Re-running the idea unchanged would not settle it.

## Ideas
- No ideas: The theme's effect is not in the data. In agitated markets a close below the 20-day average is followed by no rebound at 3, 5, 10 or 20 days (F1), the move does not grow with depth (F2), no trend, year or coin shows the rebound (F4), and the test already covered all the data available (F5).

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
