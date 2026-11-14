---
brief: 002_moving-average-cross-trend-persistence
source-idea: 002-01_sma-golden-cross-upward-drift
line: 7.d not profitable
backtest: 002-01_sma-golden-cross-upward-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: (new idea) In one coin, the closer the close stands to its recent high, the larger its rise over the following days; the further below that high it stands, the more it keeps falling.
Consequence: Rank long exposure by how near price is to its recent high rather than by the moving-average spread, which carries no graded information.
Why:
- F2: The spread size that sets the forecast does not grade what follows. Its active quartiles give 10-bar excesses of +0.001, +0.013, -0.005 and -0.007, with no |t| above 1.04, which is why the main slope's t is 0.37.
- F4: How close price sits to its recent high grades the gain the same way. In the active state, bars at the 30-bar high are followed by a 10-bar excess of +0.041 (t 2.37). Bars in the deepest quartile below it (median -0.28) are followed by -0.022 (t -2.03).
- F8: The mean daily gain is starved by small positions. The lowest forecast bucket (0-5) holds a mean allocation of 0.13 and earns -0.000011 a day while the coin earns 0.000909. The 8453 flat days earn about zero while the coin earns 0.0013.
