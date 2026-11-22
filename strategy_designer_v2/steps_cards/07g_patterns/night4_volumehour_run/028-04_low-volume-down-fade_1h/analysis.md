---
line: 7.g patterns
backtest: 028-04_low-volume-down-fade_1h
idea tested: 028-04_low-volume-down-fade
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3496 USD
---
## Findings
- **F1:** Across the 6-hour grid, large falls, large rises and volume levels do not sort the next 6 hours' unusual move: of the 28 cells (seven bands of the hour's move in usual moves, four bands of volume ratio), none reaches |t| 2.2. The largest are quiet-volume falls of 1.5 to 2.5 usual moves with volume under 2/3 of average (+27 bp, t 2.14, n 277), rises of 2.5 to 4 usual moves with volume over 3 times average (+49 bp, t 1.85, n 111), and falls of 2.5 to 4 usual moves with volume over 3 times average (+60 bp, t 1.56, n 116).
- **F2:** The band the idea traded, falls of 1.5 to 2.5 usual moves with volume between 2/3 and 1.5 times average, is followed by +15 bp over 6 hours (t 1.48, n 503). Deeper falls in that band are followed by −4 bp (2.5 to 4 usual moves, n 182) and −47 bp (beyond 4, n 23). The gradient runs against the idea, which matches the failed supporting check (−0.02 %).
- **F3:** Over 24 hours, falls beyond 2.5 usual moves are followed by +56 bp unusual move (t 1.54, n 232), and rises beyond 2.5 by +3 bp (t 0.08, n 233); neither is distinguishable from chance.
- **F4:** Neither the prior 24-hour return quintile (|t| ≤ 1.73) nor the volatility quintile (|t| ≤ 1.97) orders the next 6 hours' unusual move.
- **F5:** By weekday, the only extreme is Thursday at −14 bp over 6 hours (t −3.59, n 3046); the others lie within ±9 bp and |t| 2.4. By 3-hour block, 00–03 UTC shows −7.5 bp (t −2.87, n 4817). These are calendar cells taken from about 50 groupings, with no graded situation behind them.
- **F6:** The book moves with the coin at about one fifth of the coin's daily move: on the coin's worst-quintile days the book makes −130 bp against −511 bp, and on its best-quintile days +92 bp against +553 bp. This is the residue of being long only, not timing.
- **F7:** Trades are positive before fees: BTC +0.08 % on average over 6608 trades (61 % winners), ETH +0.23 % over 6128 (65 %). After the 0.11 % cost per trade, BTC loses (−0.02 %) and ETH keeps +0.13 %. The idea's measured total move per case (+0.07 %) stays below the cost.

## Ideas
- No ideas: Across the moves, volume, regime, volatility, weekday, hour, horizon and book angles I examined, no graded pattern stands out above what roughly 70 cells of chance would produce. The one cell that does (Thursday, t −3.6) is a calendar condition, not a graded situation.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
