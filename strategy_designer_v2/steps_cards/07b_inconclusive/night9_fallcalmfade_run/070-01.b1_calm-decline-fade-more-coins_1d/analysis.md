---
line: 7.b inconclusive
backtest: 070-01.b1_calm-decline-fade-more-coins_1d
idea tested: 070-01.b1_calm-decline-fade-more-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3524 USD
---
## Findings
- **F1:** Over all folds, step 5's main measure sits at zero: the mean next-day move beyond drift on the short side is +0.04 % (t 0.24, 1667 cases on 658 days), a strength of 0.011. In folds B and C it is +0.50 % with a day-summed t of 1.81 (570 cases, 276 days; strength 0.096, t 1.94), so the effect is uneven across the folds.
- **F2:** The cases are diluted by the shortest runs. Up days after a 1-day run make 276 of the 570 cases in folds B and C, and their next-day move beyond drift is +0.04 % (t 0.10). After runs of 2, 3, 4 and 5+ days it is +0.80 %, +0.33 %, +1.34 % and +2.42 %; the 5+ group has a t of 3.44 on 39 cases over 33 days.
- **F3:** The depth of the run's fall grades the giveback better than its length. In folds B and C, the deepest quarter of runs (mean run fall -14.6 %) is followed by a next-day fall of +2.08 % beyond drift (t 3.74, 139 cases, 74 days). The two middle quarters give +0.01 % and +0.35 %, and the shallowest quarter (run fall -1.1 %) gives -0.39 % (t -0.78). The correlation of the run's fall with the next-day short return is -0.20, against +0.12 for the run's length in days.
- **F4:** Longer runs give the larger fall in every year, but the effect depends on the period. Runs of 3+ minus runs of 1-2 is +1.98 % vs +1.07 % in 2018, +0.42 % vs +0.24 % in 2019, +0.13 % vs -0.67 % in 2020 and +0.81 % vs -0.57 % in 2021. Over all folds, step 5's Welch t for longer minus shorter is -2.14.
- **F5:** The fall after long runs shows on most coins and is not carried by one. For runs of 3+ days, the mean next-day short return beyond drift is +5.0 % on ADA (7 cases), +1.8 % on BTC (17), +1.2 % on ETH (21, t 2.09), +2.0 % on XMR (17, t 2.10) and +1.0 % on ZEC (24), with LTC (+0.26 %) and XRP (+0.03 %) near zero.
- **F6:** The move after the deepest runs is not small against costs. In the deepest quarter it is about 9 times the 0.22 % cost of a trade, while the all-case unusual move of +0.04 % is 0.2 times the cost. A test of every run-break day cannot pay whatever its sizing.

## Ideas
- `070-01.b1.b1_calm-decline-depth-fade` (from F1, F2, F3, F4, F5, F6): In a falling, calm market, a day that closes up after an unbroken run of down days is followed by a fall over the next day, and the deeper the total fall of that run of down days, the larger the next day's fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
