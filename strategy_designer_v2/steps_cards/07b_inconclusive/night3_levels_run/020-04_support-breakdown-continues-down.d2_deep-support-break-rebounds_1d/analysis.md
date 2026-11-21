---
line: 7.b inconclusive
backtest: 020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds_1d
idea tested: 020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4650 USD
---
## Findings
- **F1:** The tested forecast reaches its +20 ceiling on 35 % of the positive cases, and its 70th percentile is already 20, so the "top fifth by forecast" is simply the capped cases. Their raw depth × touches value runs from 6.7 (10th percentile) to 116 (90th), mixing shallow and deep breaks, and within them the raw value barely ranks the 5-day move (Spearman 0.048). The test's +0.17 % (t 0.44, 815 cases) is therefore a blend.
- **F2:** Ranked on the raw depth × touches value instead, the 5-day unusual move rises with the situation. Decile 0 is -0.21 %, deciles 1–4 are -0.78 % to -1.38 % (decile 2: t -2.34), decile 8 is -0.01 %, and the top decile is +1.97 % (t 2.32, 235 cases), with a total move of +2.57 % and a strength of 0.17. The top raw fifth is +0.98 % (t 1.81, 470 cases), total +1.58 %, strength 0.09.
- **F3:** Shallow breaks of support keep falling rather than rebounding. In raw quintile 1 (median 5.2) the 5-day unusual move is -1.12 % (t -2.67, 465 cases) and the 10-day one is -1.60 % (t -2.50, 443 cases). Over all positive-forecast cases the 5-day unusual move is -0.30 % (t -1.42, 2346 cases).
- **F4:** The rebound after the deepest breaks is broad but small in each part. In the top raw fifth the 5-day unusual move is positive on all 6 coins (LTC +0.07 % to XMR +2.14 %, none with t above 1.6) and in 7 of 8 years (2019: -0.04 %), with 29 to 121 cases per year.
- **F5:** The rebound shows most clearly over about 3 days. For the top raw fifth it is +0.96 % at 3 days (t 2.35, 473 cases, strength 0.12), +0.98 % at 5 days (t 1.81) and +1.21 % at 10 days (t 1.59, 443 cases). The tested forecast-top fifth gives only t 0.92, 0.44 and 0.86 at the same horizons.
- **F6:** Against the backtest's 0.19 % cost per buy and sell, the deepest breaks clear it and the whole set does not. The top raw fifth's total move (+1.58 %) is about 8 times the cost and its unusual move (+0.98 %) about 5 times. The tested idea's whole set has an unusual move of -0.19 % per case (-1.0 times the cost), consistent with the earlier finding that no idea below cost pays.

## Ideas
- `020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds.b1_deep-support-break-rebounds-wider` (from F2, F4, F6): When a coin closes far below a price where it turned up several times in the past 90 days, it tends to rise over the next 5 days, and the deeper its close under that level and the more times the level held, the larger the rise.
- `020-04_support-breakdown-continues-down.d2_deep-support-break-rebounds.b2_deepest-support-breaks-rebound-fast` (from F2, F3, F5, F6): When a coin closes far below a price where it turned up several times in the past 90 days, it tends to rise over the next 3 days, and the rise grows with the close's depth under that level times the number of times the level held, so that the deepest breaks of the most-touched levels rise the most.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
