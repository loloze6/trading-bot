---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-05_failed-breakout-multiday-drift
line: 7.g patterns
backtest: 029-05_failed-breakout-multiday-drift_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The heavier a coin's volume on a down day, relative to its 20-day average volume, the larger its rise over the next 8 days.
Consequence: A short taken right after a heavy-volume down day is likely to meet a rebound and should be refused.
Why:
- F6: Down days on heavy volume rebound most. A down day in the highest tercile of volume against its 20-day mean is followed by +3.04 % over 8 days (t 2.94, 294 cases), against +0.96 % (t 1.14) in the lowest tercile. An up day in the lowest volume tercile is followed by -1.73 % (t -2.57).
- F1: Over 8 days a coin moves against its last daily return, scaled by its 20-day volatility. Regressed on that scaled return, the 8-day unusual move has a slope of -0.0165 with t -4.57 over 1691 independent cases. The lowest quintile is followed by +2.87 % (t 3.20) and the fourth quintile by -2.30 % (t -3.64).
