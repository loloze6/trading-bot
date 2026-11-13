---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-06_deep-below-average-rebound
line: 7.g patterns
backtest: N1-06_deep-below-average-rebound_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin trading below its 200-day average closes a day down by more than its usual daily move (at least one 20-day standard deviation), it rises the next day more often than on an ordinary day, because forced and panicked sellers in a downtrend overshoot and are absorbed within a day.
Consequence: A trader can take a one-day long after an outsized down close below the SMA200, and avoid opening fresh shorts on that close.
Why:
- F1: Across all six coins, a daily drop of 1 to 2 times the coin's 20-day volatility is followed by a next-day excess return of +0.42% (t=3.03, n=1276 one-day cases, 58% up), every bucket with a drop of 1 sigma or more rises the next day 58-61% of the time, and a rise of 1 sigma or more is followed by an up day only 41-47% of the time.
- F2: The next-day rebound after a drop of 1 sigma or more is larger when the close is below its SMA200, at +0.57% (t=3.29, n=1013, 59% up), than above it, at +0.25% (t=1.34, n=794); it is positive in all six coins (strongest in XMR, +0.84%, t=3.08, n=301) and in six of eight years (2020 t=2.61, 2021 t=3.44), though it fades to about zero in 2024-2025.
