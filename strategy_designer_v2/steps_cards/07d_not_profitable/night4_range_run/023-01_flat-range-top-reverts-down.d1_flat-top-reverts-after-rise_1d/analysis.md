---
line: 7.d not profitable
backtest: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise_1d
idea tested: 023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5735 USD
---
## Findings
- **F1:** The book loses because its shorts lose. Its 895 cases with a forecast of -2 or lower moved -0.77 % per 5 days against the short after drift (t -1.85). The total move per case was -0.79 %, that is -4.1 times the 0.19 % cost of a trade. The book's Sharpe was -1.08 and its mean daily return -0.058 %, so no change of sizing or holding can make it pay.
- **F2:** Inside the 90-day-rise regime the close's place in its 30-day range predicts continuation, not reversion. The 5-day unusual move was +1.14 % at the top of the range (t 1.99, n 495) and +0.77 % in the upper part (t 1.30, n 246). It was -1.44 % in the lower part (t -2.39, n 186) and -1.48 % at the bottom (t -1.57, n 182). Grading the deviation by the cube of the flatness gives the same pattern: the lowest two quintiles had -1.26 % (t -2.07) and -2.39 % (t -3.25), and the fourth had +1.19 % (t 2.08).
- **F3:** The flatness factor lets mostly trending months into the cases. Only 15.6 % of the cases fall in the flattest fifth of months, and that fifth is the only one where the short gains: +0.70 % (t 0.90, n 109). The other four fifths lose between -1.02 % and -1.50 % per case.
- **F4:** In the 90-day-rise regime, the shorts that lose most are closes above the middle in the most trending fifth of months: -1.68 % per case (t -1.93, n 238). Closes above the middle in the flattest fifth earn +0.54 % (t 0.64, n 90). At the very top of the flattest fifth the coin fell 3.34 % against drift (t -2.84, n 38), against +1.68 % at the top of the most trending fifth.
- **F5:** In the 90-day-rise regime and the two most trending fifths of months, a close far from the middle kept going its own way. The far third moved +2.32 % per 5 days after drift (t 2.05, n 183), +2.75 % in total, about 14 times the cost of a trade. The middle third moved +1.85 % (t 1.71, n 160) and the near third +0.13 % (t 0.18, n 180).
- **F6:** That continuation in trending months during a 90-day rise held in 6 of 8 years: 2019 +2.3 %, 2020 +4.1 %, 2021 +1.3 %, 2022 +0.4 %, 2024 +1.5 % and 2025 +0.9 %. The exceptions were 2018 (-6.3 %, n 25) and 2023 (-1.0 %).
- **F7:** Taken over all regimes, the flattest two fifths of months show no graded reversion. The far third from the middle reverted 0.00 % (t 0.01, n 341) and the slope of the unusual move on range position there was +0.0042 (t 0.75, n 1022). The reversion in F4 is therefore narrow, not a broad effect.

## Ideas
- `023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.d1_reversion-only-near-zero-net-move` (from F3, F4, F7): In a coin whose 30-day net move has been small relative to its 30-day high-low range, the further its close sits above the middle of that range, the more it falls over the next 5 days, only while its 90-day return is positive, and the more so the closer its 30-day net move is to zero, so that the fall shows only in the flattest months.
- `023-01_flat-range-top-reverts-down.d1_flat-top-reverts-after-rise.d2_range-position-momentum-in-uptrends` (from F2, F4, F5, F6): In a coin whose 90-day return is positive, the higher its close sits in its 30-day closing range, the more it rises over the next 5 days, and the more so the larger its 30-day net move relative to that range.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
