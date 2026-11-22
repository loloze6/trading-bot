---
line: 7.g patterns
backtest: 029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline_1d
idea tested: 029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3729 USD
---
## Findings
- **F1:** The day after a coin's sharpest falls, measured against its own prior 20-day volatility (the lowest decile of the day's return divided by that volatility), the coin's next-day return beats its normal daily drift by +0.52 % (median +0.60 %, t 3.51, 1440 days). The effect survives trimming the 5 % tails on each side (t 4.03), is positive in all six coins (+0.23 % BTC to +0.90 % XMR, t 2.90) and in 7 of 8 years.
- **F2:** The effect is graded. The next decile up gives +0.26 % (t 2.12), the third +0.08 % (t 0.59), and the middle deciles about zero to negative. Across the 7056 down days, the Spearman correlation between the fall's size in volatility units and the next day's unusual return is +0.064.
- **F3:** Failed breakouts as the book defines them are not followed by any unusual 5-day move. On non-overlapping 5-day cells, failures show a mean unusual move of +0.002 % (169 cases) against -0.0001 % for all other cells (3250).
- **F4:** Sorting failures by breakout-day volume runs against the tested idea's grading. The thin tercile falls only 0.65 % (t -0.47, 57 cases) and the heavy tercile rises 0.87 % (t 0.72). Deep failures, closing furthest below the old high, rebound by +2.35 % (t 1.61, 57 cases).
- **F5:** Breakouts tend to continue rather than fail. A close above the prior 20-day high is followed over 5 days by +2.46 % above the coin's drift (t 2.19, 149 cases). This is only borderline given the many angles examined, is not graded by the breakout's size (terciles +2.1 %, +2.4 %, +2.7 %, each t near 1.5), and is mixed across years (negative in 2022, 2023 and 2025).
- **F6:** The book was short on only 2.3 % of bars (0.007 trades a day), so its result rests on very few positions.

## Ideas
- `029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline.g1_volatility-scaled-drop-next-day-rebound` (from F1, F2, F4): When a coin's daily close falls sharply against its own volatility of the previous 20 days, the coin rises over the next day. The larger the fall in units of that volatility, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
