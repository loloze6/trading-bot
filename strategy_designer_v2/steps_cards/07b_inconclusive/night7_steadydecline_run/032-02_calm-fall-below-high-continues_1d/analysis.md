---
line: 7.b inconclusive
backtest: 032-02_calm-fall-below-high-continues_1d
idea tested: 032-02_calm-fall-below-high-continues
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 1
cost: 0.1944 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts but falls short of the bar: step 5's slope is +0.00077 with a day-clustered t of 1.22 over 1071 grid cases on 435 days. The size is clearer: the unusual move is +1.06 % per case over 3 days, with t 2.60 over 421 days, a strength of 0.124. In folds B and C, the 3-day return minus drift regressed on the raw depth below the 30-day high gives a slope of 0.069 with t 2.58 over 605 cases (unclustered), so deeper sits are followed by lower returns.
- **F2:** The grading is mixed rather than smooth across depth quintiles at 3 days, with 121 cases each. The three deepest quintiles (mean depth -37 %, -25 % and -18 %) show unusual short moves of +1.32 % (t 1.75), +0.88 % (t 1.39) and +2.21 % (t 3.22). The two shallowest (-10 % and -2 %) show -0.53 % (t -0.80) and -1.39 % (t -1.52), so much of the slope is the gap between near-high bars, which rise, and the rest.
- **F3:** The effect changes sign across periods. The unusual short move is +1.29 % (t 2.08, 265 cases) in 2018 and +1.34 % (t 3.52, 216 cases) in 2019. It turns to -2.84 % (t -3.38, 57 cases) in 2020 and -2.49 % (t -2.92, 67 cases) in 2021, driven by windows w16 (-5.9 %, t -4.38) and w18 (-5.2 %, t -3.81). These later years hold few cases, which drowns the overall t.
- **F4:** The effect is broadly on the predicted side across coins, though each coin is weak alone. The unusual 3-day short move is positive for 5 of 6 coins: ETH +1.58 % (t 1.73), ZEC +0.97 %, LTC +0.70 %, XMR +0.19 % and BTC +0.13 %. XRP is the exception at -0.79 % (t -0.74). No single coin has enough cases (68 to 136) to show it clearly.
- **F5:** The plan's 3-day horizon is where the graded effect shows best. The slope of return minus drift on depth has these t values: 2.34 at 1 day (1850 cases), 2.58 at 3 days (605), 1.34 at 5 days (361) and -0.70 at 10 days (176). No other horizon would give a clearer answer.

## Ideas
- `032-02.b1_calm-fall-depth-more-coins` (from F1, F3, F4, F5): In a falling, calm market, the further a coin's close sits below its highest close of the past 30 days, the more it falls over the next three days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
