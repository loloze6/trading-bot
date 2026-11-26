---
line: 7.g patterns
backtest: 031-03_uprun-size-scales-wide-flat-reversal_1d
idea tested: 031-03_uprun-size-scales-wide-flat-reversal
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4006 USD
---
## Findings
- **F1:** The tested reversal shows up in no form. Long-side 5-day unusual moves after wide flat days (range at least 1.5× the 20-day mean, body at most 10 %) that follow a 5-day rise average +2.33 % (t 1.65, 68 cases on 59 days), so the coin kept rising rather than falling. Within the book, the 149 trades lost 4.76 % on average after fees, with only 23 % winners; five of six coins averaged negative (best XRP +0.47 %, worst XMR −10.5 %).
- **F2:** The run's size does not grade the move after a wide flat day. Spearman rho between the standardised 5-day run (z5) and the next 5-day unusual move is 0.08 (p 0.41, 102 cases). Only the top quartile (z5 2.4) stands apart, with +4.98 % in the run's direction (t 2.07, 26 cases on 23 days). One cell out of four, among many tested, is not distinguishable from chance.
- **F3:** Wide days with a firm body are followed by a move in the body's direction that grows weakly with the body: +0.01 %, +0.74 %, +0.61 % and +1.41 % over 5 days across |body| quartiles 0.24 to 0.87 (largest t 1.32, about 320 cases each). By year the sign flips: 2018 +2.9 %, 2022 −0.2 %, 2023 −0.7 %, 2025 −1.3 %.
- **F4:** On the non-overlapping 5-day grid, the following 5-day unusual move is never separated from 0 when split by the prior 5-day standardised return (top quintile +0.91 %, t 1.24), the 20-day return (largest t 1.25), the volatility ratio (top quartile +0.98 %, t 1.14), today's move size in its own direction (largest t 1.73), or close location on wide days (largest t 1.40).
- **F5:** Saturday's 1-day unusual return is +0.34 % (t 2.24, 2484 coin-days), with t 1.67 and 1.73 in the two halves of the years. Weekdays run −0.30 % to +0.21 %. This is the only |t| above 2 among roughly 40 cells examined, which is about what chance alone would produce.
- **F6:** The book traded on only 5 % of the coins' days, at 0.0081 trades per day. Its total move per case (−1.94 %) is 10 times the 0.19 % cost of a trade, against it.

## Ideas
- No ideas: Across the flat-day, wide-day, run-size, volatility, close-location, move-size, yearly and weekday angles (about 40 groups), no pattern stands out beyond |t| ≈ 2, which is what chance gives over that many looks. The loose hints of 5-day continuation (F2, F3, F4) are not strong or stable enough across years to support a new idea.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
