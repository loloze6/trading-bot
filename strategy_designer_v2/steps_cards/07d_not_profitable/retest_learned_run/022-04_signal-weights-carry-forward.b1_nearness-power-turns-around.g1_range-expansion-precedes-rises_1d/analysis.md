---
line: 7.d confirmed, not profitable
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5437 USD
---
## Findings
- **F1:** The book was short more often than long (9616 short coin-bars against 7557 long), because the forecast turns negative whenever the day's range is narrower than usual; the shorts lost (mean gain −0.0088 % per bar, allocation −0.109) while the longs earned (+0.0426 % per bar, allocation +0.187).
- **F2:** The positions were small (mean |allocation| 0.14), so the book earned only 0.0101 % a day across 99 % of coin-days in a position, against the required 0.05 %; this gap and the losing shorts in F1 explain the failed mean on days in a position.
- **F3:** The effect sits on the wide side only. On the 5-day grid, the 4th and 5th range-ratio quintiles have excess returns of +0.81 % (t 1.99, n 568) and +0.76 % (t 1.53, n 569), while the narrowest quintile is near zero (−0.25 %, t −0.55, total +0.39 %); narrow days give no clean short.
- **F4:** Wide ranges pay only in an uptrend. With the 20-day return positive, wide days (top two quintiles) have a 5-day excess of +1.08 % (t 2.44, 705 cases) and a total move of +1.72 %, about 9 times the 0.19 % cost of a trade. With the 20-day return negative, wide days have only +0.29 % (t 0.69, 432 cases).
- **F5:** The uptrend condition is not the effect by itself on the idea's measure. Narrow days in an uptrend have a 5-day excess of −0.13 % (t −0.31, 713 cases; total +0.50 %) against +1.08 % for wide days in an uptrend. As a book, narrow-up long held 5 days reaches Sharpe 0.45 and Calmar 0.18, against wide-up long at Sharpe 0.88 and Calmar 0.59.
- **F6:** By year, the widest quintile's 5-day excess is negative in the falling years 2018 (−3.9 %), 2019 (−0.9 %), 2022 (−0.8 %) and 2023 (−0.7 %), and positive in 2020 (+3.6 %), 2021 (+3.3 %), 2024 (+2.8 %) and 2025 (+1.6 %). The effect is a rising-market one.
- **F7:** Rebuilt books with costs, against holding (Sharpe 0.56, Calmar 0.17, mean in position 0.117 %):
- **F8:** The book's falls come from its longs during broad drops. On its worst 5 % of days, 67 % of coins were held long (43 % on all days) and the coins' mean day was −2.94 %. The wide-up long book still fell −51 %, so the Calmar shortfall sits in crash days that the 20-day trend has not yet registered.
- **F9:** A longer horizon carries a larger move on the widest days: 5-day excess +0.76 % (t 1.53), 10-day +1.95 % (t 1.79, 281 cases), 20-day +2.62 % (t 1.20, 137 cases). However, the 10-day hold after a top-20 % range did not beat the 5-day hold as a book (Sharpe 0.62 against 0.58).

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d1_range-expansion-in-uptrends` (from F4, F5, F6, F7): The wider a coin's daily high-low range is relative to its average range over the past 30 days, the higher that coin's return over the next 5 days, only while the coin's own 20-day return is positive.
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d2_wide-range-days-lead-rises` (from F1, F2, F3, F7): The further a coin's daily high-low range exceeds its average range over the past 30 days, the higher that coin's return over the next 5 days above its usual drift, the effect lying in days wider than the norm.
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises.d3_range-expansion-ten-day-rise` (from F4, F9): The wider a coin's daily high-low range is relative to its average range over the past 30 days, while its 20-day return is positive, the higher that coin's return over the next 10 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
