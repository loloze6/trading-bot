---
line: 7.b inconclusive
backtest: 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion_4h
idea tested: 027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3907 USD
---
## Findings
- **F1:** The tested idea comes out at zero, not short of the bar. On the plan's 14-day horizon its cases earn -0.24 % against the coin's normal drift (t -0.39, 1146 cases; my recount gives -0.05 %, t -0.09, 1289 cases). Yet the same cases earn +0.28 % over the next 1 day (t 1.97), so the move the idea points to shows sooner than the test measured it.
- **F2:** On each window's non-overlapping grid, sorting the bars that carry the raw panic value (a fall times the range multiple times the volatility ratio) by size shows the effect is graded but short-lived. The top fifth earns more than the coin's normal drift by +1.14 % over 1 day (t 7.7, 1692 cases), +1.91 % over 3 days (t 4.55, 561 cases), +2.14 % over 7 days (t 2.42, 245 cases) and only +2.59 % over 14 days (t 1.28, 116 cases).
- **F3:** Over 3 days the grading rises steadily across the fifths, from -0.95 % (t -2.72) in the smallest to -0.32 %, -0.52 %, +0.39 % and +1.91 % in the largest, with a rank correlation of 0.115 over 2805 cases. Over 14 days the three middle fifths sit at -2.8 %, -3.2 % and -2.5 % (t about -1.8 to -2.2), which cancels the top fifth and gives the test's zero.
- **F4:** The 14-day result is carried by the market's own long swings rather than by the panic. The top two fifths' 14-day excess swings from -10.4 % (t -4.16) in 2018 and -4.1 % in 2022 to +7.3 % in 2021. The 3-day excess of the same cases is positive in 7 of 8 years (2020 +2.97 % t 4.0, 2025 +2.62 % t 2.96, only 2022 at -0.12 %) and in all 6 coins (+0.57 % XMR to +2.39 % ZEC, ZEC t 2.53).
- **F5:** Inside the tested cases the volatility-ratio condition orders the 14-day move. The top quarter of volatility ratio earns +5.48 % (t 2.16, 144 cases) and the bottom quarter -3.47 % (t -2.00, 144 cases). This agrees with the idea's grading, but at 14 days it rests on few cases.
- **F6:** The short horizon is large enough to pay. The top fifth's 3-day excess of +1.91 % is about 10 times the 0.19 % cost of a trade. The 14-day total move of +1.87 % per case is mostly the coin's normal drift (+2.10 %), not the panic.

## Ideas
- `027-01_panic-range-multiple-rebound.d1_panic-inside-volatility-expansion.b1_panic-rebound-within-three-days` (from F1, F2, F3, F4, F6): When a coin falls over a 24-hour stretch and its high-low range over that stretch is a large multiple of its average 24-hour range over the past 30 days, while its volatility over the past 7 days is high against its volatility over the past 60 days, it earns more than its usual return over the next 3 days, and the larger the range multiple times that volatility ratio, the higher the return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
