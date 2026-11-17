---
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways_1d
idea tested: 011-01_weekend-rise-reverses-monday.d1_weekend-moves-reverse-both-ways
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4631 USD
---
## Findings
- **F1:** The reversal after a weekend move shows mainly in the middle-sized moves, not the largest. Ranked by |weekend z| in fifths, the 2-day reverse move in units of usual daily moves is 0.05 (t 0.53), 0.30 (t 3.12), 0.37 (t 4.28), 0.10 (t 1.19) and -0.07 (t -0.73) per fifth, about 410 cases each. That is why the top third by |forecast| loses to the bottom third (-0.019 vs 0.121 vol units; raw 0.0030 vs 0.0069), and why the supporting check fails even though the main t is 2.75.
- **F2:** The share of cases that reverse also peaks in the middle. It is 0.52, 0.57, 0.60, 0.57 and 0.55 across the |z| fifths. Larger weekend moves therefore do not bring larger or more reliable moves back, and the correlation of |z| with the volatility-scaled reversal is -0.048.
- **F3:** The reversal itself is real and is tied to the weekend at 2 and 3 days. The return-signed 2-day excess, -z × excess, has t 2.40 on Sundays and between -0.93 and 1.43 on every other weekday. At 3 days it has t 3.01 on Sundays and between -1.46 and 0.68 elsewhere. At 1 day, Monday's move after Sunday (t 2.80) is matched by Tuesday, Wednesday, Thursday and Saturday (t 2.04 to 3.28).
- **F4:** Weekend volume does not grade the effect, contrary to the brief. The 2-day reversal by quintile of Sunday volume relative to the 28-day mean runs 0.0076, 0.0116, 0.0051, 0.0086 and 0.0077, and its rank correlation with relative volume is -0.007. Relative volume is also correlated 0.41 with |z|, so it mostly stands in for the size of the move.
- **F5:** The main value is positive in 7 of 8 years and in all 6 coins, but only reaches t ≥ 2 in XMR (2.61), 2020 (2.06) and 2025 (2.46). It is larger after weekend rises (t 2.49) than after weekend falls (t 1.30).

## Ideas
- No ideas: The weekend reversal is present but only as a sign effect that peaks for moderate weekend moves and fades for the largest ones (F1, F2), and relative volume adds no grading either (F4). No graded version of the idea fits these results, and more data is unlikely to rescue the grading that the data already contradicts.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
