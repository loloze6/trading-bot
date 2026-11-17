---
line: 7.b inconclusive
backtest: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday_1d
idea tested: 011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3520 USD
---
## Findings
- **F1:** The main measure leans clearly toward the idea, with a slope of 0.000338 per forecast unit and t 3.16 over 2489 Sunday cases. The result is inconclusive only because of the volume clause: the high-volume minus low-volume slope difference has t −0.0001. My per-coin volume terciles agree, with slopes of 2.9, 4.2 and 3.4 bp per forecast unit (t 1.04, 1.95, 1.86, n ≈ 690 each), so there is no gradient with volume.
- **F2:** The reversal shows in the earlier years only. Sunday slopes in 2018–2021 are 4.5, 5.9, 11.0 and 6.3 bp per forecast unit (t 1.0, 2.7, 3.4, 1.2, about 258 cases each). In 2022–2025 they are −0.2, 0.5, −0.4 and −1.1 bp (all |t| < 0.4).
- **F3:** The effect is spread unevenly across coins. XMR carries the strongest slope at 6.2 bp (t 2.47, n 345), ZEC, LTC and ETH sit at 3.5–5.3 bp (t 1.2–1.6), and BTC is flat at −0.2 bp (t −0.07).
- **F4:** The reversal works by direction more than by size. After down Sundays the next-day excess mean is +60 bp, and after up Sundays it is −56 bp. Within the up side the slope runs the wrong way, at −5.8 bp (t −2.24, n 1099). Across forecast quintiles the next day reads −15, −96, −37, +74 and +66 bp, so the most extreme quintiles reverse less than the moderate ones.
- **F5:** Reversal of a day's scaled move into the next day is not specific to Sunday. The slope of next-day excess return on minus the 20-day z of the move is 45.9 bp per z unit for Saturday bars (t 4.13, n 2069) and 43.7 bp for Sunday bars (t 3.23, n 2069). Tuesday to Thursday bars give 22–34 bp (t 2.1–3.2), while Monday bars continue at −20.5 bp (t −2.27).

## Ideas
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday.b1_sunday-move-reverses-monday` (from F1, F4): In a coin, Sunday's daily return, measured in its 20-day daily standard deviations, is reversed over the next 1 day: the larger Sunday's move, the larger Monday's move against it.
- `011-01_weekend-rise-reverses-monday.b1_weekend-fall-reverses-monday.g1_high-volatility-fall-reversal.g1_sunday-move-reverses-monday.b2_saturday-move-reverses-sunday` (from F5, F2): In a coin, Saturday's daily return, measured in its 20-day daily standard deviations, is reversed over the next 1 day: the larger Saturday's move, the larger Sunday's move against it.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
