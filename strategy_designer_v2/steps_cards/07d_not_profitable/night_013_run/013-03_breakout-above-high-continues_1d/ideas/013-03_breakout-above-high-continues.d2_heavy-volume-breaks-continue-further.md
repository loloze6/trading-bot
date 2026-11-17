---
brief: 013_anchoring-to-recent-high
source-idea: 013-03_breakout-above-high-continues
line: 7.d not profitable
backtest: 013-03_breakout-above-high-continues_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its prior 52-week high, the further above that high it closes and the heavier its volume on that day relative to its own 30-day average volume, the larger its return over the next 30 days.
Consequence: High-volume breaks deserve the larger position, and quiet breaks a smaller one.
Why:
- F7: Volume adds to the break. Breaks on volume above the median of their ratio to the prior 30-day mean volume returned 23.8 % over 30 days (n 24), against 10.8 % for the low-volume breaks (n 25). This matches the brief's heavy-volume clearing.
- F3: The break does continue, but over days, not over one bar. Across the 75 fresh breaks (the first break after at least 10 days without one), the coin rose on average 2.1 % over the next day, 6.1 % over 5 days, 9.5 % over 10 days (n 73) and 15.8 % over 30 days (n 52). The book captured almost none of this.
- F6: The size of the break predicts the next 10 days, but not later. At the break itself, the 10-day return rises with the distance above the old high (slope 0.0121, t 3.15, n 73). The 30-day slope is weaker (t 1.87, n 52). On the later days, the distance above the broken high carries nothing: daily slope t −0.41 (n 1517), 10-day grid slope t 0.15 (n 141).
