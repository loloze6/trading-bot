---
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday_1d
idea tested: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3643 USD
---
## Findings
- **F1:** The tested fall side has a level but no grading: Sunday falls are followed by a mean excess 2-day return of +0.0054 (t 2.45, n 1036), but within falls the slope on the fall's size has t 0.71 (n 1050). The deepest fall quintile (z −1.13) earns +0.0045 against +0.0078 for the next quintile (z −0.37), so the plan's graded slope (t 0.29) finds nothing.
- **F2:** The effect is graded once both sides of Sunday's move are taken together. The slope of the excess forward return on Sunday's volatility-scaled return is −0.0047 at 2 days (t −2.62) and −0.0075 at 3 days (t −3.54), with n 2087 at both horizons. Sunday is the only weekday with a significant 3-day slope; the other days range from t −0.06 to 1.67.
- **F3:** Weekend rises carry most of the reversal. Sunday rises are followed by a mean excess 2-day return of −0.0103 (t −4.60, n 1116), against +0.0054 after falls (rise-minus-fall Welch t −5.00). At 3 days the Sunday rise-minus-fall Welch t is −4.17, while on the other weekdays it runs from −0.37 to 1.68.
- **F4:** The Sunday 3-day reversal slope has the same sign everywhere. Its t is negative in all 8 years (from −0.01 to −4.16, strongest in 2019) and in all 6 coins (BTC −0.87, ETH −1.33, LTC −2.31, XMR −3.04, XRP −1.57, ZEC −0.00).
- **F5:** The reversal is somewhat stronger after low-volume Sundays. The 2-day slope t is −2.24 when Sunday volume is below its 28-day median, against −1.75 above it (n 1076 and 1077).
- **F6:** Within rises alone, the size of the reversal is not monotone. By rise quartile, the excess 2-day return is −0.0056, −0.0218, −0.0120 and −0.0006, so the grading in F2 comes from the full range of moves across both signs.

## Ideas
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.b1_weekend-move-reverses-three-days` (from F2, F3, F4, F1): A coin's weekend move (its Saturday-to-Sunday close-to-close return) is partly undone over the next 3 days (Monday to Wednesday): the higher its weekend return relative to the coin's usual daily move, the lower its return over those 3 days, and the lower the weekend return, the higher.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
