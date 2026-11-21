---
line: 7.b inconclusive
backtest: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins_4h
idea tested: 019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.4296 USD
---
## Findings
- **F1:** The result is inconclusive because of how the forecast was built, not because the effect is weak. The standardised forecast hits its cap of 20 on 89 % of the 3,662 cases (median 20), so step 5's median split put all 3,662 cases in the smaller half and none in the larger. Split instead at the median of the raw break (0.41 of the 30-day average 4h range), the larger breaks gain +1.60 % unusual move over 6 days and the smaller ones -0.21 %, a difference of +1.82 % (Welch t 3.25, 1,692 vs 1,693 cases).
- **F2:** The gain sits in the largest breaks only. By quintile of the raw break, the unusual move is -0.54 %, -0.38 %, +0.87 %, +0.63 % and +2.88 % (t -1.18, -0.67, 1.18, 1.33, 3.57; 677 cases each; top quintile's mean break 1.95 ranges). Spearman between break size and the scaled move is only 0.07, so the grading is steep at the top and flat below it.
- **F3:** The size of the coin's 7-day rise carries a second gradient, also only at its top. By 7-day-return quintile the unusual move is -0.10 %, +0.92 %, -0.57 %, -0.15 % and +3.75 % (t 3.55, 682 cases, mean 7-day return +27 %). The two combine: the top tercile of break and of 7-day rise earns +3.65 % (488 cases), against -0.72 % to +0.50 % in most of the low-break cells.
- **F4:** The large-minus-small break difference holds across the data, with years and coins that go against it. It is positive in 7 of 8 years (largest +6.8 % in 2021; -1.4 % in 2025) and in 13 of 19 coins (68 %). The overall effect is mixed by market year: +2.6 % (t 3.83) in 2020, +4.4 % in 2021, +1.6 % in 2023, against -2.7 % (t -4.48) in 2022 and -0.9 % in 2025.
- **F5:** The main measure is on the side the idea predicts and already uses all the data available: +0.77 % unusual move over 6 days, t 2.85, 3,662 cases, all 19 coins and all four folds. It builds from 3 days (+0.43 %, t 3.13) to 6 days (+0.77 %) and stops growing at 12 days (+0.81 %, t 2.00). Its size, 3.4 times the 0.22 % cost of a trade on the unusual move alone, sits within the paying range of findings F10 and F11.

## Ideas
- `019-03_upward-breakout-quiet-continuation.b2_large-breakout-in-rising-week.b2_large-breakout-six-day-continuation.b1_two-day-breakout-more-coins.b1_large-break-in-steep-week` (from F1, F2, F3, F4, F5): When a four-hour bar closes above the highest high of a coin's preceding two days, only while the coin's 7-day return is positive, the coin rises over the next six days. The farther that close sits above the two-day high, measured in the coin's 30-day average four-hour range, and the larger the coin's 7-day rise, the larger the rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
