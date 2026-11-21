---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal
line: 7.g patterns
backtest: 017-05_settlement-move-reverses-after.g2_volatility-scaled-two-hour-reversal_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: A coin's 2-hour move in the same direction as its 24-hour return reverses over the next 2 hours by more as that 24-hour return grows in the coin's own volatility units.
Consequence: A trader should fade short spikes that extend an already stretched daily run, and stand aside from spikes that come without such a run.
Why:
- F5: Among large 2-hour moves that go the same way as the coin's 24-hour return, the fade grows with the size of that 24-hour return in volatility units, by quartile: 4.0 bp (t 1.9), 4.2 bp (t 2.1), 6.3 bp (t 3.0), 16.2 bp (t 5.3), with 5573 to 7897 cases.
- F2: The reversal is lopsided. In the bottom decile of the 2-hour move (big falls, mean z -2.74), the next 2 hours return +12.3 bp in excess (t 8.2, n 19950). In the top decile (big rises, mean z +2.75), they return only -3.7 bp (t -2.9). In that falls decile, 8.4 bp of the fade comes in the first hour against 4.9 bp in the second, which contradicts the idea's claim that most of the reversal comes in the second hour.
