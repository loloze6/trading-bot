---
line: 7.g patterns
backtest: 035-01_nearness-to-high-rises_1d
idea tested: 035-01_nearness-to-high-rises
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4165 USD
---
## Findings
- **F1:** The effect lives only near or above the 20-day high: a piecewise regression of the 5-day excess return on the raw distance in daily swings, broken at the median distance of −1.6, gives a slope of 0.027 (t 2.03, clustered by day) on the near side and 0.0013 (t 0.29) on the far side. In quintiles, the nearest quintile (−0.6 to +3.9 swings) has +2.17 % (t 2.07, 485 grid cases), while the three farthest quintiles sit flat at −0.8 % to −1.2 % with no grading among them.
- **F2:** Nearness grades the drift in every trend, but most steeply in a choppy market. By 60-day trend, the near tercile is positive everywhere: choppy +7.9 % (t 1.38, 70 cases), falling +2.6 % (t 2.32, 90), rising +2.5 % (t 2.67, 240). The far tercile is negative everywhere, deepest in a choppy market at −7.8 % (t −3.72, 51). The slope on raw distance is 0.043 (t 1.93) in a choppy market, 0.015 (t 2.05) in a rising one and 0.002 (t 0.45) in a falling one.
- **F3:** Nearness is not separable from recent momentum in these folds. With the last day's swing-scaled return and the 20-day swing-scaled return in the same regression, the raw distance keeps its slope (0.0089 against 0.0082 alone) but its t falls from 2.08 to 1.58. Neither control is significant (t 0.88 and −0.46).
- **F4:** The book is almost all timing, and its small net position holds it back. Its mean daily return is 0.072 %, of which only 0.013 % comes from the market's own rise, with a mean net allocation of 0.05. Its returns are convex in the market's day: −0.11 % on the worst fifth of days against +0.42 % on the best fifth.
- **F5:** The idea's move covers the cost of trading it. The total move is +1.24 % per case over 5 days against a cost of 0.22 % per trade. The book failed only on mean daily return on days in a position (0.00047 against 0.0005), because about 99 % of coin-days hold a position, including the far cases that F1 shows add nothing.

## Ideas
- `035-01.g1_near-high-side-carries-drift` (from F1, F4, F5): The further a coin's daily close stands above its prior 20-day closing high, or the less it sits below it, measured in its own 20-day daily swing, the more the coin rises over the next 5 days. Closes that sit well below the high show no grading of their drift.
- `035-01.g2_choppy-market-nearness-to-high` (from F2, F1): In a choppy market, the fewer daily swings a coin's daily close sits below its 20-day closing high, the more the coin rises over the next 5 days. The further below, the more it falls.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
