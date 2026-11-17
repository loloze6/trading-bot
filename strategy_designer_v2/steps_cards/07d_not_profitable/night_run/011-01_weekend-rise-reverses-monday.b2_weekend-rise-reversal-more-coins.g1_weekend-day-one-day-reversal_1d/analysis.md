---
line: 7.d not profitable
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal_1d
idea tested: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5535 USD
---
## Findings
- **F1:** The book misses its gain targets mostly because of fees and because it is flat most of the time. It holds almost nothing from Monday to Friday (mean absolute position about 0.005, against 0.32 to 0.39 on weekend bars). Its gross gain is 0.000278 per bar, of which fees take 0.000207. This leaves a daily mean of 0.000194, against 0.001389 for holding the coins, with a daily standard deviation of 0.0079 and 24% of days at exactly zero.
- **F2:** Fees cost about half the weekend gain. Saturday bars earn 0.000756 gross against 0.000384 in fees. Sunday bars earn 0.001200 gross against 0.000612 in fees. Monday's unwind adds another 0.000449 per bar in fees.
- **F3:** The gain sits in the largest moves, and the smallest moves lose to fees. By quintile of the weekend day's absolute vol-scaled move, the gain per bar runs 0.00002, 0.00012, 0.00083, 0.00140 and 0.00256. Fees run 0.00015, 0.00027, 0.00042, 0.00063 and 0.00102. The two smallest quintiles therefore lose money net.
- **F4:** High weekend volume carries the reversal, which is the opposite of what the brief expects. Volume is measured against the coin's 20-day median.
- **F5:** The reversal of a Sunday move keeps running past Monday.
- **F6:** The same one-day fade on weekdays is small and flat across move size, at -0.0006 to 0.0008 across all quintiles. This confirms that the effect belongs to weekend days, but the book can trade it on only two bars a week.
- **F7:** The timing gain is not steady across years. It is positive in 2018 to 2020, 2022 and 2024 (0.00037 to 0.00120 per bar) and negative in 2023 (-0.00010) and 2025 (-0.00017). This feeds the weak Calmar of 0.22.

## Ideas
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal.d1_high-volume-weekend-moves-reverse` (from F3, F4, F2, F1): A coin's one-day return on a Saturday or a Sunday, measured against its own recent daily volatility, is reversed over the next day. The larger the weekend day's rise, the larger the next day's fall, and the larger its fall, the larger the next day's rise. The reversal is larger the higher that weekend day's traded volume is against the coin's own usual volume over the past 20 days.
- `011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal.d2_sunday-reversal-spans-two-days` (from F5, F2, F1): A coin's one-day return on a Saturday or a Sunday, measured against its own recent daily volatility, is reversed over the next day. The larger the weekend day's rise, the larger the next day's fall, and the larger its fall, the larger the next day's rise. A Sunday's move keeps being reversed over the following two days, in proportion to its size.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
