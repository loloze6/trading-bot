---
brief: 002_moving-average-cross-trend-persistence
source-idea: N1-04_rebound-after-large-drop
line: 7.d not profitable
backtest: N1-04_rebound-after-large-drop_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's next-day rebound after a down day appears when its recent daily moves are larger than its usual size, and is stronger the more volatile the recent days are. In calm periods a down day is followed by a slightly weaker than average next day.
Consequence: Hold the rebound long only when the coin's trailing volatility is above its norm, and stay flat after small drops in calm periods, which carry exposure without gain.
Why:
- F3: The gain sits in the large positions. Bars with a forecast of 16 or more (n=1280, one-bar horizon, so the cases are independent) earn 0.62% above the coin's all-window mean (t 3.80), with a hit rate of 0.608. The small positions with a forecast in (0,5] (n=6068) earn only 0.02% above the coin's mean (t 0.40), so they keep the book exposed to the crash days with no edge.
- F6: The rebound grows with volatility:
- F1: The book fails only on Calmar (0.748 against 0.75); its pooled daily equity falls 46.2% at its deepest. The deepest falls inside windows are w9 (-40.5%), w13 (-36.2%), w14 (-32.9%), w2 (-32.3%) and w3 (-32.2%). In each of these the coins themselves fell 44% to 68%.
