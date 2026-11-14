---
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
idea tested: 002-03_price-cross-above-long-sma
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3382 USD
---
## Findings
- **F1:** A daily fall larger than one standard deviation of the coin's last 20 daily returns is followed by an above-average next day: z in (-2,-1] gives +0.48% excess (n=1272, t=3.29, 57.4% positive), z in (-3,-2] gives +0.50% (t=1.93, 58.7%) and z ≤ -3 gives +0.86% (t=1.49, 60.9%), while rises of the same size give no such effect (z in (1,2] gives -0.04%, t=-0.32).
- **F2:** This next-day rebound after a ≥1-sd fall shows in all six coins (excess +0.22% to +0.92%, 55–62% positive, strongest in XMR at t=3.36) and in 7 of 8 years.
- **F3:** The rebound is about twice as large when the close is below its 200-day SMA (+0.69%, n=993, t=3.90, 58.3% positive) as when it is above (+0.30%, n=753, t=1.61).
- **F4:** Wednesday closes are followed by a below-average next day (excess -0.30%, n=2437, t=-2.75, 45.2% positive), and this is negative in all six coins (-0.14% to -0.40%).
- **F5:** Friday closes are followed by an above-average next day (excess +0.30%, n=2430, t=3.66, 51.7% positive), positive in all six coins; Thursday is also positive (+0.21%, t=2.29, positive in all six coins), while Monday is negative (-0.22%, t=-2.34, negative in 5 of 6 coins).
- **F6:** The book's edge comes from a few long holds: its 2228 trades win only 29.4% of the time with a median of -3.7%, trades shorter than 20 days lose on average (-4.4% to -6.5%), and trades longer than 60 days average +60.7% (n=204).
- **F7:** The forecast's weakest positive values (0–5, the close only just above its typical distance from the SMA) are followed by underperformance (20-bar excess -2.9%, t=-5.79 on overlapping bars), but on non-overlapping blocks this weakens to t=-1.63, so it is suggestive only.

## Ideas
- `002-03_price-cross-above-long-sma.g1_sharp-down-day-next-day-rebound` (from F1, F2, F3): After a daily close that falls by more than one standard deviation of the coin's last 20 daily returns, the coin's next-day return is above its average day, and more so when the close is below its 200-day simple moving average.
- `002-03_price-cross-above-long-sma.g2_weak-thursday-after-wednesday-close` (from F4): A coin's return from Wednesday's close to Thursday's close is below its average daily return.
- `002-03_price-cross-above-long-sma.g3_strong-day-after-friday-close` (from F5): A coin's return from Friday's close to Saturday's close is above its average daily return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
