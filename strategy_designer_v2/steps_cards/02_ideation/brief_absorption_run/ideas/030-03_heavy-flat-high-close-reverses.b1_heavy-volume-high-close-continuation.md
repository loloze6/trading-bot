---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses
line: 7.b inconclusive
backtest: 030-03_heavy-flat-high-close-reverses_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: On a day when a coin's volume is far above its 20-day average, the closer its close sits to the day's high, the more the coin rises over the next 10 days, and the effect is larger the heavier that day's volume is.
Consequence: Continuation: a heavy-volume close near the high means buyers absorbed the day's selling and held the level, a reason to lean long and to refuse shorts after such days.
Why:
- F1: The tested short side was on the wrong side of the result: on heavy (volume ≥ 2x its prior 20-day mean) flat days, the 5-day unusual move after the bet's close was -0.74 % per case on the short side (t -0.94, 150 cases), so the coin rose more than its drift. Recomputed on the first heavy flat day of each 5-day cell, the move after a close in the top third of the range was +1.50 % (t 0.84, 43 cases), against +0.13 % after a close in the bottom third (40 cases), with a correlation of +0.12 between close location and the 5-day move.
- F2: Heavy-volume days that were not flat point the same way as F1, the opposite of the tested reversal, and more clearly: after a close in the top third of the range the unusual move was +1.75 % over 5 days (t 2.52, 323 cases) and +3.56 % over 10 days (t 3.07, 319 cases), against +0.13 % and +1.00 % after a close in the bottom third.
- F3: The link grows with volume and horizon. On a 10-day grid of all days with volume ≥ 2x the prior 20-day mean, the correlation of the 10-day unusual move is +0.09 with close location alone and +0.27 with close location x volume ratio (145 cases). The high-minus-low-close spread over 10 days is +14.9 % on days with volume ≥ 3x (t 1.33, 46 cases).
- F5: The signal is rare: flat heavy days give 20–26 cases per coin, and the book was in a position on 6 % of coin-days. The continuation move in F2 (+3.56 % over 10 days) is many times the 0.19 % cost of a trade, while the tested short's total move (-1.35 %) loses about 7 times that cost.
