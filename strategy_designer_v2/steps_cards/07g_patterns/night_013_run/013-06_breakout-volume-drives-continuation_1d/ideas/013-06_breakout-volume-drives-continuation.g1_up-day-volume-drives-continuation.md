---
brief: 013_anchoring-to-recent-high
source-idea: 013-06_breakout-volume-drives-continuation
line: 7.g patterns
backtest: 013-06_breakout-volume-drives-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day a coin closes higher, the larger that day's volume relative to its own 30-day average volume, the larger its return over the next 7 days.
Consequence: Heavy-volume up days, not only 52-week breakouts, would justify a long position sized up with the volume surge, while heavy volume on down days carries no such signal.
Why:
- F4: Volume predicts the next 7 days only after up days. The slope of the 7-day excess return on the log of the day's volume over its prior 30-day mean has t = 3.60 (n = 848) when the day closed up, against t = 0.14 (n = 938) when it closed down.
- F5: The volume effect is not limited to the breakouts the strategy trades.
