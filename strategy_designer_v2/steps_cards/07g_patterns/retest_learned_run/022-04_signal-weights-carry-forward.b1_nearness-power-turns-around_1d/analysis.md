---
line: 7.g patterns
backtest: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around_1d
idea tested: 022-04_signal-weights-carry-forward.b1_nearness-power-turns-around
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4575 USD
---
## Findings
- **F1:** The forecast's skill sits on its long side: over 3042 non-overlapping 5-day cases, the top forecast quintile is followed by +0.88 % excess (t 1.93, 610 cases), but the bottom quintile by only -0.24 % (t -0.50), so shorts earn about 0.24 %. The pooled rank correlation is 0.054 (t 2.99), positive in five coins (0.024 to 0.081) and negative in ZEC (-0.026).
- **F2:** The book's worst 2 % of coin-days (310, mean -8.40 %) come on days the coin rose on average (+1.03 %, only 50 % of them down days), so its largest losses are mostly short positions caught in rallies. Its best 2 % (mean +8.59 %) come on days the coin rose +2.95 %.
- **F3:** A wide day predicts the next 5 days. The larger a day's high-low range against its own 30-day average, the higher the coin's excess return over the next 5 days: the second quintile is followed by -0.90 % (t -2.15) and the top quintile by +0.78 % (t 1.64), with the pooled rank correlation of the raw range at 0.051 (t 2.80, 3042 cases).
- **F4:** The range effect in F3 holds coin by coin and year by year: its rank correlation is positive in all six coins (0.041 to 0.144) and in 7 of 8 years (-0.020 in 2019, 0.214 in 2024). In a joint regression with the forecast, however, the range term falls to t 0.16 while the forecast keeps t 2.07, so part of the effect overlaps the tested forecast.
- **F5:** Large days continue upward rather than reverse. Days in the top quintile of absolute move against 30-day volatility are followed by +1.07 % over 5 days (t 2.19, 482 cases; +0.147 of a usual move, t 2.36), positive in all six coins (rho 0.012 to 0.083). This comes from up days: days above +2 standard deviations are followed by +3.23 % (t 2.06, 84 cases) and days below -2 by -0.69 % (t -0.69, 58 cases).
- **F6:** Saturdays carry an excess daily return of +31 bp (t 3.63, 2210 days), positive in all six coins but negative in 2022 and 2023. The 5-day grid shows a Monday-start +1.38 % (t 2.63) and a Sunday-start -1.53 % (t -2.86). These are calendar conditions, not graded situations, and among the many angles looked at they are not proposed as ideas.
- **F7:** Volume against its 20-day mean has a pooled rank correlation of 0.049 (t 2.53) with the next 5 days, but it is near zero in BTC (-0.002) and LTC (-0.004). It is not consistent enough to count.

## Ideas
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g1_range-expansion-precedes-rises` (from F3, F4, F2): The wider a coin's daily high-low range is relative to its average range over the past 30 days, the higher that coin's return over the next 5 days.
- `022-04_signal-weights-carry-forward.b1_nearness-power-turns-around.g2_strong-up-days-continue` (from F5, F2, F1): The larger a coin's daily rise is relative to its volatility over the past 30 days, the higher that coin's return over the next 5 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
