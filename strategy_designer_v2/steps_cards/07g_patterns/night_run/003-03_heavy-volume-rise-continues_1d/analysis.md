---
line: 7.g patterns
backtest: 003-03_heavy-volume-rise-continues_1d
idea tested: 003-03_heavy-volume-rise-continues
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5219 USD
---
## Findings
- **F1:** The book earns almost nothing because it is mostly out of the market: mean daily return 0.000053 against 0.00119 for holding the coins, mean position 0.116 and a position on only 23.5 % of days; of the position's 0.000242 daily gain before costs, 0.000137 comes from the market's own rise and only 0.000104 from timing.
- **F2:** On the non-overlapping 5-day grid, the size of a one-day rise predicts the 5-day excess return more than its volume does: among up days with z > 0.3 (n=950), Spearman(z, excess) is 0.086 (p=0.008) and is positive in all 6 coins (0.013 to 0.149); in a joint fit, z has t=1.76 while log relative volume has t=0.71.
- **F3:** The excess return rises step by step with the day's move in usual units: z in (0.3, 1] gives −0.0001 (n=570), z in (1, 2] gives +0.0155 (t=2.38, n=286) and z > 2 gives +0.0258 (t=1.76, n=94); down and flat days show nothing comparable.
- **F4:** Continuation after large rises fails in falling years: the 5-day excess on forecast ≥ 5 bars is −0.0292 (t=−1.94, n=41) in 2018 and −0.0191 (t=−1.56, n=42) in 2022, against +0.02 to +0.05 with t near 2 in 2019, 2021, 2023 and 2024; LTC and XMR are slightly negative overall (−0.0053, −0.0037).
- **F5:** After down days, thin volume is followed by further falls: excess is −0.0112 (t=−2.02, n=347) in the thinnest third of relative volume, −0.0056 in the middle third and +0.0013 in the heaviest third; Spearman(rv, excess) is 0.068 (p=0.029, n=1036), positive in 4 of 6 coins. The volume term weakens to t=1.33 once the fall's size is included, and the pattern is strongest in 2018 and 2019. This is the opposite of the brief's reversal of thin-volume moves.
- **F6:** Saturday's daily return averages 0.0045 (t=5.53, n=2484) and beats the other days in 5 of 6 coins (LTC t=2.67, XMR t=2.01) and 7 of 8 years. It is a calendar condition with no grading, so no idea is drawn from it.

## Ideas
- `003-03_heavy-volume-rise-continues.g1_rise-size-drives-continuation` (from F2, F3, F1): The larger a coin's one-day rise measured against its typical daily move over the past 20 days, the larger its gain over the next 5 days, whatever the day's volume.
- `003-03_heavy-volume-rise-continues.g2_thin-volume-falls-keep-falling` (from F5): The thinner a coin's volume on a one-day fall, compared with its own 30-day average daily volume, the more the coin keeps falling over the next 5 days.
- `003-03_heavy-volume-rise-continues.g3_rises-continue-in-uptrends` (from F4, F3): The further a coin stands above its own price of 60 days earlier, the larger its further gain over the next 5 days after a large one-day rise, measured against its typical daily move over the past 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
