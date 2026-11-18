---
line: 7.b inconclusive
backtest: 011-02_weekend-drop-rebounds-monday_1d
idea tested: 011-02_weekend-drop-rebounds-monday
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3465 USD
---
## Findings
- **F1:** The test's main measure is on the predicted side but short of the bar: the forecast-weighted excess 2-day return after Sunday drops has t 1.35 over 1197 cases (my recount: t 1.30, n 1196), and the top-minus-bottom-third check passes (+0.0025). The six coins all have positive per-coin means but per-coin t only 0.04 to 1.44, so the sign is consistent and the size is too small for these six coins.
- **F2:** The plain rebound exists but is weakly graded. Sunday drops are followed by a mean excess 2-day return of +0.0065 (t 2.84, n 967), against +0.00044 after weekday drops (Welch t, Sunday minus weekday, 2.46). Yet the deepest quartile of drops rebounds less (+0.0047, t 0.90) than the second and third quartiles (+0.0113 and +0.0101, t 2.64 and 2.20). The depth-weighted product therefore reaches only t 1.53, and the grading the plan rewards is what dilutes it.
- **F3:** The effect sits mostly in certain years. The main measure has t 4.07 in 2020 (n 156) and 1.43 in 2021, against -2.81 in 2018 (n 143), and it is near zero (t between -0.13 and 0.63) in 2019 and 2022–2025.
- **F4:** The horizon matters. Product t for Sunday drops is 2.68 at 1 day and 2.52 at 3 days, against 1.53 at the plan's 2 days.
- **F5:** The opposite side shows more clearly. Sunday rises are followed by a mean excess 2-day return of -0.0098 (t -4.26, n 1083). Across all Sundays, the slope of excess 2-day return on the Sunday move in usual moves is -0.0046 (t -2.46). No other weekday has a 2-day slope with |t| above 1.6.
- **F6:** More data is available. Thirteen more coins (ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO) have folds A and D, plus parts of B and C. This could multiply the 1197 cases, which is what a positive t of 1.35 needs.

## Ideas
- `011-02_weekend-drop-rebounds-monday.b1_weekend-drop-rebound-more-coins` (from F1, F2, F6): A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 2 days (Monday and Tuesday), and the larger the weekend drop, the larger the rebound.
- `011-02_weekend-drop-rebounds-monday.b2_weekend-rise-fades-monday` (from F5, F2): A coin that rose over the weekend (its Saturday-to-Sunday close-to-close return) falls over the next 2 days (Monday and Tuesday), and the larger the weekend rise, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
