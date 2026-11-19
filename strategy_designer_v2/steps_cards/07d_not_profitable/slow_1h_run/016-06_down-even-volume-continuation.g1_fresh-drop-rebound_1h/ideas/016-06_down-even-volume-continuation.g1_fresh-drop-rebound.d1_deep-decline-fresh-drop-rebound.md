---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 3 days, and the deeper its 3-day fall, the larger that rebound.
Consequence: Buy the rebound in proportion to both the depth of the 3-day decline and the size of the fresh 1-day drop, and refuse it after mild 3-day declines where the coin keeps underperforming.
Why:
- F4: The rebound sits in the deepest 3-day falls only. The excess 72-hour return was +0.0092 in the deepest tercile (t 2.32, n 608), -0.0059 in the middle tercile (t -1.81, n 609) and -0.0088 in the shallowest (t -3.17, n 608). Deep 3-day falls combined with big 1-day falls gave +0.0133 (n 371).
- F5: Inside the active cases, a larger 1-day fall pays and a small one loses. The biggest 1-day-fall tercile earned +0.0076 excess (t 2.03), and the smallest earned -0.0097 (t -3.38). Grid bars with forecasts between 0 and 8 averaged -0.006 to -0.009 excess (n 695), while forecasts from 8 to 21 averaged +0.0013 (n 1,196).
- F6: Taken equally weighted, the active grid cases do not beat the coin's average. Their mean excess was -0.0017 (t -0.87, n 1,891), and the edge appears only when weighted by forecast (+0.0027). The weak cases, which come from mild 3-day falls, dilute it.
