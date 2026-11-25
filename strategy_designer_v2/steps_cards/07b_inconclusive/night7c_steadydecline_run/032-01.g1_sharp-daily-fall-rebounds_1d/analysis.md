---
line: 7.b inconclusive
backtest: 032-01.g1_sharp-daily-fall-rebounds_1d
idea tested: 032-01.g1_sharp-daily-fall-rebounds
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3403 USD
---
## Findings
- **F1:** The tested result points the way the idea predicts but falls short of the bar: the mean excess 2-day return over all folds is +0.22 % (t 0.51, 463 cases on 191 days, slope t 0.33). On folds B and C the same cases (one per 2-day cell, 20-day z ≤ −2) give +1.23 % over 2 days and +1.24 % over 1 day, but with cases on one day taken together the t is only 1.55 and 1.43, because the 184 cases fall on only 74 days.
- **F2:** The effect lasts 1 to 2 days and then fades. The excess return is +1.24 % (naive t 2.53) over 1 day and +1.23 % (t 2.52) over 2 days, then +0.44 % (t 0.67) over 3 days and −0.56 % (t −0.60) over 5 days, so the plan's 2-day horizon is where the effect shows.
- **F3:** The effect is mixed across periods and is drowned in one of them.
- **F4:** The rise is positive on every coin but significant on none. The 2-day means run from +0.46 % (ETH, t 0.41) to +1.98 % (XRP, t 1.34), with 25 to 35 cases per coin, so each coin adds too few cases on its own.
- **F5:** The grading is weak and not monotone, which is why the slope fails.
- **F6:** No split by trend explains the result.
- **F7:** In size the move is close to the cost of a trade. The unusual move of +0.22 % per case is 1.2 times the 0.19 % round-trip cost, with a strength of 0.037 of a usual 2-day move (6.58 %).

## Ideas
- `032-01.g1.b1_sharp-fall-rebound-more-coins` (from F1, F2, F4, F7): When a coin's daily return is a fall that is large against its own typical daily move over the past 20 days, the coin rises over the next 1 to 2 days, and the larger that fall in units of its typical daily move, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
