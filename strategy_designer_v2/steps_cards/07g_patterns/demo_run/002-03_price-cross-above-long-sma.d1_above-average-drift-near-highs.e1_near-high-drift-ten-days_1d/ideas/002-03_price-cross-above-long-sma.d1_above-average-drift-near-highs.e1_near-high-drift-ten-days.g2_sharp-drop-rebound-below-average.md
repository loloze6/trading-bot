---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days
line: 7.g patterns
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs.e1_near-high-drift-ten-days_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: While a coin's close is below its 200-day average, the larger its one-day fall measured against its 30-day daily volatility, the larger its rebound over the next 1 to 3 days.
Consequence: Below the long average, a trader would buy unusually sharp one-day drops for a short hold, sized by how extreme the drop is, rather than sell them.
Why:
- F4: Large one-day falls tend to reverse the next day. Days in the lowest decile of return scaled by 30-day volatility are followed by an excess next-day return of +0.0061, against roughly -0.002 to +0.002 in deciles 3 to 10 (1,436 cases each).
- F5: That reversal is graded on down days. The slope of next-day excess return on the scaled fall is negative in all six coins, with t of -4.42 for XMR, -3.12 for XRP and -2.00 for ZEC.
- F6: The reversal is stronger below the 200-day average. After the lowest-decile days the next-day excess is +0.0084 below the average (808 cases) and +0.0031 above it (628 cases). On a non-overlapping 3-day grid, the lowest quintile still gains +0.0043 over the next 3 days (943 cases).
