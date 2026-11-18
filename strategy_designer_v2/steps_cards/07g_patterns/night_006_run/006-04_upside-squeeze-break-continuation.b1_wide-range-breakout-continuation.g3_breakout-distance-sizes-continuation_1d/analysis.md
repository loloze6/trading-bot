---
line: 7.g patterns
backtest: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation_1d
idea tested: 006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3631 USD
---
## Findings
- **F1:** The 20-day range width sets the size of the next 10 days' move. Measured against the coin's own 20-day volatility (|10-day return| / (20-day daily std × √10)), the move falls steadily across the width quintiles: 1.39, 0.99, 0.80, 0.86 and 0.63, from the narrowest to the widest, with about 165 non-overlapping cases each. So the narrowest ranges are followed by moves more than twice as large, in volatility units, as the widest.
- **F2:** The narrowest-range quintile is followed by a 10-day absolute move 1.27 times the coin's average, against 0.93 for the other quintiles (Welch t = 3.33, 168 cases vs 659). The ratio is above 1 in every coin, from 1.15 for BTC to 1.41 for XMR. Compression predicts the size of the move but not its direction: the excess 10-day return by width quintile is flat (Spearman ρ = 0.014, p = 0.68).
- **F3:** A coin's next-day return rises the deeper today's fall is, measured in units of its 20-day volatility. Over all z < 0 days, the slope of the next-day excess return on today's z is −0.0026 (t = −3.63, n = 7056), and it is negative in all six coins (XMR t = −3.05, XRP t = −2.40).
- **F4:** After a down day of 1 to 2 sigma, the next-day excess return is +0.48% (t = 3.26, n = 1310), and after a fall beyond 2 sigma it is +0.68% (t = 2.57, n = 484). Up days of the same size are followed by nothing (t = −0.16 and 0.24). The rebound is positive in every coin, but it fades in recent years: +1.4% in 2020–2021 (t ≈ 3.1–3.4) against ≈ 0 in 2024–2025 (t = −0.28, 0.30).
- **F5:** The tested breakout signal is not graded. The excess 10-day return by distance above the prior 20-day high is −1.8% in quintile 2 (t = −2.34) and +2.9% only in the top quintile (t = 2.63), with an overall ρ of 0.058 (p = 0.03, n = 1403).
- **F6:** The book barely trades and earns almost nothing. It is in the market on only 5–11% of bars per coin, its mean daily return is 0.0000118 against 0.00119 for holding, and its position gain is negative in three of six coins (XMR −0.39, LTC −0.12 summed).
- **F7:** Weekday patterns were checked but are not used. Next-day returns after Fridays are high (t = 3.76, n = 2479), but this is one of many weekday, hour and year cuts examined, and it is an on/off calendar condition, not a graded one.

## Ideas
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation.g1_compressed-range-enlarges-move` (from F1, F2): The narrower a coin's 20-day high-to-low range is relative to its own usual 20-day range width, the larger its absolute price move over the next 10 days, measured in units of its 20-day volatility.
- `006-04_upside-squeeze-break-continuation.b1_wide-range-breakout-continuation.g3_breakout-distance-sizes-continuation.g2_sharp-drops-rebound-next-day` (from F3, F4): The larger a coin's one-day fall, measured in units of its own 20-day daily volatility, the more its price rises over the next day.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
