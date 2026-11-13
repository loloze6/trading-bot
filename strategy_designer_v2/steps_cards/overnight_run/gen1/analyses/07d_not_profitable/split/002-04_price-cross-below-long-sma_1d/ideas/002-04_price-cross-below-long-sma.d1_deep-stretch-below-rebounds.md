---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-04_price-cross-below-long-sma
line: 7.d not profitable
backtest: 002-04_price-cross-below-long-sma_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close sits far below its 200-day average, more than about a fifth of the way down, the coin tends to rise over the following days, a rebound from deep stretch rather than further decline.
Consequence: A trader should not short a coin that is deeply below its long average, and could take the long side of a rebound there.
Why:
- F2: A larger forecast loses more: bars with forecast below -15 (mean allocation -1.79) saw the coin rise +0.447% per day, for a gross -0.0083 per bar and a summed gross of -10.97 out of the total -12.27 on active bars; a unit short there earns -0.0045 per day (t = -3.24), against +0.00085 (t = 0.77) in the -15..-10 bin.
- F3: The deepest distances below the SMA200 rebound: in the two deepest raw-distance quintiles (-72.9 to -34.8 % and -34.8 to -21.3 %) the coin rose +0.177% and +0.211% per day and the book lost -0.0032 and -0.0030 per bar, while the middle quintile (-21.3 to -12.3 %) was flat at +0.00013.
- F4: Across all active bars the coin rose more while the book was short (+0.136% per day) than while it was flat (+0.120% per day), and a unit short over all active bars earns -0.00136 per day (t = -2.97), which is a reversal, not downward persistence.
