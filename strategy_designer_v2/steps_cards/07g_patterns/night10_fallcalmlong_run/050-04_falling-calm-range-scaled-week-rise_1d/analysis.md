---
line: 7.g patterns
backtest: 050-04_falling-calm-range-scaled-week-rise_1d
idea tested: 050-04_falling-calm-range-scaled-week-rise
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3756 USD
---
## Findings
- **F1:** In the falling calm bars (regime "unknown", 255 non-overlapping 3-day grid cases on 168 days), the 3-day unusual move rises with the 7-day return scaled by the 30-day mean daily range: Spearman 0.18 (p 0.007), from −2.28 % in the lowest fifth (t −1.41) to +1.50 % in the highest (t 1.43). No fifth has a t of 2.
- **F2:** The gradient in F1 comes from the sign of the week's move, not from its size. Among up weeks only (87 cases), Spearman is 0.10 (p 0.38) and the largest quarter (+0.94 %) is below the middle quarters (+2.24 %, +2.01 %). Among down weeks only (135 cases), Spearman is 0.04 (p 0.64). This agrees with step 5's supporting check, where the larger-forecast half minus the smaller-forecast half was −0.51 %.
- **F3:** The falling calm profile as a whole gives a long holder nothing above the drift: mean 3-day unusual move −0.29 % (day-pooled t −0.50, 255 cases), against a normal 3-day drift of +0.71 %.
- **F4:** Two other measures of where the price stands grade the move the same way as F1, with p-values that do not stand out once about ten measures have been looked at.
- **F5:** The result flips sign by year: 2018 −2.57 % (52 cases) and 2019 −1.70 % (105 cases), against 2020 +2.40 % (45) and 2021 +2.46 % (53). Coin means also range from −1.55 % (ETH) to +1.88 % (BCH), so no stable long effect is visible.
- **F6:** Several other angles showed no pattern that stands out (no |t| ≥ 2 with a monotone gradient):

## Ideas
- No ideas: In falling calm markets the only graded pattern (F1, F4) separates down weeks from up weeks rather than growing with the rise, and it has no fifth with t ≥ 2 and flips sign between 2018–2019 and 2020–2021 (F2, F5). Its nearness-to-high form is already held (035-01.b1), and no other angle looked at (F6) stands out from chance, so no long idea rests on these findings.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
