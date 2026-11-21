---
brief: 016_grind-versus-jump-moves
source-idea: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold
line: 7.d not profitable
backtest: 016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: The more heavily a coin traded during a 1-day fall, relative to its 30-day average volume, the more it rises over the next 3 days, while a fall on light volume is followed by a further decline over the next 3 days.
Consequence: Read the volume of a down day as the sign of whether to fade it or follow it.
Why:
- F2: On the non-overlapping 72-bar grid bars with a long forecast, how much the coin traded over the last day decides the outcome. In the quietest quarter, where 24-hour volume is lowest against its 30-day mean, the next-3-day excess return is -0.0132 (t -3.17, n 448). In the busiest quarter it is +0.0095 (t 2.34, n 448). The same split holds over all grid bars with both a 3-day and a 1-day fall.
- F4: The forecast's size alone is not enough. Its two lower quarters lose (-0.0103, t -2.51, n 473; -0.0058, t -1.47, n 473), and only the upper half gains (+0.0047, t 1.85, n 945). The size of the 1-day fall multiplied by its volume ratio grades better: its quintiles run monotonically from -0.0115 (t -2.80) to +0.0110 (t 2.10), n 275 each.
