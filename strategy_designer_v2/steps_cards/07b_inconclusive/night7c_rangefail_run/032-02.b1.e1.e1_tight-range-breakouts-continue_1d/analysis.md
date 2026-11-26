---
line: 7.b inconclusive
backtest: 032-02.b1.e1.e1_tight-range-breakouts-continue_1d
idea tested: 032-02.b1.e1.e1_tight-range-breakouts-continue
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3692 USD
---
## Findings
- **F1:** The test graded the bet by its standardised forecast, which compares the range's narrowness with the coin's own last 61 values, and that grading carries nothing (step 5's slope -0.0034, clustered t -0.57 over 255 cases on 196 days; in folds B and C the forecast's clustered slope t is 0.42 over 129 cases on 92 days). The unstandardised narrowness, 1/(1 + 60-day closing range in mean absolute daily moves), carries the grading the idea names (clustered slope t 2.02, Spearman 0.21 over the same 129 cases), and its rank correlation with the forecast is only 0.64.
- **F2:** Graded by the unstandardised narrowness, the tightest third of breaks shows the rise and the other two thirds show none: unusual 20-day move +8.8 % (t 2.10, strength 0.34, 70 % up) in the tightest third, +0.7 % in the middle third and -0.1 % in the widest third, 43 cases each. On the 47 cases with a full 60-day history inside the window, the range in usual moves gives the same order (lowest third +21.6 % with t 2.95, highest third +8.5 % with t 1.43).
- **F3:** The coin's run into the break grades the rise against its size: the 20-day return before the break has a clustered slope of -0.28 (t -2.92, 97 cases on 69 days) and the 1-day return a clustered slope t of -3.36 (123 cases). Breaks after the smallest 20-day run gain +11.2 % unusual (t 2.44, 72 % up) against +0.1 % after the largest (32 and 33 cases).
- **F4:** The breaks rise on average (mean unusual move +4.83 %, t 2.04, 196 days; strength 0.179), but the rise is mixed across years: +8.2 % in 2019 (t 2.84), +10.0 % in 2020 (t 2.55), -4.0 % in 2021 and -26.4 % in 2018 (6 cases). The narrowness grading also changes sign by year (Spearman -0.27 in 2019, +0.43 in 2020, +0.36 in 2021), though it is positive on all six coins (0.14 to 0.39). This is why no single slope is clear.

## Ideas
- `032-02.b1.e1.e1.b1_absolute-tight-range-breakouts-continue` (from F1, F2, F4): In a coin that closes above its prior 60-day closing high, the narrower that 60-day range of closes, counted in the coin's mean absolute daily moves over the same 60 days and not compared with the coin's own past ranges, the larger the coin's rise over the next 20 days.
- `032-02.b1.e1.e1.b2_quiet-approach-breakouts-continue` (from F3, F4): In a coin that closes above its prior 60-day closing high, the smaller its 20-day return into that close, the larger the coin's rise over the next 20 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
