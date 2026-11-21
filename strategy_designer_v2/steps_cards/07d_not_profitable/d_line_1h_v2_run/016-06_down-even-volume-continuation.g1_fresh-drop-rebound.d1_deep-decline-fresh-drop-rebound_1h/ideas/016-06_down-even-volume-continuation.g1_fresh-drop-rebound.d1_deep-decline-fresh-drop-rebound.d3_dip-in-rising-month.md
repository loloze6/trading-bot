---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 30 days, the deeper its fall over the past 3 days, the more it rises over the next 3 days.
Consequence: Treat dips inside a rising month as buying opportunities, scaled by the depth of the dip.
Why:
- F3: On the 72-bar grid, the active cases with a 30-day (720-bar) return in the top third returned +0.0081 over the next 3 days (t 2.56, n 679). Those in the bottom third returned only +0.0003 (t 0.09, n 678), and the middle third returned -0.0016 (n 678). The highest forecast tercile inside the rising-month group returned +0.0197, against +0.0010 in the falling-month group.
- F6: Being in the fall regime costs the book the market's rise. Grid bars with a positive forecast returned +0.0026 over the next 3 days, against +0.0055 on the 2921 bars the book sat flat. Window fees of 0.014–0.020 per coin eat about half of the window gross of -0.003 to +0.071, and ETH's gross is negative.
