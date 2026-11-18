---
line: 7.b inconclusive
backtest: 012-03_lower-wick-flush-recovery_1d
idea tested: 012-03_lower-wick-flush-recovery
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3237 USD
---
## Findings
- **F1:** The test's own measure sits on the predicted side but is close to nothing: on 223 independent flush bars the 3-day slope of excess return on the close's location in the range is +0.024 with t 0.74. The flush bars' mean 3-day excess return is +0.0003 (t 0.05), and the wick terciles run low −0.011, mid +0.008, high +0.004, which is not graded.
- **F2:** The plan's 3-day horizon falls where the effect turns over. Over 1 day the same slope is −0.073 with t −2.43 (n=226), the opposite of the idea. Over 5 and 10 days it is +0.008 (t 0.18) and −0.064 (t −1.21), so the positive 3-day reading is a crossing point, not a peak.
- **F3:** Over the next day, flush bars that close nearer their low rebound more. By quartile of close-near-low (1 − wick: 0.54, 0.74, 0.84, 0.94), the next-day excess return rises −0.013, −0.004, +0.010, +0.029 (about 41 bars each). Controlling for fall size and log volume ratio, that slope is +0.097 with t 2.78, while fall size has t −0.14.
- **F4:** The next-day rebound after a close near the low is broad across coins but uneven across years. It is positive in 5 of 6 coins (t 0.54 to 1.67; ZEC −0.35). By year it ranges from t −1.00 (2018) to t 4.54 (2022). The tested 3-day slope is also mixed by year, from t +1.59 (2018) to t −2.23 (2021).
- **F5:** The volume burst sets flush bars apart from other sharp falls over 3 days, but the wick does not. Sharp falls with a volume burst beat those without by +0.0168 in 3-day excess return (Welch t 2.00; n 163 vs 205). Among sharp falls without the burst, a close near the high predicts a weaker 3 days (slope t −2.99).
- **F6:** Coin by coin, no group carries the tested effect. Every coin's 3-day slope t lies between −0.15 and 1.45 (n 28 to 48), and the slope is not stronger among the deepest falls (t −0.25), the middle ones (t 0.78) or the shallowest (t −0.70).

## Ideas
- `012-03_lower-wick-flush-recovery.b1_lower-wick-rebound-more-coins` (from F1, F6): Among bars that fall sharply on a volume burst, the longer the lower wick below the close, as a share of the bar's high-to-low range, the larger the price rise over the next 3 days.
- `012-03_lower-wick-flush-recovery.b2_flush-closing-low-next-day-rebound` (from F2, F3, F4): Among bars that fall sharply on a volume burst, the nearer the close sits to the bar's low, as a share of the bar's high-to-low range, the larger the price rise over the next 1 day.
- `012-03_lower-wick-flush-recovery.b3_volume-burst-fall-rebound` (from F5, F3): Among bars that fall sharply, the larger the bar's volume relative to its prior 20-day mean, the larger the price rise over the next 3 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
