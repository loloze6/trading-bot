---
brief: 030_absorption-day-close-location
source-idea: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g1_heavy-fall-closing-at-low
line: 7.g patterns
backtest: 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b1_volume-surge-precedes-rise.d2_volume-surge-next-day-rise.g1_heavy-volume-selloff-next-day-rebound.g1_heavy-fall-closing-at-low_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: The larger a coin's one-day fall, and the higher its 20-day volatility against its own past level, the more it rises over the next day.
Consequence: A trader buys a coin for a day after a sharp fall in a turbulent market, and refuses to buy after the same fall in a calm market.
Why:
- F1: The coin's 20-day volatility sets the size of the next-day reversal. In the coins' own top third of 20-day volatility, a down day is followed by a next-day excess return of +0.71 % (t 5.59, 2357 days) and an up day by -0.36 % (t -3.20, 2491 days). In the bottom third, down days are followed by -0.16 % (t -2.03) and up days by -0.00 % (t -0.03).
- F2: The reversal is graded by the size of the move times the volatility level. On down days, regressing the next-day excess return on the day's return gives t 2.63 for the return alone and t -6.64 for the return × relative volatility term (7151 days). On all days the return × relative volatility term has t -4.34 (14500 days).
- F3: Inside the high-volatility third, the next day follows the day's return quintile in a steady line: +1.13 % (t 5.18) after the largest falls, +0.45 % (t 2.31), -0.00 %, -0.46 % (t -2.64), and -0.32 % (t -1.59) after the largest rises, about 970 days each. In the low-volatility third, no quintile goes past +0.10 % or below -0.26 %.
- F4: The high-volatility reversal (next-day return signed against the day's move) is broad.
