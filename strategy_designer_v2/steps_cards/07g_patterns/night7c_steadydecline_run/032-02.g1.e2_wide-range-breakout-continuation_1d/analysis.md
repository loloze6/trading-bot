---
line: 7.g patterns
backtest: 032-02.g1.e2_wide-range-breakout-continuation_1d
idea tested: 032-02.g1.e2_wide-range-breakout-continuation
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3974 USD
---
## Findings
- **F1:** On the 5-day grid of folds B and C, closes at the 28-day highest close (within 0.1 %) were followed by a mean excess 5-day return of +4.78 % (t 2.60 with the cases of one day taken together, 114 cases on 54 days, strength 0.39). All other grid bars returned -0.47 % (1164 cases).
- **F2:** The effect grows with horizon. At 10 days the same at-high cases give +8.88 % excess (t 3.67, 108 cases), against -0.87 % (t -1.78) for the rest.
- **F3:** The wide-range condition of the tested idea adds nothing. At-high cases with a wide day (range at least its 28-day mean) gave +4.78 % (t 2.17, 75 cases), and those with a narrow day gave +4.79 % (t 1.57, 39 cases).
- **F4:** The tested idea's own regime selected few cases and little effect. Grid bars with a 28-day return above 0 and a wide range gave only +0.24 % excess (t 0.33, 276 cases). Unconditional nearness carried the edge: the top quintile of nearness to the 28-day highest close gave +2.99 % (t 3.67), and the second-lowest quintile gave -3.17 % (t -4.88).
- **F5:** The pattern holds over other lookbacks:
- **F6:** The grading by nearness is not monotonic across the whole range. By decile of nearness to the 28-day high:
- **F7:** The at-high gain is weakest after the largest run-ups. The top tercile of 28-day return among at-high cases gave -0.36 % (t -0.17, 38 cases), against +6.11 % and +8.59 % (t 2.83) for the lower two terciles.
- **F8:** The book's profit is concentrated. The 10 % best of its 1080 trades carry 84 % of the summed net trade profit, and the window Sharpe ranges from -3.10 (w9) to 4.01 (w11).
- **F9:** The brief's calm-decline situation does not grade in these folds. Among grid bars with a 28-day return below 0 and below-median volatility, only the second quartile of 28-day return fell (-3.78 %, t -3.42). The deepest quartile gave -0.15 % (t -0.10).

## Ideas
- `032-02.g1.e2.g1_closing-high-continuation-ten-days` (from F1, F2, F3, F4, F5): In any coin, the nearer its close is to its highest close of the last 28 days, the larger its rise over the next 10 days, whatever the width of that day's range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
