---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: After a daily close that falls by more than one standard deviation of the coin's last 20 daily returns, the coin's next-day return is above its average day, and more so when the close is below its 200-day simple moving average.
Consequence: A trader should refuse to sell, or should buy, at the close of a sharp down day, especially in a coin trading below its long average.
Why:
- F1: A daily fall larger than one standard deviation of the coin's last 20 daily returns is followed by an above-average next day: z in (-2,-1] gives +0.48% excess (n=1272, t=3.29, 57.4% positive), z in (-3,-2] gives +0.50% (t=1.93, 58.7%) and z ≤ -3 gives +0.86% (t=1.49, 60.9%), while rises of the same size give no such effect (z in (1,2] gives -0.04%, t=-0.32).
- F2: This next-day rebound after a ≥1-sd fall shows in all six coins (excess +0.22% to +0.92%, 55–62% positive, strongest in XMR at t=3.36) and in 7 of 8 years.
- F3: The rebound is about twice as large when the close is below its 200-day SMA (+0.69%, n=993, t=3.90, 58.3% positive) as when it is above (+0.30%, n=753, t=1.61).
