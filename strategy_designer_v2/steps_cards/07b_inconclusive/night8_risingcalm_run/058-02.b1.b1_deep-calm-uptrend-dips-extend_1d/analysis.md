---
line: 7.b inconclusive
backtest: 058-02.b1.b1_deep-calm-uptrend-dips-extend_1d
idea tested: 058-02.b1.b1_deep-calm-uptrend-dips-extend
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4027 USD
---
## Findings
- **F1:** The tested idea, that deeper scaled dips fall more over 5 days, is on its own side but far from the bar: the main measure's mean is 0.0052 with t 0.61 (715 cases, 239 days), and its size is an unusual move of +0.04 % per case with t 0.09 (1159 cases, 594 days), 0.000 of the usual 11.68 % move.
- **F2:** At the plan's 5-day horizon inside rising calm (folds B and C, 265 cases on 101 days), the depth is not graded: the product has t 0.09, and the mean excess 5-day return is -1.21 % for the deepest third, +1.30 % for the middle third and +0.81 % for the shallowest third, so the supporting check passed only because of the deepest third.
- **F3:** Over shorter horizons inside rising calm, the depth points toward recovery, the brief's own effect: with the depth recomputed from prices, deeper dips are followed by a higher excess return over 1 day (product t +2.13, Spearman -0.108, mean excess +0.45 %, 1011 cases on 413 days) and over 3 days (t +1.98, Spearman -0.264, mean excess +0.70 %, 323 cases on 139 days); the plan's forecast-based product agrees, with t -1.73 over 1 day and -1.88 over 3 days (negative here means recovery).
- **F4:** The short-horizon recovery is specific to rising calm: in other markets the same depth measure shows nothing, with 1-day t of -0.82 (choppy), -0.16 (falling) and +0.04 (rising agitated), and 3-day t of -0.80, -1.07 and +0.34.
- **F5:** The 5-day effect is mixed across periods and coins: the product is -0.041 in 2020 (106 cases), +0.017 in 2021 (90 cases) and +0.118 in 2018 (18 cases), and it is positive on 5 of the 10 coins and negative on the other 5.
- **F6:** No more data is available than the test used, since it already ran all 19 coins on all four folds; the short book also lost (Sharpe -0.77), because its total move per case of -0.69 % comes from the coin's normal drift against a short (-0.73 %) and costs 3.1 times the 0.22 % cost of a trade.

## Ideas
- `058-02.b1.b1.b1_calm-uptrend-dips-bounce-briefly` (from F3, F4, F2, F1): In a rising, calm market, the further a coin's close sits below its highest close of the past 5 days, measured against its usual daily swing over the past 30 days, the larger its rise over the next 3 days.
- `058-02.b1.b1.b2_calm-uptrend-dip-next-day-rebound` (from F3, F4): In a rising, calm market, the further a coin's close sits below its highest close of the past 5 days, measured against its usual daily swing over the past 30 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
