---
line: 7.g patterns
backtest: 033-03_downside-break-continues-falling_1d
idea tested: 033-03_downside-break-continues-falling
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4064 USD
---
## Findings
- **F1:** On the non-overlapping 5-day grid of folds B and C (1,422 cases, 256 days), the close's place in its prior 20-day high-to-low range is graded against the next 5 days' return beyond the coin's drift: from the bottom fifth to the top fifth the excess is -1.55 %, -1.24 %, -0.35 %, +1.32 %, +2.20 %. The rank slope has a day-pooled t of 2.36, and the Spearman is positive on all six coins (0.095 to 0.137).
- **F2:** The gradient lives in calm markets, where the coin's 20-day swing is at or below its median. There the rank slope has t 3.28 (708 cases, 181 days), with fifths running -2.78 %, -2.19 % (t -2.48), -0.23 %, +1.53 %, +3.82 % (t 2.83). In agitated markets it is flat: slope t 0.61 (714 cases, 209 days), top fifth +1.31 % with t 0.80.
- **F3:** Closes above the prior 20-day high are followed by +5.10 % beyond drift over 5 days (t 2.14, 66 cases, 39 days). In calm markets the figure is +7.69 % (t 2.57, 43 cases, 24 days) and in agitated markets +0.26 % (t 0.10, 23 cases). Inside the breakout set, depth beyond the high is not graded (Spearman -0.14).
- **F4:** The tested situation does not continue. Closes below the prior 20-day low are followed by +1.27 % beyond drift (t 0.43, 53 cases, 22 days), and deeper closes rebound slightly more (Spearman of depth -0.17). The book's 15 best days came as the coins fell 10.1 % on average, and its 15 worst as they rose 8.8 %, so its result rests on a few crash and squeeze days.
- **F5:** The range-position slope does not stand out within any single window. Its per-window t runs from -0.85 to 1.04 across w7 to w18, so the pooled effect is small per case: about 0.1 rank correlation, roughly 0.05 to 0.1 of the usual 10.6 % 5-day move.
- **F6:** The other angles I checked do not survive this many looks. The 1-day, 5-day, 20-day and 60-day returns and the volatility level give slope t between -0.46 and 1.96. The weekday means have t at most 2.50 in magnitude and do not follow a coherent pattern.

## Ideas
- `033-03.g1_calm-range-position-drift` (from F1, F2, F5): In a calm market, the higher a coin's daily close sits within its range of the past 20 days, the more it rises over the next 5 days, and the lower it sits, the more it falls.
- `033-03.g2_calm-upside-break-continues` (from F2, F3): In a calm market, when a coin closes above its 20-day high, it rises over the next 5 days, and it rises more the further the close sits above that high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
