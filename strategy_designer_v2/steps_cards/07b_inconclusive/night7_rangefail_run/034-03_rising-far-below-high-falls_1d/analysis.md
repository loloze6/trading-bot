---
line: 7.b inconclusive
backtest: 034-03_rising-far-below-high-falls_1d
idea tested: 034-03_rising-far-below-high-falls
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3952 USD
---
## Findings
- **F1:** The test's result is on the idea's side but nowhere near the bar, and the rising profile holds no effect to find. Step 5's pooled slope was +0.00029 with t 0.64 over 2,350 cases, and the deep group (forecast ≤ −10, 1,174 cases) had a mean excess 5-day return of +0.05 %, so the supporting check failed. In folds B and C, rising-market cases below the 20-day high had a mean excess 5-day return of +0.39 % (t_day 0.43, 779 cases on 162 days). The slope was 0.0033 (t 0.77), and the cases 2.5 or more swings below the high averaged −0.45 % (t −0.29, 254 cases).
- **F2:** The same graded fall shows clearly in choppy markets (60-day return between −10 % and +10 %), and the steps are monotonic. Below the 20-day high, the slope of the excess 5-day return on swing-scaled distance was 0.0186 (t 4.28, 167 cases, 70 days), with a mean excess of −3.17 % (t_day −2.13). The excess return by depth was:
- **F3:** In falling markets the deep cases also fall, but the effect is neither graded nor steady across years. The cases 2.5 or more swings below the high averaged −1.38 % (t −2.11, 350 cases), but the slope was flat (t 0.32, 508 cases). The deep mean changes sign by year: −3.4 % in 2018 and 2019, +6.2 % (t 3.87) in 2020, and −0.1 % in 2021.
- **F4:** Inside the rising profile, the brief's effect sits on the other side of the high. Rising-market cases at or above the 20-day high had a mean excess 5-day return of +4.41 % (t 2.84, 127 cases) and +8.5 % over 10 days (t 2.70, 63 cases). Cases below the high were near 0 at every depth (from −1.8 % to +1.2 % per bin, |t| ≤ 1.27). The rising profile therefore carries the at-the-high drift, not a fall below it.
- **F5:** The per-coin and per-window slopes inside the rising profile are mixed, so the pooled rising slope is noise rather than a weak effect. LTC (t 2.20) and ZEC (t 1.97) point the idea's way, while DOGE (t −1.77) and XRP (t −1.07) point against it. By window, w16 has t 2.72 and w11 has t −2.00. By year, 2020 has t 3.16 and 2021 has t −1.22.

## Ideas
- `034-03.b1_choppy-far-below-high-falls` (from F2, F1, F5): In a choppy market, a coin whose daily close has slipped below its 20-day high falls over the next 5 days, more the more of its own daily swings over the last 20 days it stands below that high.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
