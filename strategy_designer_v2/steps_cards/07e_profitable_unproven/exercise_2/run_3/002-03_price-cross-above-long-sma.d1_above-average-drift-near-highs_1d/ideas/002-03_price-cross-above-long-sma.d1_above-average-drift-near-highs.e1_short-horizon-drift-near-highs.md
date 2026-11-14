---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs
line: 7.e profitable but not proven
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its long moving average, the nearer the close sits to its recent high and the stronger its recent rise, the larger the coin's excess gain over the following days to two weeks. This short-horizon drift has faded by about a month.
Consequence: A trader who goes long on strength above the long average should expect the edge in the first days to two weeks and size by how stretched toward the high the close is, not hold for a month expecting more.
Why:
- F1: The plan's own measure, (forecast/10) × the coin's excess return on non-overlapping grid bars with a positive forecast, is positive with t ≥ 2 at shorter horizons: t 2.21 at 1 bar (n 6090), 2.08 at 5 bars (n 1200) and 2.06 at 10 bars (n 598). At the plan's 20 bars it falls to t 0.61 (n 284), so the test measured the effect past the horizon where the book earns it.
- F3: The effect is graded in forecast strength. Among positive-forecast days, the next-day excess return rises from -0.00175 in the lowest forecast quartile (mean forecast 1.96) to 0.00349 in the top quartile (mean forecast 17.1), with Welch t 2.65 (n 1523 per quartile). At 10 bars the top quartile's excess is 0.041 against 0.0008 in the lowest (t 1.77, n 150).
- F4: On a coin's next day, the return averages 0.00197 when the book was in, against 0.00057 when it was out (n 7693 vs 9687), and the in-minus-out excess on the grid has Welch t 1.82 at 1 bar and 1.94 at 5 bars.
- F8: Within the forecast, the closeness of the close to its 20-day high carries more than the rise does. At 5 bars, the Spearman correlation with excess return is 0.040 for the transformed near-high part, against 0.034 for the transformed rise and -0.009 for the raw 20-day rise (n 1200).
