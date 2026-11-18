---
line: 7.g patterns
backtest: 012-03_lower-wick-flush-recovery_1d
idea tested: 012-03_lower-wick-flush-recovery
step 5: mismatch
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.4575 USD
---
## Findings
- **F1:** On down days, sampled on each window's 0,3,6,... grid, the coin's excess 3-day return rises with the log of the day's volume over its prior 20-day median: slope 0.0126, t 4.72, n 2245. The slope stays at t 4.44 once the day's volatility-scaled return is controlled for. It has the same sign in both halves (w1-12 t 2.79, w13-24 t 3.78) and in 7 of 8 years, and it is positive for all six coins (t from 0.36 for BTC to 2.55 for ZEC).
- **F2:** The effect is graded in volume. Excess 3-day returns on down days are -0.0026 (t -1.10, n 1203) at volume ratio ≤1, +0.0014 (n 237) at 1.5–2, +0.022 (t 2.76, n 174) at 2–3, +0.035 (t 3.25, n 91) at 3–5 and +0.060 (t 2.33, n 34) above 5. On up days the slope is the other way and not significant: -0.0030, t -1.35, n 2466.
- **F3:** The tested wick share adds nothing among sharp falls on a volume burst. On grid events with z ≤ -1.5 and volume ratio ≥2, the slope of excess 3-day return on wick share is 0.0067 (t 0.16, n 109). With overlapping events, burst falls give +0.019 at the low-wick tercile and +0.0097 at the high-wick tercile. The rebound is carried by the volume, not the wick.
- **F4:** The book barely trades and loses. It is in position on about 1.5% of bars (522 of 17,524 coin-days), with a mean in-position daily return of -0.00014 and a Sharpe of -0.03. The trigger requires z ≤ -2 together with a volume burst, which leaves out most of the high-volume down days that carry F1.
- **F5:** Next-day returns after Thursday and Friday bars are positive in excess of the coin's mean in both halves (t 2.72 and 3.52, n ≈ 2480 each), for all six coins, and in 7 of 8 years. This calendar pattern does not come from the brief, and after the many angles examined it is noted only as secondary.

## Ideas
- `012-03_lower-wick-flush-recovery.g1_high-volume-down-day-rebound` (from F1, F2, F3, F4): On a day a coin closes lower, the larger that day's volume relative to its median over the prior 20 days, the larger the coin's rise over the next 3 days.
- `012-03_lower-wick-flush-recovery.g2_volume-not-fall-size-drives-rebound` (from F1, F3): The larger a coin's volume on a down day relative to its prior 20-day median, the larger its excess rise over the next 3 days, whatever the size of that day's fall in units of its 20-day volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
