---
brief: 019_quiet-range-then-breakout-on-four-hour-bars
source-idea: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week
line: 7.d not profitable
backtest: 019-03_upward-breakout-quiet-continuation.d1_breakout-after-quiet-week_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a four-hour bar closes above the highest high of a coin's preceding two-day stretch, the coin rises over the next three days, and the rise is larger the more active the coin's past 7 days were compared with its past 60 days.
Consequence: A trader should weight an upward breakout up, not down, when the preceding week was busier than the coin's usual two months.
Why:
- F5: The quiet-week weighting points the wrong way. In-position gain is largest when the past 7 days were busier than the past 60: 11.7 bps per bar in the top quintile of the 7-day/60-day volatility ratio (median 1.48, t 3.48), against 1.1 to 2.2 bps in the three quietest quintiles (t 0.55 to 1.36).
- F6: The quiet-week weight ratio tells the same story. Gain is 8.9 bps per bar (t 2.72) in its top quintile (7-day range 1.53 times the 60-day range), against 1.9 to 3.5 bps below it.
- F7: The idea's own move is smaller than a trade's cost. Per case, the unusual move is +0.18 % over 3 days (strength 0.020, t 1.13, 3102 cases), 0.9 times the 0.19 % round-trip cost. The total move is +0.58 %, 3.0 times the cost, so the book earns mostly from the coin's drift, which it takes while the coin is rising.
