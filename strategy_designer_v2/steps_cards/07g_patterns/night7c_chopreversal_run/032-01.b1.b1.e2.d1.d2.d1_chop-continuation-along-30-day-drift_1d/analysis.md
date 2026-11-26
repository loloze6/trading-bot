---
line: 7.g patterns
backtest: 032-01.b1.b1.e2.d1.d2.d1_chop-continuation-along-30-day-drift_1d
idea tested: 032-01.b1.b1.e2.d1.d2.d1_chop-continuation-along-30-day-drift
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4363 USD
---
## Findings
- **F1:** Where the 30-day efficiency ratio is below 0.3 and the 7-day and 30-day returns share a sign, the next 7 days' unusual move, signed by the 30-day direction, averages +3.77 % (t 3.08 with same-day cases pooled, 344 cases on 120 days). Regressed on the 30-day return scaled by daily swings (r30 / (30-day daily std × √30)), it gives a slope of 0.052 with t 4.87. The 7-day scaled move the book uses gives a slope of 0.043 (t 4.24) in the .15–.3 band and 0.030 (t 2.57) below .15.
- **F2:** The continuation depends on chop. The agreeing cases earn +2.88 % (t 2.94, n 171) at efficiency below .15 and +4.64 % (t 3.95, n 173) at .15–.3. They turn to −1.23 % (t −0.84, n 156) at .3–.5 and −0.79 % (n 36) above .5. Across all bars, following the 30-day direction earns only +1.42 % (t 1.54, 859 cases).
- **F3:** Inside agreeing chop the gain grows with the size of the 7-day scaled move. By tercile of its absolute value it is +1.57 % (t 1.20, n 104), +3.68 % (t 2.84, n 128) and +5.89 % (t 4.39, n 112). The non-agreeing chop cases show no grading: +1.25 %, −1.38 % and +0.85 %, all with |t| ≤ 1.2.
- **F4:** The book's short trades lose and its long trades pay. 1143 shorts average −1.59 % net (median −2.42 %); shorts held 8 days or less average −4.44 % (n 739). 1028 longs average +4.86 %. Yet the chop down-side cases have a positive unusual move of +3.1 % to +3.5 % in each volatility tercile (t 1.09–1.35). So the shorts' loss is the coins' upward drift and the timing of exits, not a missing edge.
- **F5:** The effect is uneven over the years. The agreeing-chop cases earn +1.75 % (t 1.03) in 2018 and +0.95 % (t 0.91) in 2019, then +5.36 % (t 3.47) in 2020 and +6.51 % (t 3.99) in 2021.
- **F6:** Other angles showed nothing beyond chance with same-day cases pooled:

## Ideas
- `032-01.b1.b1.e2.d1.d2.d1.g1_chop-drift-scaled-continuation` (from F1, F2, F3): When a coin's past 30 days have gone back and forth with little net progress against the sum of its daily moves, and its 7-day move points the same way as its 30-day net move, the coin keeps moving in the direction of that 30-day net move over the next 7 days. The larger the 30-day net move counted in the coin's 30-day daily swings, the larger the move that follows.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
