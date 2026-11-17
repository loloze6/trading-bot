---
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday_1d
idea tested: 011-01_weekend-rise-reverses-monday
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3454 USD
---
## Findings
- **F1:** The main measure is positive (mean gain 0.00646, t 2.75, 1268 cases), but the supporting check fails because the size grading runs backwards. Sunday rises in the smallest-z quintile (mean z 0.11) are followed by a 2-day excess return of −0.0158. The largest-z quintile (mean z 2.21) is followed by only −0.0037, and the steps between are monotone (−0.0124, −0.0097, −0.0072). So the large-minus-small difference is +0.0035.
- **F2:** The reversal is specific to Sunday. Rises stamped Sunday are followed by a 2-day excess of −0.0098 (t −4.26, n 1083). Rises on other weekdays are followed by between −0.0025 and +0.0022 (|t| ≤ 1.2), except Thursday at +0.0088.
- **F3:** Sunday falls reverse as well (2-day excess +0.0065, t 2.84, n 967), and on the fall side the grading runs the right way. The Sunday sextiles with mean z of −1.64, −0.59 and −0.14 are followed by +0.0116, +0.0048 and +0.0009. Over all Sundays, the 2-day excess regressed on the clipped z has slope −0.0047 (t −3.30, n 2051).
- **F4:** Betting against the sign of the Sunday return alone earns 0.0082 per case (t 5.08, n 2051), about the same as the graded short-only measure but with far more certainty. This effect is positive in every year: strongest in 2018 (0.0167, t 2.99) and 2020 (0.0183, t 4.24), weakest in 2023 (0.0008, t 0.36).
- **F5:** The reversal after Sunday rises shows in four of six coins: ETH −0.0132 (t −2.84), LTC −0.0127 (t −2.16), XMR −0.0118 (t −2.57) and ZEC −0.0161 (t −2.42). It is nearly absent in BTC (−0.0013, t −0.30) and XRP (−0.0027, t −0.36).
- **F6:** Against the brief's volume clause, the reversal is strongest when weekend volume is high, not low. The sign-only gain is 0.0146 (t 3.90) in the top quartile of weekend volume relative to its 60-day mean and 0.0080 (t 2.87) in the bottom quartile. For Sunday rises, the excess is −0.0163 (t −3.35) in the top quartile versus −0.0106 in the bottom.

## Ideas
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday` (from F3, F2, F4): A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 2 days (Monday and Tuesday), and the larger the weekend fall relative to the coin's usual daily move, the larger the rise.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins` (from F1, F2, F5): A coin that rose over the weekend (its Saturday-to-Sunday close-to-close return) falls over the next 2 days (Monday and Tuesday), and the larger the weekend rise, the larger the fall.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
