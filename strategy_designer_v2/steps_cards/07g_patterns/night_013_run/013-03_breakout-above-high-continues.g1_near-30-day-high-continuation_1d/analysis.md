---
line: 7.g patterns
backtest: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation_1d
idea tested: 013-03_breakout-above-high-continues.g1_near-30-day-high-continuation
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3723 USD
---
## Findings
- **F1:** The 10-day edge sits only in the closest-to-high quintile. On non-overlapping 10-day samples, the excess return by distance-to-30-day-high quintile is −0.010, −0.0075, −0.0014 and −0.0108 for q0 to q3 (none with |t| above 1.3), against +0.030 (t 2.48, n 252) for the top quintile (mean distance −1.4 %). Per-coin slopes are significant only for XRP (t 2.60) and ZEC (t 2.46); BTC, LTC and XMR have slopes at or below 0.
- **F2:** Among near-high samples (top 40 % of distance per coin), heavy recent volume carries the follow-through. With 5-day volume over 30-day volume in its top tercile, the excess 10-day return is +0.042 (t 2.77, n 168), against −0.006 and −0.007 in the lower terciles. The high-minus-low Welch t is 2.47, and the slope on log relative volume has t 3.80.
- **F3:** The near-high volume gap has the same sign in all six coins (high minus low: BTC +0.030, ETH +0.018, LTC +0.016, XMR +0.077, XRP +0.062, ZEC +0.085). In coins far below the high it reverses (low-volume tercile +0.008, high −0.020). The gap is concentrated in windows w13–w24 (+0.076 vs −0.033); in w1–w12 it is +0.006 vs +0.012.
- **F4:** A 1-day move scaled by 20-day volatility is followed by a next-day reversal. The pooled slope t is −4.99, negative in w1–w12 (t −3.42) and in w13–w24 (t −3.65), and negative in all six coins (XMR t −5.26, ETH −2.63, LTC −2.22). It is gone at 3 days (non-overlapping t −0.33, n 5003).
- **F5:** The reversal is graded and lives in high-volatility conditions. When 20-day volatility is above the coin's median, next-day excess return runs +0.0245 after moves below −2σ (n 170), +0.0098 after −2σ to −1σ, −0.0040 after 0 to +1σ and −0.0075 after more than +2σ. In low-volatility conditions the pattern is flat or inverted (−0.0043 after below −2σ, +0.0057 after above +2σ).
- **F6:** The book's gain comes only from the top distance quintile. There it averages 0.00081 daily at a mean allocation of +0.23; every other quintile earns between −0.00025 and +0.00005. The short-leaning bottom quintile (allocation −0.096) loses while its coins' next-day excess return is +0.00088.
- **F7:** The positions are small and correlate with distance. Mean allocation is 0.009 with standard deviation 0.177, and its correlation with distance is 0.54. The book's mean daily return is below holding in most windows (for example w11: 1.7 vs 125.6 ×1e-4), consistent with its Sharpe of 0.29 against holding's 0.55.

## Ideas
- `013-03_breakout-above-high-continues.g1_near-30-day-high-continuation.g1_volume-backed-near-high-continuation` (from F2, F3, F1): When a coin closes near the highest high of its prior 30 days, the heavier its traded volume over the last 5 days relative to its 30-day average, the larger its return over the next 10 days.
- `013-03_breakout-above-high-continues.g1_near-30-day-high-continuation.g2_volatile-regime-one-day-reversal` (from F4, F5): When a coin's 20-day volatility is high, the larger its 1-day return relative to that volatility, the lower its return over the next 1 day, with sharp down days followed by the strongest rebounds.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
