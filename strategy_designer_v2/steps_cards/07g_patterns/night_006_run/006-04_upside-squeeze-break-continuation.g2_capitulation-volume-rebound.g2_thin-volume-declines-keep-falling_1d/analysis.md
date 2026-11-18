---
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g2_thin-volume-declines-keep-falling_1d
idea tested: 006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g2_thin-volume-declines-keep-falling
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3633 USD
---
## Findings
- **F1:** Over all bars, not only after 5-day falls, the 5-day/30-day log volume ratio predicts the coin's excess 3-day return upward: the pooled slope is 0.0124 (t 4.32, n 4283 non-overlapping cases); it is 0.0170 after falls (t 4.07, n 2071) and 0.0072 after rises (t 1.80, n 2212), while the ratio multiplied by the sign of the 5-day return gives t -1.99, so the effect follows volume, not the fall the idea names.
- **F2:** The volume-ratio effect holds at 7 days too (slope 0.0233, t 3.22, n 1723), but it is concentrated in a few places: XRP (t 3.75) and ZEC (t 2.36), against t 0.36 to 1.32 for BTC, ETH, LTC and XMR, and windows w19-24 (t 4.39) against t 1.00 to 1.92 in the other three window groups.
- **F3:** The 5-day return predicts the excess 3-day return in the same direction (slope 0.0236, t 2.30, n 5435; top quintile +0.00734, t 2.46), and this momentum sits entirely on thin-volume bars: slope 0.0550 (t 2.80, n 2513) when the volume ratio is ≤ 0, against 0.0019 (t 0.13, n 1770) when it is above 0.
- **F4:** Against the brief, a compressed range is not followed by larger moves: the mean absolute 3-day return is 0.0538 in the most compressed 5/30-day range quintile and 0.0663 in the most expanded, the excess absolute return rises with the range ratio (t 5.61) and with the volume ratio (t 6.89), and the next 3 days' range follows the past range ratio (t 20.96).
- **F5:** The book's mean daily return of 0.00017 sits far below the coins' own mean daily returns of 0.00067 to 0.00155, because it is short on 28-36 % of bars against long on 18-21 % (mean position -0.035 to -0.086); its gain from the market's own rise is -0.000076 a day.

## Ideas
- `006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g2_thin-volume-declines-keep-falling.g1_heavy-volume-precedes-gains` (from F1, F2, F5): The higher a coin's 5-day average volume against its 30-day average, the higher its return over the next 3 days, whatever the direction of its last 5 days.
- `006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g2_thin-volume-declines-keep-falling.g2_quiet-volume-momentum-continues` (from F3): While a coin's 5-day average volume is below its 30-day average, the larger its 5-day return, the larger its return over the next 3 days in the same direction.
- `006-04_upside-squeeze-break-continuation.g2_capitulation-volume-rebound.g2_thin-volume-declines-keep-falling.g3_range-expansion-keeps-expanding` (from F4): The wider a coin's 5-day average daily range against its 30-day average, the larger its absolute price move over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
