---
line: 7.g patterns
backtest: 012-01_liquidation-flush-rebound_1d
idea tested: 012-01_liquidation-flush-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5487 USD
---
## Findings
- **F1:** Among all 1-day falls of at least one usual move (20-day volatility), the 3-day excess return rises steadily with the bar's volume over its prior 30-day mean. It goes from -0.013 (n=189) at a ratio of 1 or less, to -0.002 (n=156) at 1–1.5, +0.010 (n=82) at 1.5–2, +0.036 (n=62) at 2–3 and +0.064 (n=41) above 3. Above 3, the median is +0.075, 78% of cases are positive and the winsorised t is 5.46.
- **F2:** In a regression of the 3-day excess return on falls (n=530, non-overlapping grid), log volume ratio carries a slope of 0.037 per log unit (t 4.62). It still carries 0.025 (t 4.08) with returns winsorised at 2%/98%. The fall's size in usual moves adds nothing: slope t 0.97 raw, 0.11 winsorised.
- **F3:** The lower wick does not carry the rebound, against the idea. Wick share has slope -0.016 (t -0.54) in that regression, and its Spearman with the 3-day excess return is -0.048 (n=530). Falls with the shortest wicks (≤0.15 of range) earn +0.015 (t 2.52, n=238), while falls with wicks of 0.333–0.6 earn +0.009 (t 0.84, n=96). This explains why the test's forecast, half wick, had Spearman -0.009 despite a mean flush excess return of +0.016 (t 2.11, n=158).
- **F4:** The volume effect belongs to falls only. Over 3 days, rises of at least one usual move with volume 2–4x earn -0.005 (t -0.63, n=115) and with volume above 4x earn +0.001 (t 0.03, n=26). Quiet bars with volume above 4x earn -0.038 (t -1.80, n=20). Falls with volume 2–4x earn +0.045 (t 3.01, n=84) and above 4x earn +0.057 (t 3.31, n=19).
- **F5:** The volume-graded rebound appears in most coins and later years, but not all. The Spearman of volume ratio with the 3-day excess return on falls is positive in 5 of 6 coins: LTC 0.29 (p 0.005), XRP 0.24 (p 0.03), XMR 0.13, ZEC 0.10, ETH 0.06, BTC -0.00. It is positive in 2020–2022 and 2024 (0.28 to 0.49) but near zero or negative in 2018, 2019 and 2023. Falls on at least 2x volume earn +0.073 (t 3.14, n=43) in windows w17–w24 against +0.032 (t 2.18, n=34) in w1–w8.
- **F6:** The book barely traded and did not profit. It averaged 0.009 trades per bar and was active on only 40–63 of about 2,897 days per coin. Its Sharpe was -0.03 against a mean daily return of -4e-06, because the position existed only on the flush bar itself rather than over the 3 days in which the rebound shows.
- **F7:** Next-day excess return by weekday is uneven: Friday bars +0.0028 (t 3.16), Wednesday -0.0034 (t -2.87) and Monday -0.0026 (t -2.50), with about 2,050 cases each. Across the many angles looked at, this has no mechanism behind it and is noted, not built on.

## Ideas
- `012-01_liquidation-flush-rebound.g1_volume-graded-fall-rebound` (from F1, F2, F3, F4, F5): After a day that closes sharply lower, the heavier that day's volume relative to the coin's own 30-day average volume, the larger the coin's rise over the next 3 days, whatever the length of the day's lower wick.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
