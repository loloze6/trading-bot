---
line: 7.b inconclusive
backtest: 027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation_4h
idea tested: 027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3805 USD
---
## Findings
- **F1:** The tested result is not on the idea's side, and it does not grow with the forecast. Step 5's mean unusual 78-bar move is -0.53 % per case (t -0.81, 692 cases, weighted check -0.18 %). In my approximate rebuild of the cases (592 with a complete 78-bar return), the Spearman correlation between the forecast and the unusual move is 0.027 (p 0.51). By forecast quartile the means are -2.04 % (t -1.79), -0.33 %, -0.86 % and +2.12 % (t 1.02).
- **F2:** The cases' small mean comes from one year, which hides a negative result everywhere else. In 2020 alone the mean unusual move is +12.3 % (t 4.38, 45 cases); without 2020 it is -1.29 % (t -1.70, 547 cases). 2018 is -5.40 % (t -2.78, 114 cases) and 2022 is -1.81 % (t -1.19, 122 cases).
- **F3:** Measured on the bars, panics that come after a deep 30-day fall are followed by a clear premium, and the premium is graded by the depth of that fall. I took the first panic bar in each 78-bar cell (24-hour fall in usual moves times range multiple above 3) and measured the coin's return from one day after the panic to 14 days after it, minus the coin's drift.
- **F4:** The 90-day condition the idea uses points the same way but rests on too few cases. Only 30 % of the cases have a 90-day prior return that can be measured inside their window. Among those, the deepest quartile (mean -51 %) has +6.6 % (t 1.63, 36 cases), against -2.9 % to -4.0 % (t ≈ -1.6 to -1.8) in the other three quartiles.
- **F5:** The panic's own severity does not grade the later move. Across all panics, the Spearman correlation between the panic score and the move from one day to 14 days after is -0.030 (p 0.48). By panic-score tercile the unusual moves are +1.88 %, -0.12 % and +1.14 %.
- **F6:** The unconditional panic premium is small and carried by two years. Over all panics it is +0.98 % (t 1.31, 534 cases, strength 0.045). Without 2021 (+6.8 %, t 2.11) and 2024 (+6.7 %, t 2.89) it is -0.71 % (t -0.90, 384 cases).

## Ideas
- `027-04_panic-delayed-recovery-drift.d1_panic-premium-after-capitulation.b1_panic-after-30-day-slide` (from F3, F4, F1, F5): After a 24-hour panic stretch, the coin's return from one day after the stretch ends to 14 days after it is higher than usual, only while the coin's 30-day return before the stretch is deeply negative; the deeper that 30-day fall, the higher this later return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
