---
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d
idea tested: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3917 USD
---
## Findings
- **F1:** Across all six coins, a day's return scaled by its 20-day standard deviation is reversed the next day much more after weekend days than after weekdays: slope −0.00446 (t −5.03, n 4138) for weekend signal days against −0.00100 (t −2.29, n 10362) for weekday signal days.
- **F2:** Saturday reverses as strongly as Sunday, although the tested idea trades only Sunday. The next-day slope on the scaled move is −0.00459 (t −4.13, n 2069) after Saturday and −0.00438 (t −3.23, n 2069) after Sunday. Among weekdays, only Tuesday reaches that size, at −0.00344 (t −3.20).
- **F3:** Sunday's scaled move keeps being reversed beyond Monday. Over the next 3 days the slope is −0.00746 (t −3.48, n 2021, one Sunday a week, so no overlap), against −0.00438 over the next 1 day.
- **F4:** The reversal sits in high-volatility periods. With 20-day volatility measured against its own 120-day median, the next-day slope is +0.00069 (t 0.74) in the lowest tercile, −0.00126 (t −1.32) in the middle and −0.00274 (t −2.32) in the highest. On the non-overlapping 3-day grid the highest tercile gives −0.00932 (t −2.64, n 621), against +0.00332 in the lowest.
- **F5:** Inside the high-volatility tercile, the reversal is stronger on light-volume days, which is the brief's original volume direction and the opposite of the plan's supporting check. Day volume is measured against its 20-day average. The slope is −0.00775 (t −2.64, n 742) in the lowest-volume tercile, −0.00510 (t −2.03) in the middle and −0.00144 (t −0.82) in the heaviest.
- **F6:** The reversal comes from falls, not rises. On down days the next-day slope is −0.00314 (t −3.61, n 7151); on up days it is +0.00088 (t 1.12, n 7349). The lowest quintile of scaled moves is followed by +0.40% excess the next day (t 4.13, n 2894).
- **F7:** The Sunday reversal is not stable over time. It is strong in 2019 (−0.00748, t −3.03) and 2020 (−0.01099, t −3.00). It is near zero or positive in 2022 to 2024 (+0.0007, +0.0005, +0.0010). This matches the book's weak result: mean daily return 5.6e-05, Sharpe 0.16, all its gain booked on Mondays at +0.00080 a day.

## Ideas
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday.g1_saturday-move-reverses-sunday` (from F1, F2): In a coin, Saturday's daily return measured in its 20-day daily standard deviations is reversed over the next 1 day: the larger Saturday's move, the larger Sunday's move against it.
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday.g2_sunday-move-reverses-midweek` (from F3, F1): In a coin, Sunday's daily return measured in its 20-day daily standard deviations is reversed over the next 3 days: the larger Sunday's move, the larger the move against it from Sunday's close to Wednesday's close.
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday.g3_light-volume-moves-reverse-in-turbulence` (from F4, F5): In a coin whose 20-day volatility is high against its own past 120 days, a day's return measured in its 20-day standard deviations is reversed over the next 1 day. The reversal is larger the lower that day's volume is against its 20-day average.
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday.g4_scaled-falls-rebound-next-day` (from F6, F1): In a coin, a daily fall measured in its 20-day daily standard deviations is followed by a rebound over the next 1 day: the larger the scaled fall, the larger the next day's rise.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
