---
line: 7.b inconclusive
backtest: 058-02.b1.g1.b2_agitated-falling-rally-fades_1d
idea tested: 058-02.b1.g1.b2_agitated-falling-rally-fades
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3158 USD
---
## Findings
- **F1:** In the falling, agitated profile, the next day reverses the one-day move on both sides. After up days the unusual move in the short direction is +0.98 % (t 4.23, 613 cases, 258 days). After down days it is −1.26 % (t −5.38, 675 cases, 289 days), meaning the coin rose 1.26 % more than its normal drift. Outside the profile the same split is small: +0.14 % (t 1.57) after up days and −0.06 % (t −0.66) after down days.
- **F2:** The tested short side does not grow with the size of the rise, which is why the slope is about zero (−0.00015, t −0.49) despite a positive mean. By quartile of the rise against the 20-day swing, the next-day fall is +0.81 % (t 1.70), +0.84 % (t 1.66), +1.93 % (t 4.84), then −0.14 % (t −0.24) for the sharpest rises (136 cases, 74 days).
- **F3:** The mirror side is graded the way the brief predicts for the low edge. By quartile of the down day's size against the 20-day swing, the next-day rise beyond drift is +2.44 % for the sharpest falls (t 4.00, 140 cases, 70 days), then +1.23 % (t 3.12), +1.82 % (t 4.28), and +0.01 % (t 0.02) for the smallest falls.
- **F4:** The fade after up days is not carried by one coin or one year. It is positive on all six coins (+0.26 % to +1.23 %) and in every year of folds B and C (2018 +1.56 %, 2019 +0.77 %, 2020 +0.37 %, 2021 +0.72 %). The test's weak result therefore comes from the shape of the effect, which is a sign effect with no growth in the sharpest rises, not from patchiness.

## Ideas
- `058-02.b1.g1.b2.b1_agitated-falling-selloffs-rebound` (from F1, F3): In a falling, agitated market, the larger a coin's one-day fall against its usual daily swing over the last 20 days, the larger its rise over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
