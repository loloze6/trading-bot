---
line: 7.b inconclusive
backtest: 031-01_extreme-rise-partly-reverses_1d
idea tested: 031-01_extreme-rise-partly-reverses
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3318 USD
---
## Findings
- **F1:** The mean is pulled down by a few very large continued rises: over 30 days my recount (179 cases, 112 days) gives a mean unusual move of -4.04 % (t -1.07, cases of one day together), but the median is +1.24 % and 54 % of cases go the predicted way. Capping the 5 % largest and smallest moves brings the mean to -0.16 % (t -0.06), so the typical case shows neither reversal nor continuation.
- **F2:** The effect is not graded by the size of the rise. The correlation between the raw z90 and the 30-day unusual move is 0.017. By z90 tercile the mean goes from -7.95 % (low, z about 1.06, t -1.22) to -1.19 % (high, z about 3.34, t -0.22), the opposite of the grading the idea predicts. By forecast tercile the strongest third is -5.09 % (t -1.70).
- **F3:** No coin, period or recent-path subset shows a clear reversal:
- **F4:** A shorter horizon does not show the reversal either. Over 10 days on its own grid (448 cases, 246 days) the mean unusual move is -1.73 % (t -1.32, median +0.64 %), and capped it is -0.81 % (t -0.83).
- **F5:** Most of the losing total move is the coins' normal drift, not timing. The 30-day total move is -7.91 % (t -2.39, cases not clustered) against an unusual move of -4.04 %. This matches step 5's -8.13 % total, of which -3.86 % is drift, so shorting after these rises mostly pays away the coins' usual rise.

## Ideas
- No ideas: The result sits on the continuation side but cannot be told from zero, and it rests on a few large outliers (F1). No coin, period, recent path, horizon or forecast size shows the predicted reversal (F2–F4), so there is no part of the data to narrow the idea to and no continuation effect large enough to propose instead.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
