---
line: 7.g patterns
backtest: 022-01_learned-combined-signal-score_1d
idea tested: 022-01_learned-combined-signal-score
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3722 USD
---
## Findings
- **F1:** The learned composite predicts slightly the wrong way, not merely weakly: its rank correlation with the coin's 5-day return beyond drift is negative on 5 of 6 coins (BTC -0.073, ZEC -0.053, ETH -0.037, XRP -0.028, LTC -0.013; XMR +0.022) and in 7 of 8 years. Its quintiles are not ordered (top quintile z +0.005, bottom +0.066, fourth -0.091 with t -2.53; about 655 grid cases each).
- **F2:** What a signal predicted over one year does not carry into the next. Correlating each coin's yearly rank correlation with the following year's gives -0.12 for the 28-day return, -0.08 for the 1-day reversal, -0.02 for nearness to the 90-day high and +0.07 for 30-day volatility (about 40 coin-year pairs each). Yet the yearly correlations themselves are sizeable, with mean absolute values of 0.10 to 0.12. The 365-day weights therefore chase relations that flip sign, which is the brief's own failure condition.
- **F3:** Taken alone, none of the four signals is graded on the 5-day grid. Mean rank correlations over coins are +0.019 (28-day return), -0.006 (1-day return), +0.004 (nearness) and +0.010 (volatility). Their only quintile t beyond 2 are isolated middle or edge quintiles: ret28 top +2.09, r1 second -3.69, near second -2.47. Given the 25 quintiles examined, these are no stronger than chance.
- **F4:** The book is net short in rising coins and loses through timing. It is short on 51 % of bars, with a mean allocation of -0.07 to -0.08 on every weekday. It loses on all 6 coins (-0.026 % to -0.108 % a day) while the coins rise (+0.067 % to +0.186 % a day). Drift explains only about -0.01 % a day of its -0.068 % mean, so the rest is timing and costs.
- **F5:** The next day's return depends on the weekday of the signal bar, but the effect is not stable.
- **F6:** Reversal after large 1-day falls is suggestive but not established. After falls beyond 2 standard deviations the next 5 days run +0.21 of a usual move above drift, with t 1.66 on only 67 cases. The neighbouring bins (-2 to -1 sd: +0.06, t 1.00; above +2 sd: +0.09, t 0.63) show no graded line.

## Ideas
- No ideas: Across the 25 signal quintiles, the weekday-by-coin, by-year and by-volatility tables, the persistence check and the large-move bins, nothing is graded and stands out from chance. The one strong pattern, the weekday effect in F5, is a fixed calendar condition that is neither graded nor stable across years and volatility levels, so it cannot be written as a graded idea.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
