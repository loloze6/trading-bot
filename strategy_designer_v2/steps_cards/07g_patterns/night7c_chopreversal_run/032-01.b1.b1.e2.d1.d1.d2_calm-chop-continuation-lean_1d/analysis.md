---
line: 7.g patterns
backtest: 032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean_1d
idea tested: 032-01.b1.b1.e2.d1.d1.d2_calm-chop-continuation-lean
step 5: confirmed
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3639 USD
---
## Findings
- **F1:** Across all coins in folds B and C, on a 1-day grid, the more a day's fall is measured in the coin's 30-day daily swings, the larger the next day's drift-removed return. Days with z ≤ −3 are followed by +3.78 % (t 3.01, n 48), z in (−3, −2] by +1.18 % (t 2.60, n 131) and z in (−1, 0] by +0.15 % (t 1.40, n 2393). The slope on down days is −0.00624 per unit of z (t −5.15, n 3146), the strongest pattern among the many angles examined.
- **F2:** The rebound is one-sided. On up days the slope of the next day's drift-removed return on z is +0.00086 (t 0.84, n 3305), and days with z > 2 are followed by small, non-significant falls (−0.58 % t −1.30; −0.36 % t −0.43).
- **F3:** After days with z ≤ −1.5 (n 371 with 30-to-90-day swing ratio available), the next-day rebound grows with how wide the 30-day swings are against the 90-day swings. In the calm tercile it is −0.01 % (t −0.02, n 124), in the middle tercile +0.89 % (t 2.21, n 123) and in the wide tercile +2.43 % (t 4.11, n 124).
- **F4:** The rebound after z ≤ −1.5 days holds in every coin (+0.50 % for BTC to +1.49 % for XMR, all positive), in every year (+0.63 % in 2018 to +1.99 % in 2020), and whether the 30-day return is down (+0.98 %, t 2.52, n 249) or up (+1.29 %, t 2.87, n 133).
- **F5:** The tested book does not capture this rebound. After days with z ≤ −1.5 its position is net short (mean allocation −0.112, short 45 % of the time and long 32 %, n 382), yet the book's day after its worst 2 % of days still averages +0.85 % (t 2.85, n 173).
- **F6:** The tested idea itself is graded inside its regime. The active grid bars' directional drift-removed 7-day return rises from +2.03 % (t 1.29, n 80) in the lowest |forecast| quartile to +6.38 % (t 3.98, n 80) in the highest. Across all grid bars, aligned continuation is strongest at 30-day efficiency 0.15 to 0.3 (+4.53 %, t 3.80, n 162) and in the calm 30-to-90-day swing tercile (+3.36 %, t 3.13, n 191). It is absent in the wide tercile (−1.10 %, t −0.87, n 146).

## Ideas
- `032-01.b1.b1.e2.d1.d1.d2.g1_widened-swing-sharp-drop-rebound` (from F1, F2, F3, F4, F5): The larger a coin's 1-day fall, counted in its past 30 days' daily swings, the larger its rise over the next 1 day, and the more so the wider its past 30 days' daily swings are compared with its past 90 days'.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
