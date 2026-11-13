---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-04_rebound-after-large-drop
line: 7.g patterns
backtest: N1-04_rebound-after-large-drop_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily bar falls and closes in the bottom fifth of an unusually wide range (wide against its recent ranges), the next day's close is higher more often than on ordinary days.
Consequence: Buy a down day only when it closes near the low of an expanded range, and skip drops that recovered toward the high before the close.
Why:
- F1: On down days the next-day rebound depends on where the bar closed within its range. Down days closing in the bottom 20% of the range were followed by a rise 57.6% of the time, with a mean of +0.49% (t 4.62, n 2163). Down days closing in the top 20% rose only 46.6% of the time, with a mean of -0.34% (t -0.88, n 116).
- F2: Within the forecast's own large drops (z ≤ -1.88) the same split holds. Drops that closed in the bottom 20% of the range rose next day 62.9% of the time, mean +1.01% (t 4.29, n 580). Drops that closed above mid-range rose only 47.3% of the time, mean -0.53% (t -0.78, n 55). The idea's drop size does not capture this.
- F3: The low-close rebound grows with range expansion against the prior 20 days.
