---
line: 7.b inconclusive
backtest: 050-02.b1.d2_scaled-rise-strong-case_1d
idea tested: 050-02.b1.d2_scaled-rise-strong-case
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3451 USD
---
## Findings
- **F1:** The test's result points the idea's way but fails its grading check: the mean unusual 3-day move is +0.96 % (t 2.39, 297 days, 410 cases), yet the Spearman correlation between forecast and move is −0.022, so the larger forecasts did not carry more over 3 days.
- **F2:** In the explore half (97 cases on BCH, ETH, XMR and ZEC), the carry keeps building past the plan's 3 days, and so does its grading. The mean unusual move is +0.17 % (t 0.43) at 1 day, +1.54 % (t 2.48) at 3 days, +2.34 % (t 2.45) at 5 days and +2.92 % (t 2.29) at 7 days. The forecast's Spearman with the move rises with the horizon: 0.089 at 3 days, 0.133 at 5 days and 0.168 at 7 days.
- **F3:** At 3 days the idea's own measure, the 7-day rise in units of the 30-day swing, does not grade the move (Spearman 0.015). By scaled-rise quartile the 3-day means are 0.1 %, 1.7 %, 0.7 % and 0.5 %. At 7 days the same quartiles give 1.8 %, 2.5 %, 2.3 % and 3.9 %, and the top quartile is the only one with t ≥ 2 (t 2.27, 18 cases).
- **F4:** The forecast's grading is compressed at the top: 35 % of cases sit at the cap of 20. Those capped cases end only +1.41 % at 3 days (t 1.31, 34 cases), against +1.61 % (t 2.10, 63 cases) for the rest. The top forecast quintile, all at 20, is flat (+0.20 %, t 0.14). At 3 days the strongest signals carry no more than the weaker ones.
- **F5:** The effect is uneven across coins and years, so it is mixed rather than absent. At 3 days, BCH +2.4 % (t 1.75), XMR +1.9 % (t 1.46) and ETH +1.6 % (t 1.30) are positive, while ZEC is +0.4 % (t 0.41). At 7 days ZEC is −0.5 % (t −0.20). By year, 2020 is +3.0 % (t 2.43) and 2021 +2.8 % (t 2.36), against 2019 at −0.1 % (t −0.14).
- **F6:** The move is large against what a trade costs: the total move per case is 4.2 times the 0.31 % cost and the unusual move 3.1 times. The book's failure on Calmar (0.28) comes from the effect's unevenness, not from a move too small to pay.

## Ideas
- `050-02.b1.d2.b1_scaled-rise-week-carry` (from F1, F2, F3, F4): In a falling, calm market, a coin that has risen over the last 7 days keeps rising over the next 7 days, and rises further the larger its 7-day rise is in units of its 30-day daily-return swing, so that the largest scaled rises carry the most.
- `050-02.b1.d2.b2_scaled-rise-more-coins` (from F1, F5): In a falling, calm market, a coin that has risen over the last 7 days keeps rising over the next 3 days, and rises further the larger its 7-day rise is in units of its 30-day daily-return swing, so that the largest scaled rises carry the most.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
