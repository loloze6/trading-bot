---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 3 days, only while that 1-day fall came with heavy trading, and the heavier the last day's volume against its usual 30-day level, the larger the rise.
Consequence: Buy fresh drops made on a burst of volume, and refuse those made on thin trading, which keep falling.
Why:
- F1: Of the book's mean daily return of 0.000115, the market's own rise accounts for 0.000397 (mean position 0.34), so the timing part is -0.000281: being long after 1-day falls has cost money against simply holding, which is why the Sharpe trails holding's by 0.41 and the mean daily return stays below 0.0005.
- F2: On the non-overlapping 72-bar grid bars with a long forecast, how much the coin traded over the last day decides the outcome. In the quietest quarter, where 24-hour volume is lowest against its 30-day mean, the next-3-day excess return is -0.0132 (t -3.17, n 448). In the busiest quarter it is +0.0095 (t 2.34, n 448). The same split holds over all grid bars with both a 3-day and a 1-day fall.
- F4: The forecast's size alone is not enough. Its two lower quarters lose (-0.0103, t -2.51, n 473; -0.0058, t -1.47, n 473), and only the upper half gains (+0.0047, t 1.85, n 945). The size of the 1-day fall multiplied by its volume ratio grades better: its quintiles run monotonically from -0.0115 (t -2.80) to +0.0110 (t 2.10), n 275 each.
