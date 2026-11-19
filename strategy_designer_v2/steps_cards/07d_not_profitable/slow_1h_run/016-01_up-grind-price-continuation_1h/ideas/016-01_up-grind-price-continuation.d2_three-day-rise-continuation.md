---
brief: 016_grind-versus-jump-moves
source-idea: 016-01_up-grind-price-continuation
line: 7.d not profitable
backtest: 016-01_up-grind-price-continuation_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The larger a coin's rise over the past 3 days, the more the coin keeps rising over the next 3 days.
Consequence: A trader would lean long, and more so, on coins with a larger 3-day rise, and hold for days.
Why:
- F3: The slow situation itself does carry gain at 3 days: on the non-overlapping 72-bar grid, risen windows return 0.0052 over the next 72 bars against 0.0014 for the others, and grid cases with a forecast above 0 return 0.0125 (n = 938) against 0.0034 for holding the coin.
