---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 3 days, and the deeper its 3-day fall, the larger that rebound, only while the coin has risen over the past 30 days, with the rebound larger the stronger that 30-day rise.
Consequence: Buy fresh drops in proportion to their depth when the coin's month is rising, and refuse them when its 30-day trend is down, which is where the book's deepest falls came from.
Why:
- F2: The book's worst windows are the ones where the coins themselves fell. In w2 the book returned -0.0029 a day while the coins returned -0.0038; in w14 it was -0.0019 against -0.0043, in w7 -0.0014 against -0.0047, in w1 -0.0014 against -0.0015, and in w9 -0.0010 against -0.0026. So the rebound bet keeps buying falls that continue when the larger trend is down, and these windows carry the falls and the one-window-left-out weakness.
- F3: On the 72-bar grid, the active cases with a 30-day (720-bar) return in the top third returned +0.0081 over the next 3 days (t 2.56, n 679). Those in the bottom third returned only +0.0003 (t 0.09, n 678), and the middle third returned -0.0016 (n 678). The highest forecast tercile inside the rising-month group returned +0.0197, against +0.0010 in the falling-month group.
- F1: The book barely earns while simply holding the coins earns far more. Its mean daily return is 5.6e-05 against roughly 0.0007–0.0016 a day for holding each coin. Its chained yearly return is -0.7%, with a deepest fall of -49%. Its 3761 trades average -1.35% before fees and -1.45% after, with a 48.8% win rate.
