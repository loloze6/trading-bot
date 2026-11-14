---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs
line: 7.e profitable but not proven
backtest: 002-03_price-cross-above-long-sma.d1_above-average-drift-near-highs_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin trades above its long moving average with its close near the recent high, its next-day returns are skewed to the upside: rare large up days follow more often than usual, and they carry the gain while the typical day is flat to slightly negative.
Consequence: A trader in this situation earns from staying exposed to occasional large up days, so cutting winners early or trading only the median outcome gives up the edge.
Why:
- F2: Timing carries more of the book than the market's rise: of the book's mean daily return of 0.000565, the position × coin-mean drift part is 0.000224 and timing is 0.000340, while the mean allocation is only 0.19.
- F5: The gain sits in a fat right tail. Dropping the best 1 % of the book's 2898 days takes the mean daily return from 0.000565 to -0.000003. The top 5 % of the 2888 trades sum to 21477 of the total 26441 P/L points, while the median trade is -0.78 % and 44.7 % of trades win.
- F3: The effect is graded in forecast strength. Among positive-forecast days, the next-day excess return rises from -0.00175 in the lowest forecast quartile (mean forecast 1.96) to 0.00349 in the top quartile (mean forecast 17.1), with Welch t 2.65 (n 1523 per quartile). At 10 bars the top quartile's excess is 0.041 against 0.0008 in the lowest (t 1.77, n 150).
