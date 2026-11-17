---
brief: 013_anchoring-to-recent-high
source-idea: 013-06_breakout-volume-drives-continuation
line: 7.g patterns
backtest: 013-06_breakout-volume-drives-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall measured against its own 20-day daily volatility, on a day whose volume is above its 30-day average, the larger its rise over the next 1 day.
Consequence: Outsized heavy-volume falls are a reason to lean long for a day rather than chase the move down.
Why:
- F3: A day's return scaled by its 20-day volatility predicts a next-day reversal. The bottom quintile (the largest falls) is followed by +0.0040 and the top quintile by -0.0010, Welch t -3.83 with 14907 cases. The effect sits on heavy-volume days (hi-minus-lo -0.0061, t -2.91) and is absent on light-volume days (-0.0003, t -0.20). In a joint regression it stays at t -3.74 next to log relative volume at t +4.13.
- F4: The reversal after scaled one-day moves is negative in 5 of 6 coins on the next day (XMR -0.0098, t -3.45), and its rank correlation is negative in every coin, from -0.033 to -0.104. By year it is strongest in 2018, 2020 and 2023 (t -2.76, -2.92, -3.23) and fades in 2024 and 2025 (t +1.02, +0.86).
- F1: On all bars (one-day non-overlapping grid, coin-demeaned), a day's volume relative to its 30-day average predicts the next day's return only after down days: on down days the top volume quintile minus the bottom quintile is +0.0093, Welch t 4.89, with 7086 cases; on up days it is +0.0001, t 0.06, with 7257 cases.
