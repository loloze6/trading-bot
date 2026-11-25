---
line: 7.b inconclusive
backtest: 032-02.b2.g1.d2_long-reversal-after-wide-days_1d
idea tested: 032-02.b2.g1.d2_long-reversal-after-wide-days
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3477 USD
---
## Findings
- **F1:** The test's result is on the side the idea predicts but short of the bar: top-minus-bottom tercile +0.18 % with Welch t 1.19 over 1,814 and 1,883 days. In the folds shown (B and C) it is larger, +0.47 % with t 1.89 on 2,901 top-tercile cases, and the same sign holds on every coin (BTC +0.31 % t 1.13 up to XMR +1.48 % t 4.37) and every year 2018–2021 (t 0.58 to 1.65).
- **F2:** The effect is not graded across the forecast. It sits in the top 30 % only: forecast deciles 7, 8 and 9 earn +0.60 % (t 3.27), +0.39 % (t 2.25) and +0.81 % (t 3.60) next day, while deciles 0–6 are all flat to negative (−0.54 % to −0.04 %). By raw-signal quintile it is −0.18 %, −0.20 %, −0.42 %, +0.22 % and +0.67 % (t 4.35). A tercile split mixes the active top with an inactive middle and bottom.
- **F3:** Most of the signal comes from the close's place in the range. The close-location share alone gives +0.55 % with t 2.26, against +0.35 % with t 1.36 for the range multiple alone. In the 3×3 grid, only the low-close, wide-day cell is clearly up (+0.84 %).
- **F4:** The rebound shows only when the coin is already falling.
- **F5:** Inside the falling regime, the effect is graded by the depth of the 20-day fall. In the deepest third of falls the gap is +1.85 % (t 2.58, 445 cases); in the middle third it is −0.02 % (t −0.05), and in the shallowest +0.25 % (t 0.70). That gap is nearly ten times the 0.19 % cost of a trade. The test's overall unusual move is only +0.09 %, 0.5 times that cost.
- **F6:** The horizon fits the plan. The gap is still positive at 2 days (+0.57 %, t 1.22) but gone by 3 and 5 days (−0.20 % t −0.29; −0.82 % t −0.72). On bars that are also a fresh 30-day low, the gap is negative (−0.55 %, t −0.40, 347 cases). So the rebound follows wide low closes in a deep fall, not the monthly-low break itself.

## Ideas
- `032-02.b2.g1.d2.b1_wide-day-low-close-rebound-more-coins` (from F1, F2): The lower a coin's daily close sits within that day's high-low range, the more the coin rises over the next 1 day. The rise is larger the wider that day's range is against the coin's average daily range over the previous 20 days.
- `032-02.b2.g1.d2.b2_rebound-after-wide-days-in-decline` (from F4, F5, F3, F6): The lower a coin's daily close sits within that day's high-low range, the more the coin rises over the next 1 day, and the rise is larger the wider that day's range is against the coin's average daily range over the previous 20 days, only while the coin's 20-day return is negative, and more the deeper that 20-day fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
