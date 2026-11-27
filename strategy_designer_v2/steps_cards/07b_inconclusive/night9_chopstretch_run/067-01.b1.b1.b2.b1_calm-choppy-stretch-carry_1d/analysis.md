---
line: 7.b inconclusive
backtest: 067-01.b1.b1.b2.b1_calm-choppy-stretch-carry_1d
idea tested: 067-01.b1.b1.b2.b1_calm-choppy-stretch-carry
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3523 USD
---
## Findings
- **F1:** The tested slope is on the predicted side but small and unsure: 0.000985 per forecast unit with day-clustered t 1.22 over 514 grid cases. The idea's unusual move is +0.25 % per case over 10 days (t 0.41 over 566 days), only 0.016 of the coin's usual 15.92 % move. That is under the 0.05 typical of real ideas, and the unusual move is only 1.1 times the 0.22 % cost of a trade.
- **F2:** In folds B and C the carry lives in one year only. On the 10-day grid the forecast slope is +0.0087 (clustered t 3.59, 33 cases over 15 days) in 2021, against −0.0062 (t −2.55) in 2018, −0.0011 (t −0.54) in 2019 and −0.0012 (t −0.42) in 2020. Without 2021 it is +0.00089 (t 0.65, 81 cases over 40 days).
- **F3:** The shorter horizon shows the same thing. At 5 days the slope looks stronger overall (+0.0021, clustered t 2.24, 236 cases over 114 days), but 2021 alone carries it (t 2.85, mean move in the stretch's direction +6.2 %). The other years together give +0.00049 (t 0.75, mean move in the stretch's direction +0.4 %).
- **F4:** The 10-day mean move in the stretch's direction is mixed across windows. It is negative in w8 (−2.5 %), w9 (−0.2 %) and w10 (−5.2 %), and large in w12 (+9.6 %) and w18 (+16.4 %). The pooled grading over raw-stretch quintiles (mean 10-day move from −6.6 % in the lowest to +5.9 % in the highest) therefore comes from a few windows, not from a steady effect.
- **F5:** The effect is not confined to one side, one coin or the strongest stretches either:

## Ideas
- No ideas: The test already used all the daily data available (folds A–D, all 19 coins). Its positive but weak slope comes from one year, 2021 (t 3.59), while 2018–2020 show nothing or reversion (2018 t −2.55). No coin, side, stretch size or horizon carries the effect apart from that period, so no amendment of the idea would give a clearer answer.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
