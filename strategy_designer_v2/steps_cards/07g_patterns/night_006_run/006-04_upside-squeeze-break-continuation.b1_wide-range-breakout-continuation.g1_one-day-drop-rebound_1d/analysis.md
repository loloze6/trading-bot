---
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound_1d
idea tested: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3508 USD
---
## Findings
- **F1:** The rebound after a fall depends on how volatile the coin already is. In the coin's highest third of 60-day volatility, the slope of next-day excess return on the size of the fall is 0.0147 (t 7.09, n 2360). In the middle third it is 0.0042 (t 3.27, n 2454). In the lowest third it is -0.0001 (t -0.11, n 2337).
- **F2:** Only falls rebound; rises do not, and only the largest falls carry the effect.
- **F3:** Rising volume predicts a higher next day, even with the fall, the rise, range and close location held in the same fit. The ratio of 5-day to 60-day volume has a beta of 0.0036 (t 2.84). By quintile, the top quintile gives +0.0023 (t 2.01, n 2903) and the bottom gives -0.0020 (t -2.39).
- **F4:** The rebound also tracks the day's own volume. On the highest-volume third of days the fall slope is 0.0055 (t 4.06, n 2370); on the middle third it is -0.00004 (t -0.02).
- **F5:** Range compression does not precede larger moves; the reverse holds.
- **F6:** The edge has faded over time. The fall slope is t 2.3 to 5.3 in 2018–2020 (0.0156 in 2020) and t 0.6 to 1.3 in 2022, 2024 and 2025. The book's mean daily return is -0.00009 in 2025 while holding the coins gives +0.0020.
- **F7:** The book's tails are about 0.7 times those of holding the coins. Its worst 1% of days average -0.080 against -0.112 for the coins on the same days, and its best 1% average +0.070 against +0.106. This means the falls it buys keep falling on crash days, which is consistent with the failed Calmar of 0.70.
- **F8:** Down days that close near their low rebound more. In the lowest close-location quintile the next-day excess return is +0.0041 (t 2.93); in the highest it is +0.0006 (t 0.39). In the joint fit over all days close location is not significant (t 0.33), so this is weak.

## Ideas
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound.g1_drop-rebound-in-volatile-markets` (from F1, F2, F7): The higher a coin's 60-day volatility, the larger the rebound over the next 1 day per unit of its 1-day fall (measured in its usual daily moves).
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound.g2_high-volume-capitulation-rebound` (from F4, F2, F8): The larger a coin's 1-day fall, the higher its return over the next 1 day, and more so the larger that day's volume relative to its 60-day average.
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound.g3_volume-surge-next-day-drift` (from F3): The higher a coin's 5-day volume relative to its 60-day volume, the higher its return over the next 1 day.
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g1_one-day-drop-rebound.g4_range-expansion-persists-forward` (from F5): The wider a coin's 5-day average daily range relative to its 60-day average range, the larger its absolute move over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
