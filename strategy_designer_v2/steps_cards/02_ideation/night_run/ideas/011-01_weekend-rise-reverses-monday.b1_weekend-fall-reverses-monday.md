---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin that fell over the weekend (its Saturday-to-Sunday close-to-close return) rises over the next 2 days (Monday and Tuesday), and the larger the weekend fall relative to the coin's usual daily move, the larger the rise.
Consequence: A weekend fall is a reason to lean long into Monday and Tuesday, more so the deeper the fall, since it is partly undone once weekday liquidity returns.
Why:
- F3: Sunday falls reverse as well (2-day excess +0.0065, t 2.84, n 967), and on the fall side the grading runs the right way. The Sunday sextiles with mean z of −1.64, −0.59 and −0.14 are followed by +0.0116, +0.0048 and +0.0009. Over all Sundays, the 2-day excess regressed on the clipped z has slope −0.0047 (t −3.30, n 2051).
- F2: The reversal is specific to Sunday. Rises stamped Sunday are followed by a 2-day excess of −0.0098 (t −4.26, n 1083). Rises on other weekdays are followed by between −0.0025 and +0.0022 (|t| ≤ 1.2), except Thursday at +0.0088.
- F4: Betting against the sign of the Sunday return alone earns 0.0082 per case (t 5.08, n 2051), about the same as the graded short-only measure but with far more certainty. This effect is positive in every year: strongest in 2018 (0.0167, t 2.99) and 2020 (0.0183, t 4.24), weakest in 2023 (0.0008, t 0.36).
