---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation
line: 7.b inconclusive
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day when a coin's volume is far above its 20-day average, the closer its close sits to the day's low, the more the coin rises over the next 1 day.
Consequence: A heavy-volume close at the bottom of the day's range is a reason to buy for a one-day rebound and to refuse a short into it.
Why:
- F2: On heavy-volume days (volume at least twice the prior 20-day mean, the heaviest day per 10-day cell, 654 cases), the close's position in the range adds nothing. High-close days minus low-close days differ by +0.04 % over 10 days (Welch t 0.03, 372 vs 282 cases), and the Spearman correlation of close location with the 10-day unusual move is -0.017. Low-close heavy days (close location ≤ -0.5) also rose +1.57 % (t 1.43, 133 cases).
- F5: At a one-day horizon the close location does carry information, in the reversal direction. Heavy-volume days closing in the bottom quarter of the range (close location ≤ -0.5) are followed by a next-day unusual move of +1.95 % (t 4.02, 149 cases). Heavy days closing just below the middle (-0.5 to 0) are followed by -1.01 % (t -2.34, 183 cases), and high-close heavy days by +0.02 % (t 0.04, 216 cases). The 1.95 % move is about ten times the 0.19 % cost of a trade.
